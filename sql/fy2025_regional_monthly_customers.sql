SELECT format([Order Date], 'MMM')  AS [month],
    count(distinct S.CustomerKey) AS total_customers,
    count(distinct Case when Continent = 'Europe' then S.CustomerKey end) AS european_customers,
    count(distinct Case when Continent = 'North America' then S.CustomerKey end) AS north_american_customers,
    count(distinct Case when Continent = 'Australia' then S.CustomerKey end) AS australian_customers
FROM Sales AS S
left join Customer AS C
on S.CustomerKey = C.CustomerKey
where [Order Date] >= '2025-01-01'
GROUP BY month([Order Date]), format([Order Date], 'MMM')
order by month([Order Date])
