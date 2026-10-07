import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

# --------------------------------------------------
# 2. PostgreSQL connection
# --------------------------------------------------

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

TABLE_MAPPING = {
    "products.csv": "stg_products",
    "plants.csv": "stg_plants",
    "machines.csv": "stg_machines",
    "employees.csv": "stg_employees",
    "shifts.csv": "stg_shifts",
    "production.csv": "stg_production",
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Connected to PostgreSQL successfully.")
except Exception as e:
    print("Database connection failed:")
    print(e)
    raise SystemExit(1)

failed_files = []

for csv_file, staging_table in TABLE_MAPPING.items():
    file_path = DATA_DIR / csv_file
    print(f"\nProcessing: {csv_file}")

    try:
        df = pd.read_csv(file_path)
        print(f"Rows extracted: {len(df)}")

        cursor.execute(f"TRUNCATE TABLE {staging_table}")

        columns = list(df.columns)
        column_names = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        insert_query = f"""
            INSERT INTO {staging_table} ({column_names})
            VALUES ({placeholders})
        """

        for row in df.itertuples(index=False, name=None):
            cursor.execute(insert_query, row)

        print(f"Loaded into: {staging_table}")

    except Exception as e:
        print(f"Error processing {csv_file}:")
        print(e)
        conn.rollback()
        failed_files.append(csv_file)

if failed_files:
    conn.rollback()
    cursor.close()
    conn.close()
    raise RuntimeError(f"Staging load failed for: {', '.join(failed_files)}")

conn.commit()
cursor.close()
conn.close()

print("\nETL staging load completed successfully.")
