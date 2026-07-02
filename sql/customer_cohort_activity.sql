with last_five_years as (
    select distinct
        year([Order Date]) as order_year,
        CustomerKey
    from sales
    where [Order Date] >= dateadd(year, -5, getdate())
),

first_order_dates as (
    select
        CustomerKey,
        min(order_year) over (partition by CustomerKey) as cohort_year,
        order_year as purchase_year
    from last_five_years lf
)

select 
    cohort_year,
    purchase_year,
    count(distinct CustomerKey) as number_of_customers
from first_order_dates
group by cohort_year, purchase_year
order by cohort_year, purchase_year