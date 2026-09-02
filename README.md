# Manufacturing Data Warehouse & Production Dashboard

## 1. Project Overview

This project implements a Manufacturing Data Warehouse using PostgreSQL and provides an interactive production analytics dashboard using Streamlit and Plotly.

The system integrates manufacturing data from multiple CSV files into a dimensional data warehouse and provides analytical insights into production, quality, machine performance, and production costs.

---

## 2. Technologies Used

- Python
- PostgreSQL
- Pandas
- Psycopg2
- Streamlit
- Plotly
- SQL
- Git / GitHub

---

## 3. Data Warehouse Architecture

The ETL pipeline follows this architecture:

CSV Files
    ↓
Staging Tables
    ↓
Dimension Tables
    ↓
Fact Table
    ↓
Analytics View
    ↓
Streamlit Dashboard

### Dimension Tables

- dim_date
- dim_product
- dim_plant
- dim_machine
- dim_employee
- dim_shift

### Fact Table

- fact_production

### Analytics View

- vw_production_dashboard

---

## 4. ETL Pipeline

The ETL pipeline consists of:

### Extract and Load Staging

```bash
python etl/load_staging.py
