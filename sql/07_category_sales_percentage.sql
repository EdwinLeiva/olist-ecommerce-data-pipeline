-- =====================================================
-- 07. CATEGORY SALES PERCENTAGE
-- Description: Calculate each category's contribution
-- to total delivered product sales
-- =====================================================

WITH category_sales AS (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS total_sales
    FROM order_items oi
    INNER JOIN orders o
        ON oi.order_id = o.order_id
    INNER JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.product_category_name
)

SELECT
    product_category_name,
    ROUND(total_sales::numeric, 2) AS total_sales,

    ROUND(
        (
            100.0 * total_sales /
            NULLIF(SUM(total_sales) OVER (), 0)
        )::numeric,
        2
    ) AS sales_percentage

FROM category_sales
ORDER BY total_sales DESC;