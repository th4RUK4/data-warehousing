-- ==========================================
-- COST ANALYSIS
-- ==========================================


-- 1. Total costs
SELECT
    SUM(material_cost) AS total_material_cost,
    SUM(production_cost) AS total_production_cost
FROM vw_production_dashboard;


-- 2. Cost by product
SELECT
    product_name,
    SUM(material_cost) AS material_cost,
    SUM(production_cost) AS production_cost,

    ROUND(
        SUM(production_cost)::numeric
        / NULLIF(SUM(produced_quantity), 0),
        2
    ) AS cost_per_unit

FROM vw_production_dashboard

GROUP BY product_name

ORDER BY production_cost DESC;


-- 3. Cost by plant
SELECT
    plant_name,
    SUM(material_cost) AS material_cost,
    SUM(production_cost) AS production_cost,

    ROUND(
        SUM(production_cost)::numeric
        / NULLIF(SUM(produced_quantity), 0),
        2
    ) AS cost_per_unit

FROM vw_production_dashboard

GROUP BY plant_name

ORDER BY production_cost DESC;


-- 4. Daily production cost
SELECT
    production_date,
    SUM(material_cost) AS material_cost,
    SUM(production_cost) AS production_cost
FROM vw_production_dashboard
GROUP BY production_date
ORDER BY production_date;
