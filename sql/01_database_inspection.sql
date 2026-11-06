-- =====================================================
-- 01. DATABASE INSPECTION
-- Description: Inspect available tables and columns
-- =====================================================

-- 1. List database tables
SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;


-- 2. Inspect columns and data types
SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('orders', 'order_items', 'products')
ORDER BY table_name, ordinal_position;
