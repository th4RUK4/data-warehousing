# Source Data Contract

The active ETL expects six CSV files in each source snapshot directory.

| Entity | File | Business key |
|---|---|---|
| Product | `products.csv` | `product_id` |
| Factory | `factories.csv` | `factory_id` |
| Machine | `machines.csv` | `machine_id` |
| Employee | `employees.csv` | `employee_id` |
| Shift | `shifts.csv` | `shift_id` |
| Production | `production_orders.csv` | `production_id` |

Validation enforces required columns, non-empty datasets, non-null and unique business keys, numeric constraints, business-date rules and source referential integrity.

The small `run_1` and `run_2` datasets are deterministic correctness fixtures, not performance benchmarks.
