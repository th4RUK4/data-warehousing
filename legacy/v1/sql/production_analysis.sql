-- ==========================================
-- PRODUCTION ANALYSIS
-- ==========================================


-- 1. Daily production
SELECT
    production_date,
    SUM(produced_quantity) AS produced_quantity,
    SUM(good_quantity) AS good_quantity,
    SUM(defective_quantity) AS defective_quantity
FROM vw_production_dashboard
GROUP BY production_date
ORDER BY production_date;


-- 2. Production by plant
SELECT
    plant_name,
    SUM(produced_quantity) AS total_production,
    SUM(good_quantity) AS total_good,
    SUM(defective_quantity) AS total_defective
FROM vw_production_dashboard
GROUP BY plant_name
ORDER BY total_production DESC;


-- 3. Production by product
SELECT
    product_name,
    SUM(produced_quantity) AS total_production,
    SUM(good_quantity) AS total_good,
    SUM(defective_quantity) AS total_defective
FROM vw_production_dashboard
GROUP BY product_name
ORDER BY total_production DESC;


-- 4. Production by machine
SELECT
    machine_name,
    SUM(produced_quantity) AS total_production,
    SUM(good_quantity) AS total_good,
    SUM(defective_quantity) AS total_defective
FROM vw_production_dashboard
GROUP BY machine_name
ORDER BY total_production DESC;


-- 5. Production by date and plant
SELECT
    production_date,
    plant_name,
    SUM(produced_quantity) AS total_production
FROM vw_production_dashboard
GROUP BY production_date, plant_name
ORDER BY production_date, total_production DESC;
