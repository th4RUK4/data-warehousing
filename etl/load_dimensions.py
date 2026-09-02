import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

# --------------------------------------------------
# 1. PostgreSQL connection
# --------------------------------------------------

BASE_DIR = Path.home() / "manufacturing_dw"

load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# --------------------------------------------------
# 2. Connect to PostgreSQL
# --------------------------------------------------

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print("Connected to PostgreSQL successfully.")

except Exception as e:
    print("Database connection failed:")
    print(e)
    exit(1)


try:

    # --------------------------------------------------
    # 3. Load Product Dimension - SCD Type 2
    # --------------------------------------------------

    # Step 1: Close current record when attributes change
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

    # Step 2: Insert new version for new or changed products
    cursor.execute("""
        INSERT INTO dim_product (
            product_id,
            product_name,
            product_category,
            product_type,
            unit_of_measure,
            standard_cost,
            product_status,
            effective_start_date,
            effective_end_date,
            is_current
        )
        SELECT
            s.product_id,
            s.product_name,
            s.product_category,
            s.product_type,
            s.unit_of_measure,
            s.standard_cost,
            s.product_status,
            CURRENT_DATE,
            DATE '9999-12-31',
            TRUE
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


    # --------------------------------------------------
    # 4. Load Plant Dimension
    # --------------------------------------------------

    cursor.execute("""
        INSERT INTO dim_plant (
            plant_id,
            plant_name,
            city,
            district,
            region,
            plant_manager,
            plant_status,
            effective_start_date,
            effective_end_date,
            is_current
        )
        SELECT
            s.plant_id,
            s.plant_name,
            s.city,
            s.district,
            s.region,
            s.plant_manager,
            s.plant_status,
            CURRENT_DATE,
            DATE '9999-12-31',
            TRUE
        FROM stg_plants s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_plant d
            WHERE d.plant_id = s.plant_id
              AND d.is_current = TRUE
        );
    """)

    print("dim_plant loaded.")


    # --------------------------------------------------
    # 5. Load Machine Dimension
    # --------------------------------------------------

    cursor.execute("""
        INSERT INTO dim_machine (
            machine_id,
            machine_name,
            machine_type,
            machine_model,
            production_line,
            plant_id,
            machine_status,
            effective_start_date,
            effective_end_date,
            is_current
        )
        SELECT
            s.machine_id,
            s.machine_name,
            s.machine_type,
            s.machine_model,
            s.production_line,
            s.plant_id,
            s.machine_status,
            CURRENT_DATE,
            DATE '9999-12-31',
            TRUE
        FROM stg_machines s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_machine d
            WHERE d.machine_id = s.machine_id
              AND d.is_current = TRUE
        );
    """)

    print("dim_machine loaded.")


    # --------------------------------------------------
    # 6. Load Employee Dimension
    # --------------------------------------------------

    cursor.execute("""
        INSERT INTO dim_employee (
            employee_id,
            employee_name,
            department,
            job_role,
            employment_type,
            employee_status,
            effective_start_date,
            effective_end_date,
            is_current
        )
        SELECT
            s.employee_id,
            s.employee_name,
            s.department,
            s.job_role,
            s.employment_type,
            s.employee_status,
            CURRENT_DATE,
            DATE '9999-12-31',
            TRUE
        FROM stg_employees s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_employee d
            WHERE d.employee_id = s.employee_id
              AND d.is_current = TRUE
        );
    """)

    print("dim_employee loaded.")


    # --------------------------------------------------
    # 7. Load Shift Dimension
    # --------------------------------------------------

    cursor.execute("""
        INSERT INTO dim_shift (
            shift_id,
            shift_name,
            start_time,
            end_time,
            shift_type
        )
        SELECT
            s.shift_id,
            s.shift_name,
            s.start_time,
            s.end_time,
            s.shift_type
        FROM stg_shifts s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dim_shift d
            WHERE d.shift_id = s.shift_id
        );
    """)

    print("dim_shift loaded.")


    # --------------------------------------------------
    # 8. Commit
    # --------------------------------------------------

    conn.commit()

    print("\nDimension loading completed successfully.")


except Exception as e:

    conn.rollback()

    print("\nDimension loading failed:")
    print(e)


finally:

    cursor.close()
    conn.close()

    print("Database connection closed.")