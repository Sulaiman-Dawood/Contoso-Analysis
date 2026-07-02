with grand_total as (
    Select
        Brand,
        s.Quantity,
        sum(s.Quantity) over() as grand_total
    from Sales s
    left join Product p
        on s.ProductKey = p.ProductKey
    where s.[Order Date] >= '2025-01-01'
)

select top 5
    Brand,
    sum(Quantity) as total_orders,
    (sum(Quantity) * 1.0) * 100 / max(grand_total) as percentage_of_total
from grand_total
GROUP BY Brand
order by total_orders desc