-- =====================================================
-- 06. SALES BY CATEGORY
-- Description: Product category performance
-- =====================================================

SELECT
    COALESCE(p.product_category_name, 'uncategorized') AS category,
    COUNT(*) AS items_sold,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price)::numeric, 2) AS total_sales,
    ROUND(AVG(oi.price)::numeric, 2) AS average_item_price

FROM orders o

INNER JOIN order_items oi
    ON o.order_id = oi.order_id

INNER JOIN products p
    ON oi.product_id = p.product_id

WHERE o.order_status = 'delivered'

GROUP BY
    COALESCE(p.product_category_name, 'uncategorized')

ORDER BY total_sales DESC;