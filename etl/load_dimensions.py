import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "manufacturing_dw"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

if not DB_CONFIG["password"]:
    raise RuntimeError("DB_PASSWORD is not configured. Create a .env file from .env.example.")

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Connected to PostgreSQL successfully.")
except Exception as e:
    print("Database connection failed:")
    print(e)
    raise SystemExit(1)

try:
    cursor.execute("""
        UPDATE dim_product d
        SET
            effective_end_date = CURRENT_DATE - 1,
            is_current = FALSE
        FROM stg_products s
        WHERE d.product_id = s.product_id
          AND d.is_current = TRUE
          AND (
              d.product_name IS DISTINCT FROM s.product_name
              OR d.product_category IS DISTINCT FROM s.product_category
              OR d.product_type IS DISTINCT FROM s.product_type
              OR d.unit_of_measure IS DISTINCT FROM s.unit_of_measure
              OR d.standard_cost IS DISTINCT FROM s.standard_cost
              OR d.product_status IS DISTINCT FROM s.product_status
          );
    """)

    cursor.execute("""
        INSERT INTO dim_product (
            product_id, product_name, product_category, product_type,
            unit_of_measure, standard_cost, product_status,
            effective_start_date, effective_end_date, is_current
        )
        SELECT
            s.product_id, s.product_name, s.product_category, s.product_type,
            s.unit_of_measure, s.standard_cost, s.product_status,
            CURRENT_DATE, DATE '9999-12-31', TRUE
        FROM stg_products s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_product d
            WHERE d.product_id = s.product_id
              AND d.is_current = TRUE
              AND d.product_name IS NOT DISTINCT FROM s.product_name
              AND d.product_category IS NOT DISTINCT FROM s.product_category
              AND d.product_type IS NOT DISTINCT FROM s.product_type
              AND d.unit_of_measure IS NOT DISTINCT FROM s.unit_of_measure
              AND d.standard_cost IS NOT DISTINCT FROM s.standard_cost
              AND d.product_status IS NOT DISTINCT FROM s.product_status
        );
    """)

    print("dim_product loaded with SCD Type 2.")

    cursor.execute("""
        INSERT INTO dim_plant (
            plant_id, plant_name, city, district, region, plant_manager,
            plant_status, effective_start_date, effective_end_date, is_current
        )
        SELECT
            s.plant_id, s.plant_name, s.city, s.district, s.region, s.plant_manager,
            s.plant_status, CURRENT_DATE, DATE '9999-12-31', TRUE
        FROM stg_plants s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_plant d
            WHERE d.plant_id = s.plant_id
              AND d.is_current = TRUE
        );
    """)

    print("dim_plant loaded.")

    cursor.execute("""
        INSERT INTO dim_machine (
            machine_id, machine_name, machine_type, machine_model,
            production_line, plant_id, machine_status,
            effective_start_date, effective_end_date, is_current
        )
        SELECT
            s.machine_id, s.machine_name, s.machine_type, s.machine_model,
            s.production_line, s.plant_id, s.machine_status,
            CURRENT_DATE, DATE '9999-12-31', TRUE
        FROM stg_machines s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_machine d
            WHERE d.machine_id = s.machine_id
              AND d.is_current = TRUE
        );
    """)

    print("dim_machine loaded.")

    cursor.execute("""
        INSERT INTO dim_employee (
            employee_id, employee_name, department, job_role,
            employment_type, employee_status,
            effective_start_date, effective_end_date, is_current
        )
        SELECT
            s.employee_id, s.employee_name, s.department, s.job_role,
            s.employment_type, s.employee_status,
            CURRENT_DATE, DATE '9999-12-31', TRUE
        FROM stg_employees s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_employee d
            WHERE d.employee_id = s.employee_id
              AND d.is_current = TRUE
        );
    """)

    print("dim_employee loaded.")

    cursor.execute("""
        INSERT INTO dim_shift (
            shift_id, shift_name, start_time, end_time, shift_type
        )
        SELECT
            s.shift_id, s.shift_name, s.start_time, s.end_time, s.shift_type
        FROM stg_shifts s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_shift d
            WHERE d.shift_id = s.shift_id
        );
    """)

    print("dim_shift loaded.")
    conn.commit()
    print("\nDimension loading completed successfully.")

except Exception as e:
    conn.rollback()
    print("\nDimension loading failed:")
    print(e)
    raise

finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
