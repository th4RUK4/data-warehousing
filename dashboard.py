import os
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from dotenv import load_dotenv


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Manufacturing Analytics",
    page_icon="🏭",
    layout="wide"
)


# ==================================================
# DATABASE
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@st.cache_data
def load_data():
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "manufacturing_dw"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD"),
    }

    if not db_config["password"]:
        raise RuntimeError(
            "DB_PASSWORD is not configured. Create a .env file from .env.example."
        )

    conn = psycopg2.connect(**db_config)

    try:
        query = """
            SELECT *
            FROM vw_production_dashboard
            ORDER BY production_date;
        """
        df = pd.read_sql(query, conn)
    finally:
        conn.close()

    df["production_date"] = pd.to_datetime(df["production_date"])

    return df


# ==================================================
# LOAD DATA
# ==================================================

try:
    df = load_data()
except Exception as e:
    st.error("Unable to connect to PostgreSQL")
    st.code(str(e))
    st.stop()


# ==================================================
# HEADER
# ==================================================

st.title("🏭 Manufacturing Analytics Dashboard")
st.caption("Production • Quality • Machine Performance • Cost Analysis")
st.divider()


# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("🔎 Dashboard Filters")

plant_options = ["All"] + sorted(df["plant_name"].dropna().unique().tolist())
selected_plant = st.sidebar.selectbox("🏭 Plant", plant_options)

product_options = ["All"] + sorted(df["product_name"].dropna().unique().tolist())
selected_product = st.sidebar.selectbox("📦 Product", product_options)

min_date = df["production_date"].min().date()
max_date = df["production_date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Production Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ==================================================
# APPLY FILTERS
# ==================================================

filtered_df = df.copy()

if selected_plant != "All":
    filtered_df = filtered_df[filtered_df["plant_name"] == selected_plant]

if selected_product != "All":
    filtered_df = filtered_df[filtered_df["product_name"] == selected_product]

if len(selected_dates) == 2:
    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])
    filtered_df = filtered_df[
        (filtered_df["production_date"] >= start_date)
        & (filtered_df["production_date"] <= end_date)
    ]


# ==================================================
# KPI CALCULATIONS
# ==================================================

total_production = filtered_df["produced_quantity"].sum()
total_good = filtered_df["good_quantity"].sum()
total_defective = filtered_df["defective_quantity"].sum()
total_cost = filtered_df["production_cost"].sum()
total_downtime = filtered_df["downtime_hours"].sum()

quality_rate = total_good / total_production * 100 if total_production > 0 else 0
defect_rate = total_defective / total_production * 100 if total_production > 0 else 0


# ==================================================
# KPI CARDS
# ==================================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Production", f"{total_production:,}")
col2.metric("Good Quantity", f"{total_good:,}")
col3.metric("Defective Quantity", f"{total_defective:,}")
col4.metric("Quality Rate", f"{quality_rate:.2f}%")
col5.metric("Production Cost", f"Rs. {total_cost:,.0f}")
col6.metric("Downtime", f"{total_downtime:.2f} h")

st.divider()


# ==================================================
# PRODUCTION TREND
# ==================================================

st.subheader("📈 Production Trend")

daily = (
    filtered_df.groupby("production_date", as_index=False)
    .agg(
        produced_quantity=("produced_quantity", "sum"),
        good_quantity=("good_quantity", "sum"),
        defective_quantity=("defective_quantity", "sum")
    )
)

fig_trend = px.line(
    daily,
    x="production_date",
    y=["produced_quantity", "good_quantity", "defective_quantity"],
    markers=True,
    title="Daily Production Performance"
)

fig_trend.update_layout(
    xaxis_title="Date",
    yaxis_title="Quantity",
    legend_title="Metric",
    hovermode="x unified"
)

st.plotly_chart(fig_trend, use_container_width=True)


# ==================================================
# PLANT + PRODUCT ANALYSIS
# ==================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏭 Production by Plant")

    plant_data = (
        filtered_df.groupby("plant_name", as_index=False)["produced_quantity"]
        .sum()
        .sort_values("produced_quantity", ascending=False)
    )

    fig_plant = px.bar(
        plant_data,
        x="plant_name",
        y="produced_quantity",
        text_auto=True,
        title="Production Quantity by Plant"
    )

    fig_plant.update_layout(xaxis_title="Plant", yaxis_title="Quantity")
    st.plotly_chart(fig_plant, use_container_width=True)

with col2:
    st.subheader("📦 Production by Product")

    product_data = (
        filtered_df.groupby("product_name", as_index=False)["produced_quantity"]
        .sum()
        .sort_values("produced_quantity", ascending=False)
    )

    fig_product = px.bar(
        product_data,
        x="product_name",
        y="produced_quantity",
        text_auto=True,
        title="Production Quantity by Product"
    )

    fig_product.update_layout(xaxis_title="Product", yaxis_title="Quantity")
    st.plotly_chart(fig_product, use_container_width=True)


# ==================================================
# MACHINE + QUALITY
# ==================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ Machine Performance")

    machine_data = (
        filtered_df.groupby("machine_name", as_index=False)
        .agg(
            produced_quantity=("produced_quantity", "sum"),
            defective_quantity=("defective_quantity", "sum")
        )
    )

    fig_machine = px.bar(
        machine_data,
        x="machine_name",
        y="produced_quantity",
        text_auto=True,
        title="Production by Machine"
    )

    fig_machine.update_layout(xaxis_title="Machine", yaxis_title="Production")
    st.plotly_chart(fig_machine, use_container_width=True)

with col2:
    st.subheader("🎯 Quality Analysis")

    quality_data = (
        filtered_df.groupby("product_name", as_index=False)
        .agg(
            produced=("produced_quantity", "sum"),
            defective=("defective_quantity", "sum")
        )
    )

    quality_data["defect_rate"] = (
        quality_data["defective"]
        / quality_data["produced"].replace(0, pd.NA)
        * 100
    )

    fig_quality = px.bar(
        quality_data,
        x="product_name",
        y="defect_rate",
        text_auto=".2f",
        title="Defect Rate by Product"
    )

    fig_quality.update_layout(
        xaxis_title="Product",
        yaxis_title="Defect Rate (%)"
    )

    st.plotly_chart(fig_quality, use_container_width=True)


# ==================================================
# COST ANALYSIS
# ==================================================

st.subheader("💰 Production Cost Analysis")

cost_data = (
    filtered_df.groupby("product_name", as_index=False)["production_cost"]
    .sum()
    .sort_values("production_cost", ascending=False)
)

fig_cost = px.pie(
    cost_data,
    names="product_name",
    values="production_cost",
    title="Production Cost Distribution"
)

st.plotly_chart(fig_cost, use_container_width=True)


# ==================================================
# OPERATIONAL SUMMARY
# ==================================================

st.subheader("⚙️ Operational Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Downtime", f"{total_downtime:.2f} hours")

with col2:
    st.metric("Defect Rate", f"{defect_rate:.2f}%")


# ==================================================
# DATA TABLE
# ==================================================

st.divider()
st.subheader("📋 Production Details")

display_columns = [
    "production_id",
    "production_date",
    "product_name",
    "plant_name",
    "machine_name",
    "produced_quantity",
    "good_quantity",
    "defective_quantity",
    "quality_rate",
    "defect_rate",
    "production_hours",
    "downtime_hours",
    "material_cost",
    "production_cost"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)


# ==================================================
# DOWNLOAD
# ==================================================

st.subheader("⬇️ Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv,
    file_name="manufacturing_production_report.csv",
    mime="text/csv"
)


# ==================================================
# FOOTER
# ==================================================

st.divider()
st.caption("Manufacturing Data Warehouse | PostgreSQL • Python • Pandas • Plotly • Streamlit")
