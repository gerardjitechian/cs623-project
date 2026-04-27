-- CS623 Project
-- 04_verify_setup.sql
-- Basic sanity checks after the schema, data, and constraints are loaded.

-- Check row counts.
SELECT 'product_count' AS check_name, COUNT(*) AS actual_count, 3 AS expected_count
FROM product;

SELECT 'depot_count' AS check_name, COUNT(*) AS actual_count, 3 AS expected_count
FROM depot;

SELECT 'stock_count' AS check_name, COUNT(*) AS actual_count, 8 AS expected_count
FROM stock;

-- Show the full starting data with readable product/depot details.
SELECT
    s.prodid,
    p.pname,
    s.depid,
    d.addr AS depot_address,
    s.quantity
FROM stock AS s
JOIN product AS p
    ON s.prodid = p.prodid
JOIN depot AS d
    ON s.depid = d.depid
ORDER BY s.prodid, s.depid;

-- This should return 0 if every Stock row has a valid Product and Depot.
SELECT
    'orphan_stock_rows' AS check_name,
    COUNT(*) AS issue_count
FROM stock AS s
LEFT JOIN product AS p
    ON s.prodid = p.prodid
LEFT JOIN depot AS d
    ON s.depid = d.depid
WHERE p.prodid IS NULL
   OR d.depid IS NULL;

-- Show the constraints that were added for these tables.
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type
FROM information_schema.table_constraints AS tc
WHERE tc.table_schema = 'public'
  AND tc.table_name IN ('product', 'depot', 'stock')
ORDER BY tc.table_name, tc.constraint_type, tc.constraint_name;
