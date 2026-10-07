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
        INSERT INTO fact_production (
            production_id, date_sk, product_sk, machine_sk, plant_sk,
            employee_sk, shift_sk, produced_quantity, good_quantity,
            defective_quantity, production_hours, downtime_hours,
            material_cost, production_cost
        )
        SELECT
            s.production_id,
            d.date_sk,
            pr.product_sk,
            m.machine_sk,
            pl.plant_sk,
            e.employee_sk,
            sh.shift_sk,
            s.produced_quantity,
            s.good_quantity,
            s.defective_quantity,
            s.production_hours,
            s.downtime_hours,
            s.material_cost,
            s.production_cost
        FROM stg_production s
        JOIN dim_date d
            ON d.full_date = s.production_date
        JOIN dim_product pr
            ON pr.product_id = s.product_id
           AND pr.effective_start_date <= s.production_date
           AND s.production_date < pr.effective_end_date
        JOIN dim_machine m
            ON m.machine_id = s.machine_id
           AND m.is_current = TRUE
        JOIN dim_plant pl
            ON pl.plant_id = s.plant_id
           AND pl.is_current = TRUE
        JOIN dim_employee e
            ON e.employee_id = s.employee_id
           AND e.is_current = TRUE
        JOIN dim_shift sh
            ON sh.shift_id = s.shift_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM fact_production f
            WHERE f.production_id = s.production_id
        );
    """)

    rows_inserted = cursor.rowcount
    conn.commit()
    print(f"Fact records inserted: {rows_inserted}")
    print("\nFact table loading completed successfully.")

except Exception as e:
    conn.rollback()
    print("\nFact table loading failed:")
    print(e)
    raise

finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
