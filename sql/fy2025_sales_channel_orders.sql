SELECT case when StoreKey = 999999 then 'Online' else 'In-Store' end as channel,
    SUM(s.Quantity * s.[Net Price] * s.[Exchange Rate]) AS total_revenue,
    count(distinct [Order Number]) as total_orders
from Sales s
LEFT JOIN Customer c ON
s.CustomerKey = c.CustomerKey
where [Order Date] >= '2025-01-01'
group by case when StoreKey = 999999 then 'Online' else 'In-Store' end
order by channel;