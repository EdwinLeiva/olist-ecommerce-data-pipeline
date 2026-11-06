-- =====================================================
-- 04. PRODUCT PRICE DISTRIBUTION
-- Description: Statistical analysis of product prices
-- =====================================================
SELECT
    COUNT(*) AS total_items,
    ROUND(AVG(price)::numeric, 2) AS average_price,
    ROUND(
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price)::numeric,
        2
    ) AS median_price,
    ROUND(MIN(price)::numeric, 2) AS minimum_price,
    ROUND(MAX(price)::numeric, 2) AS maximum_price,
    ROUND(
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price)::numeric,
        2
    ) AS percentile_25,
    ROUND(
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price)::numeric,
        2
    ) AS percentile_75
FROM order_items;