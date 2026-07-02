WITH yearly_customers AS (
    SELECT DISTINCT
        CustomerKey,
        YEAR([Order Date]) AS order_year
    FROM Sales
),
max_year AS (
    SELECT MAX(order_year) AS last_year
    FROM yearly_customers
),
customer_years AS (
    SELECT
        prev.order_year AS previous_year,
        prev.order_year + 1 AS current_year,
        prev.CustomerKey
    FROM yearly_customers prev
    CROSS JOIN max_year my
    WHERE prev.order_year < my.last_year
),
churned_customers AS (
    SELECT
        cy.previous_year,
        cy.current_year,
        cy.CustomerKey
    FROM customer_years cy
    LEFT JOIN yearly_customers curr
        ON cy.CustomerKey = curr.CustomerKey
        AND cy.current_year = curr.order_year
    WHERE curr.CustomerKey IS NULL
)
SELECT
    cy.current_year AS cohort_year,
    COUNT(DISTINCT cy.CustomerKey) AS previous_year_customers,
    COUNT(DISTINCT cc.CustomerKey) AS churned_customers,
    COUNT(DISTINCT cy.CustomerKey) - COUNT(DISTINCT cc.CustomerKey) AS retained_customers,
    100 - 100 * COUNT(DISTINCT cc.CustomerKey) / NULLIF(COUNT(DISTINCT cy.CustomerKey), 0) AS retention_rate
FROM customer_years cy
LEFT JOIN churned_customers cc
    ON cy.CustomerKey = cc.CustomerKey
    AND cy.previous_year = cc.previous_year
GROUP BY cy.current_year
ORDER BY cy.current_year;