-- ==========================================================================
-- LESSON 3: JOINs — Combining Data from Multiple Tables
-- ==========================================================================
-- JOINs are the MOST IMPORTANT SQL concept for data engineers.
-- Real data lives across many tables. JOINs bring it together.
--
-- Prerequisites: Run 01_create_tables.sql and 02_crud_operations.sql first.
-- ==========================================================================

-- -----------------------------------------------------------------------
-- 1. INNER JOIN — Only matching rows from BOTH tables
-- -----------------------------------------------------------------------
-- "Show me orders with their customer names"
-- Only returns rows where customer_id exists in BOTH tables.

SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    o.order_date,
    o.total_amount,
    o.status
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date;

-- Explanation:
--   orders o          → 'o' is an alias for the orders table
--   INNER JOIN         → only include rows that match
--   ON o.customer_id = c.customer_id  → the "join condition"

-- -----------------------------------------------------------------------
-- 2. LEFT JOIN — ALL rows from left table, matching from right
-- -----------------------------------------------------------------------
-- "Show me ALL customers and their orders (even if they never ordered)"
-- Customers with no orders will have NULL for order columns.

SELECT
    c.first_name,
    c.last_name,
    o.order_id,
    o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.first_name;

-- 💡 LEFT JOIN is your best friend for finding "missing" data:
-- "Which customers have NEVER placed an order?"
SELECT
    c.first_name,
    c.last_name,
    c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- -----------------------------------------------------------------------
-- 3. JOINING MULTIPLE TABLES (very common!)
-- -----------------------------------------------------------------------
-- "Show me each order with customer name, product name, and quantity"
-- This joins 4 tables together!

SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total,
    o.order_date
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_date, c.last_name;

-- -----------------------------------------------------------------------
-- 4. SELF JOIN — Joining a table to itself
-- -----------------------------------------------------------------------
-- "Find customers who live in the same city"

SELECT
    c1.first_name AS customer_1,
    c2.first_name AS customer_2,
    c1.city
FROM customers c1
INNER JOIN customers c2
    ON c1.city = c2.city
    AND c1.customer_id < c2.customer_id   -- Avoid duplicate pairs
ORDER BY c1.city;

-- -----------------------------------------------------------------------
-- 5. CROSS JOIN — Every row paired with every row (use carefully!)
-- -----------------------------------------------------------------------
-- "Show every possible customer-product combination"
-- ⚠️  Result size = rows_table_1 × rows_table_2 (can be HUGE)

SELECT
    c.first_name,
    p.product_name,
    p.price
FROM customers c
CROSS JOIN products p
WHERE p.category = 'Electronics'  -- Filter to keep it small
ORDER BY c.first_name, p.price;

-- -----------------------------------------------------------------------
-- 6. PRACTICAL JOIN PATTERNS FOR DATA ENGINEERING
-- -----------------------------------------------------------------------

-- PATTERN 1: Revenue by customer (business report)
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(DISTINCT o.order_id) AS num_orders,
    SUM(o.total_amount) AS total_spent,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;

-- PATTERN 2: Top selling products
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC;

-- PATTERN 3: Orders by city (geographic analysis)
SELECT
    c.city,
    COUNT(o.order_id) AS num_orders,
    SUM(o.total_amount) AS total_revenue,
    COUNT(DISTINCT c.customer_id) AS unique_customers
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;

SELECT 'JOINs lesson complete!' AS status;
