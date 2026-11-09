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

-- =====================================================
-- 10. PRIMARY KEYS AND UNIQUE CONSTRAINTS
-- Description: Inspect primary keys and unique constraints
-- =====================================================

SELECT
    tc.table_name,
    tc.constraint_type,
    kcu.column_name,
    kcu.ordinal_position
FROM information_schema.table_constraints tc
LEFT JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
WHERE
    tc.table_schema = 'public'
    AND tc.table_name IN ('orders', 'order_items', 'products')
    AND tc.constraint_type IN ('PRIMARY KEY', 'UNIQUE')
ORDER BY
    tc.table_name,
    tc.constraint_type,
    kcu.ordinal_position;