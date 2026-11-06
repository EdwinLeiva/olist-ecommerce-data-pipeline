-- =====================================================
-- 08. CATEGORY PARETO ANALYSIS
-- Description: Cumulative revenue contribution by category
-- =====================================================

WITH category_sales AS (
    SELECT
        COALESCE(p.product_category_name, 'uncategorized') AS category,
        SUM(oi.price) AS total_sales
    FROM orders o
    INNER JOIN order_items oi
        ON o.order_id = oi.order_id
    INNER JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.order_status = 'delivered'
    GROUP BY
        COALESCE(p.product_category_name, 'uncategorized')
),

category_percentages AS (
    SELECT
        category,
        total_sales,
        100.0 * total_sales / SUM(total_sales) OVER () AS sales_percentage
    FROM category_sales
)

SELECT
    category,
    ROUND(total_sales::numeric, 2) AS total_sales,
    ROUND(sales_percentage::numeric, 2) AS sales_percentage,
    ROUND(
        SUM(sales_percentage) OVER (
            ORDER BY total_sales DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        )::numeric,
        2
    ) AS cumulative_percentage
FROM category_percentages
ORDER BY total_sales DESC;