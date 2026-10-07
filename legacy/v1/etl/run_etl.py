
import subprocess
import sys
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path.home() / "manufacturing_dw"
ETL_DIR = BASE_DIR / "etl"


# --------------------------------------------------
# ETL scripts
# --------------------------------------------------

scripts = [
    "load_staging.py",
    "load_dimensions.py",
    "load_fact.py"
]


# --------------------------------------------------
# Run ETL pipeline
# --------------------------------------------------

print("=" * 60)
print("MANUFACTURING DATA WAREHOUSE - ETL PIPELINE")
print("=" * 60)

for script in scripts:

    script_path = ETL_DIR / script

    print(f"\nRunning: {script}")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False
    )

    if result.returncode != 0:
        print(f"\nETL FAILED: {script}")
        sys.exit(1)

    print(f"Completed: {script}")


# --------------------------------------------------
# Pipeline completed
# --------------------------------------------------

print("\n" + "=" * 60)
print("ETL PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)
