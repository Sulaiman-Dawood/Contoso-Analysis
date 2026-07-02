SELECT st.Name,
    st.Country,
    sum(Quantity * [Net Price] * [Exchange Rate]) as net_revenue
from Sales sa
LEFT JOIN Customer c ON
sa.CustomerKey = c.CustomerKey
LEFT JOIN Store st ON
st.StoreKey = sa.StoreKey
where [Order Date] >= '2025-01-01' AND st.StoreKey != 999999
GROUP BY st.Name, st.Country
ORDER BY net_revenue DESC
