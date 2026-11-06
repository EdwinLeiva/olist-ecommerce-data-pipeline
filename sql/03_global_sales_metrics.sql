-- =====================================================
-- 03. GLOBAL SALES METRICS
-- Description: Overall performance of delivered orders
-- =====================================================

SELECT
    COUNT(DISTINCT o.order_id) AS total_delivered_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(oi.price)::numeric, 2) AS total_product_sales,
    ROUND(
        (SUM(oi.price) / NULLIF(COUNT(DISTINCT o.order_id), 0))::numeric,
        2
    ) AS average_order_value,
    ROUND(AVG(oi.price)::numeric, 2) AS average_item_price
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';