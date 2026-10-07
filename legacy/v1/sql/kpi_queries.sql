-- ==========================================
-- MANUFACTURING KPI ANALYSIS
-- ==========================================

-- 1. Overall KPIs
SELECT
    COUNT(*) AS total_production_records,
    SUM(produced_quantity) AS total_production,
    SUM(good_quantity) AS total_good_quantity,
    SUM(defective_quantity) AS total_defective_quantity,

    ROUND(
        SUM(good_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS quality_rate,

    ROUND(
        SUM(defective_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS defect_rate,

    SUM(material_cost) AS total_material_cost,
    SUM(production_cost) AS total_production_cost,
    SUM(production_hours) AS total_production_hours,
    SUM(downtime_hours) AS total_downtime_hours

FROM vw_production_dashboard;


-- 2. Average production per record
SELECT
    ROUND(AVG(produced_quantity), 2) AS avg_production,
    ROUND(AVG(good_quantity), 2) AS avg_good_quantity,
    ROUND(AVG(defective_quantity), 2) AS avg_defective_quantity,
    ROUND(AVG(production_cost), 2) AS avg_production_cost
FROM vw_production_dashboard;


-- 3. Cost per produced unit
SELECT
    ROUND(
        SUM(production_cost)::numeric
        / NULLIF(SUM(produced_quantity), 0),
        2
    ) AS cost_per_produced_unit
FROM vw_production_dashboard;
