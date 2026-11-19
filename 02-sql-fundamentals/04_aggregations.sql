-- ==========================================================================
-- LESSON 4: Aggregations & Window Functions
-- ==========================================================================
-- Aggregations summarize data. Window functions are a SUPERPOWER that
-- let you calculate things across related rows without collapsing them.
--
-- Prerequisites: Run 01_create_tables.sql and 02_crud_operations.sql first.
-- ==========================================================================

-- -----------------------------------------------------------------------
-- 1. GROUP BY — Summarize data by category
-- -----------------------------------------------------------------------

-- Orders per customer
SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_spent,
    ROUND(AVG(total_amount), 2) AS avg_order,
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id;

-- Orders by status
SELECT
    status,
    COUNT(*) AS count,
    SUM(total_amount) AS total_value
FROM orders
GROUP BY status
ORDER BY count DESC;

-- -----------------------------------------------------------------------
-- 2. HAVING — Filter AFTER aggregation
-- -----------------------------------------------------------------------
-- WHERE filters rows BEFORE grouping
-- HAVING filters groups AFTER aggregation

-- Customers who spent more than $500 total
SELECT
    customer_id,
    SUM(total_amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(total_amount) > 500
ORDER BY total_spent DESC;

-- Categories with more than 2 products
SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
HAVING COUNT(*) > 2;

-- -----------------------------------------------------------------------
-- 3. SUBQUERIES — Queries inside queries
-- -----------------------------------------------------------------------

-- Find customers whose total spend is above average
SELECT
    c.first_name,
    c.last_name,
    order_summary.total_spent
FROM customers c
INNER JOIN (
    -- This subquery calculates total spend per customer
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
) AS order_summary ON c.customer_id = order_summary.customer_id
WHERE order_summary.total_spent > (
    -- This subquery calculates the overall average
    SELECT AVG(total_amount) FROM orders
);

-- -----------------------------------------------------------------------
-- 4. WINDOW FUNCTIONS — The Data Engineer's Superpower! 🦸
-- -----------------------------------------------------------------------
-- Window functions perform calculations ACROSS rows WITHOUT collapsing them.
-- Syntax: function() OVER (PARTITION BY ... ORDER BY ...)

-- ROW_NUMBER — Assign a sequence number within each group
SELECT
    customer_id,
    order_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id     -- Restart numbering for each customer
        ORDER BY order_date          -- Number in date order
    ) AS order_sequence
FROM orders;

-- -----------------------------------------------------------------------
-- 5. RANKING FUNCTIONS
-- -----------------------------------------------------------------------

-- RANK — Rank products by price within each category
SELECT
    product_name,
    category,
    price,
    RANK() OVER (
        PARTITION BY category
        ORDER BY price DESC
    ) AS price_rank
FROM products;

-- DENSE_RANK — Like RANK but no gaps in numbering
-- (if two items tie for rank 1, the next is rank 2, not rank 3)

-- -----------------------------------------------------------------------
-- 6. RUNNING TOTALS & MOVING AVERAGES
-- -----------------------------------------------------------------------

-- Cumulative revenue over time (running total)
SELECT
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM orders
ORDER BY order_date;

-- -----------------------------------------------------------------------
-- 7. LAG & LEAD — Look at previous/next rows
-- -----------------------------------------------------------------------

-- Compare each order to the previous order's amount
SELECT
    order_id,
    order_date,
    total_amount,
    LAG(total_amount, 1) OVER (ORDER BY order_date) AS prev_order_amount,
    total_amount - LAG(total_amount, 1) OVER (ORDER BY order_date) AS difference
FROM orders
ORDER BY order_date;

-- -----------------------------------------------------------------------
-- 8. PRACTICAL ANALYTICS QUERIES
-- -----------------------------------------------------------------------

-- Monthly revenue summary
SELECT
    substr(order_date, 1, 7) AS month,
    COUNT(*) AS num_orders,
    SUM(total_amount) AS monthly_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
GROUP BY substr(order_date, 1, 7)
ORDER BY month;

-- Customer lifetime value (CLV) ranking
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value,
    RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS clv_rank
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY clv_rank;

-- Product performance with category comparison
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity * oi.unit_price) AS product_revenue,
    SUM(SUM(oi.quantity * oi.unit_price)) OVER (
        PARTITION BY p.category
    ) AS category_total,
    ROUND(
        SUM(oi.quantity * oi.unit_price) * 100.0 /
        SUM(SUM(oi.quantity * oi.unit_price)) OVER (PARTITION BY p.category),
        1
    ) AS pct_of_category
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY p.category, product_revenue DESC;

SELECT 'Aggregations & window functions lesson complete!' AS status;
