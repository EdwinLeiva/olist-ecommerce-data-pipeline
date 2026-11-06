-- =====================================================
-- 05. PRODUCT PRICE OUTLIERS
-- Description: Identify statistical price outliers using IQR
-- =====================================================

WITH price_statistics AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS q3
    FROM order_items
),

price_limits AS (
    SELECT
        q1,
        q3,
        q3 - q1 AS iqr,
        q3 + 1.5 * (q3 - q1) AS upper_limit
    FROM price_statistics
)

SELECT
    COUNT(*) FILTER (
        WHERE oi.price > pl.upper_limit
    ) AS outlier_items,

    COUNT(*) AS total_items,

    ROUND(
        (
            100.0 * COUNT(*) FILTER (
                WHERE oi.price > pl.upper_limit
            ) / COUNT(*)
        )::numeric,
        2
    ) AS outlier_percentage,

    ROUND(
        (
            SUM(oi.price) FILTER (
                WHERE oi.price > pl.upper_limit
            )
        )::numeric,
        2
    ) AS outlier_sales,

    ROUND(SUM(oi.price)::numeric, 2) AS total_sales,

    ROUND(
        (
            100.0 * SUM(oi.price) FILTER (
                WHERE oi.price > pl.upper_limit
            ) / NULLIF(SUM(oi.price), 0)
        )::numeric,
        2
    ) AS outlier_sales_percentage,

    ROUND(pl.upper_limit::numeric, 2) AS upper_outlier_limit

FROM order_items oi
CROSS JOIN price_limits pl
GROUP BY pl.upper_limit;