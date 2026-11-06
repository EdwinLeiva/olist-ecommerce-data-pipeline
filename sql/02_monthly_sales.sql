-- =====================================================
-- 02. MONTHLY SALES ANALYSIS
-- Description: Monthly sales from delivered orders
-- =====================================================

SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp)::date AS sales_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(oi.price)::numeric, 2) AS product_sales,
    ROUND(SUM(oi.freight_value)::numeric, 2) AS freight_revenue,
    ROUND(
        (SUM(oi.price) / NULLIF(COUNT(DISTINCT o.order_id), 0))::numeric,
        2
    ) AS average_order_value
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
ORDER BY sales_month;