-- =====================================================
-- 09. TOP SELLERS ANALYSIS
-- Description: Top 10 sellers by product revenue
-- =====================================================

SELECT
    oi.seller_id,
    COUNT(*) AS items_sold,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price)::numeric, 2) AS total_sales,
    ROUND(AVG(oi.price)::numeric, 2) AS average_item_price

FROM orders o

INNER JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY oi.seller_id

ORDER BY total_sales DESC

LIMIT 10;