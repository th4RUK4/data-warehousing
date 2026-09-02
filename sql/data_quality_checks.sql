-- ==========================================
-- DATA QUALITY CHECKS
-- ==========================================


-- 1. Total records
SELECT COUNT(*) AS total_records
FROM vw_production_dashboard;


-- 2. Duplicate production IDs
SELECT
    production_id,
    COUNT(*) AS duplicate_count
FROM vw_production_dashboard
GROUP BY production_id
HAVING COUNT(*) > 1;


-- 3. Produced quantity validation
SELECT
    production_id,
    produced_quantity,
    good_quantity,
    defective_quantity
FROM vw_production_dashboard
WHERE good_quantity + defective_quantity
      <> produced_quantity;


-- 4. Negative quantities
SELECT *
FROM vw_production_dashboard
WHERE produced_quantity < 0
   OR good_quantity < 0
   OR defective_quantity < 0;


-- 5. Invalid defect quantity
SELECT *
FROM vw_production_dashboard
WHERE defective_quantity > produced_quantity;


-- 6. Negative costs
SELECT *
FROM vw_production_dashboard
WHERE material_cost < 0
   OR production_cost < 0;


-- 7. NULL critical values
SELECT
    COUNT(*) FILTER (WHERE production_id IS NULL) AS missing_production_id,
    COUNT(*) FILTER (WHERE production_date IS NULL) AS missing_date,
    COUNT(*) FILTER (WHERE product_name IS NULL) AS missing_product,
    COUNT(*) FILTER (WHERE plant_name IS NULL) AS missing_plant,
    COUNT(*) FILTER (WHERE machine_name IS NULL) AS missing_machine
FROM vw_production_dashboard;
