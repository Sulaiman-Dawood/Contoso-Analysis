SELECT
    month([Order Date]) AS order_month,
    COUNT(DISTINCT s.CustomerKey) AS total_customers,
    SUM(s.Quantity * s.[Net Price] * s.[Exchange Rate]) AS total_revenue,
    count(distinct [Order Number]) as total_orders
FROM Sales s
LEFT JOIN Customer c
    ON s.CustomerKey = c.CustomerKey
WHERE s.[Order Date] >= '2025-01-01'
GROUP BY month([Order Date])
ORDER BY order_month;
