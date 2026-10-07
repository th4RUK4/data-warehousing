import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ETL_DIR = BASE_DIR / "etl"

scripts = [
    "load_staging.py",
    "load_dimensions.py",
    "load_fact.py",
]

print("=" * 60)
print("MANUFACTURING DATA WAREHOUSE - ETL PIPELINE")
print("=" * 60)

for script in scripts:
    script_path = ETL_DIR / script

    print(f"\nRunning: {script}")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        check=False,
    )

    if result.returncode != 0:
        print(f"\nETL FAILED: {script}")
        sys.exit(result.returncode)

    print(f"Completed: {script}")

print("\n" + "=" * 60)
print("ETL PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)
