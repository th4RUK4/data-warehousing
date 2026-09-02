-- ==========================================
-- QUALITY ANALYSIS
-- ==========================================


-- 1. Overall quality
SELECT
    ROUND(
        SUM(good_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS quality_rate,

    ROUND(
        SUM(defective_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS defect_rate
FROM vw_production_dashboard;


-- 2. Quality by product
SELECT
    product_name,
    SUM(produced_quantity) AS produced,
    SUM(good_quantity) AS good,
    SUM(defective_quantity) AS defective,

    ROUND(
        SUM(good_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS quality_rate,

    ROUND(
        SUM(defective_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS defect_rate

FROM vw_production_dashboard

GROUP BY product_name

ORDER BY defect_rate DESC;


-- 3. Quality by plant
SELECT
    plant_name,

    SUM(produced_quantity) AS produced,
    SUM(good_quantity) AS good,
    SUM(defective_quantity) AS defective,

    ROUND(
        SUM(good_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS quality_rate,

    ROUND(
        SUM(defective_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS defect_rate

FROM vw_production_dashboard

GROUP BY plant_name

ORDER BY defect_rate DESC;


-- 4. Quality by machine
SELECT
    machine_name,

    SUM(produced_quantity) AS produced,
    SUM(good_quantity) AS good,
    SUM(defective_quantity) AS defective,

    ROUND(
        SUM(good_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS quality_rate,

    ROUND(
        SUM(defective_quantity)::numeric
        / NULLIF(SUM(produced_quantity), 0) * 100,
        2
    ) AS defect_rate

FROM vw_production_dashboard

GROUP BY machine_name

ORDER BY defect_rate DESC;
