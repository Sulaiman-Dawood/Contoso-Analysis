with age_groups as (
    select distinct
        s.CustomerKey,
        case
            when c.Age between 18 and 30 then '18-30'
            when c.Age between 31 and 45 then '31-45'
            when c.Age between 46 and 60 then '46-60'
            when c.Age > 60 then 'Over 60'
            else 'Unspecified'
        end as Age_Group
    from Sales s
    left join Customer c
        on s.CustomerKey = c.CustomerKey
    where [Order Date] >= '2025-01-01'
),
grand_total as (
    select count(*) as grand_total
    from age_groups
)
select
    a.Age_Group,
    count(*) as Customer_Count,
    count(*) * 100.0 / gt.grand_total as Percentage_of_Customers
from age_groups a
cross join grand_total gt
group by a.Age_Group, gt.grand_total;