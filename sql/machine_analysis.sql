-- ==========================================
-- MACHINE PERFORMANCE ANALYSIS
-- ==========================================


SELECT
    machine_name,

    SUM(produced_quantity) AS produced_quantity,

    SUM(good_quantity) AS good_quantity,

    SUM(defective_quantity) AS defective_quantity,

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

    SUM(production_hours) AS production_hours,

    SUM(downtime_hours) AS downtime_hours,

    SUM(production_cost) AS production_cost

FROM vw_production_dashboard

GROUP BY machine_name

ORDER BY produced_quantity DESC;
