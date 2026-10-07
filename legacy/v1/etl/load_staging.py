import pandas as pd
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path.home() / "manufacturing_dw"
DATA_DIR = BASE_DIR / "data"


# --------------------------------------------------
# 2. PostgreSQL connection
# --------------------------------------------------

load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# --------------------------------------------------
# 3. CSV → Staging mapping
# --------------------------------------------------

TABLE_MAPPING = {
    "products.csv": "stg_products",
    "plants.csv": "stg_plants",
    "machines.csv": "stg_machines",
    "employees.csv": "stg_employees",
    "shifts.csv": "stg_shifts",
    "production.csv": "stg_production"
}


# --------------------------------------------------
# 4. Connect to PostgreSQL
# --------------------------------------------------

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print("Connected to PostgreSQL successfully.")

except Exception as e:
    print("Database connection failed:")
    print(e)
    exit()


# --------------------------------------------------
# 5. Load each CSV into staging
# --------------------------------------------------

for csv_file, staging_table in TABLE_MAPPING.items():

    file_path = DATA_DIR / csv_file

    print(f"\nProcessing: {csv_file}")

    try:
        # Extract
        df = pd.read_csv(file_path)

        print(f"Rows extracted: {len(df)}")

        # Clear previous staging data
        cursor.execute(f"TRUNCATE TABLE {staging_table}")

        # Load rows
        columns = list(df.columns)

        column_names = ", ".join(columns)

        placeholders = ", ".join(["%s"] * len(columns))

        insert_query = f"""
            INSERT INTO {staging_table}
            ({column_names})
            VALUES ({placeholders})
        """

        for row in df.itertuples(index=False, name=None):
            cursor.execute(insert_query, row)

        print(f"Loaded into: {staging_table}")

    except Exception as e:
        print(f"Error processing {csv_file}:")
        print(e)

        conn.rollback()
        continue


# --------------------------------------------------
# 6. Commit transaction
# --------------------------------------------------

conn.commit()


# --------------------------------------------------
# 7. Close connection
# --------------------------------------------------

cursor.close()
conn.close()

print("\nETL staging load completed successfully.")
