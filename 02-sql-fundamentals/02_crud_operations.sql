-- ==========================================================================
-- LESSON 2: CRUD Operations (DML — Data Manipulation Language)
-- ==========================================================================
-- CRUD = Create, Read, Update, Delete
-- These are the four basic operations for working with data.
-- ==========================================================================

-- First, run 01_create_tables.sql to create the tables!

-- -----------------------------------------------------------------------
-- 1. INSERT — Adding data to tables
-- -----------------------------------------------------------------------

-- Insert a single row
INSERT INTO customers (customer_id, first_name, last_name, email, city)
VALUES (1, 'Alice', 'Johnson', 'alice@example.com', 'New York');

-- Insert multiple rows at once
INSERT INTO customers (customer_id, first_name, last_name, email, city)
VALUES
    (2, 'Bob', 'Smith', 'bob@example.com', 'San Francisco'),
    (3, 'Charlie', 'Brown', 'charlie@example.com', 'New York'),
    (4, 'Diana', 'Ross', 'diana@example.com', 'Chicago'),
    (5, 'Eve', 'Davis', 'eve@example.com', 'San Francisco'),
    (6, 'Frank', 'Wilson', 'frank@example.com', 'Chicago');

-- Insert products
INSERT INTO products (product_id, product_name, category, price, stock_quantity)
VALUES
    (1, 'Laptop', 'Electronics', 999.99, 50),
    (2, 'Mouse', 'Electronics', 29.99, 200),
    (3, 'Desk Chair', 'Furniture', 249.99, 30),
    (4, 'Notebook', 'Stationery', 5.99, 500),
    (5, 'Monitor', 'Electronics', 399.99, 75),
    (6, 'Keyboard', 'Electronics', 79.99, 150);

-- Insert orders
INSERT INTO orders (order_id, customer_id, order_date, total_amount, status)
VALUES
    (1, 1, '2024-01-15', 1029.98, 'delivered'),
    (2, 2, '2024-01-16', 29.99, 'delivered'),
    (3, 1, '2024-01-20', 249.99, 'shipped'),
    (4, 3, '2024-02-01', 485.97, 'delivered'),
    (5, 4, '2024-02-05', 5.99, 'pending'),
    (6, 5, '2024-02-10', 1399.98, 'shipped'),
    (7, 3, '2024-02-15', 79.99, 'pending');

-- Insert order items
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price)
VALUES
    (1, 1, 1, 1, 999.99),   -- Alice bought 1 Laptop
    (2, 1, 2, 1, 29.99),    -- Alice also bought 1 Mouse
    (3, 2, 2, 1, 29.99),    -- Bob bought 1 Mouse
    (4, 3, 3, 1, 249.99),   -- Alice bought 1 Desk Chair
    (5, 4, 5, 1, 399.99),   -- Charlie bought 1 Monitor
    (6, 4, 4, 1, 5.99),     -- Charlie also bought 1 Notebook
    (7, 4, 6, 1, 79.99),    -- Charlie also bought 1 Keyboard
    (8, 5, 4, 1, 5.99),     -- Diana bought 1 Notebook
    (9, 6, 1, 1, 999.99),   -- Eve bought 1 Laptop
    (10, 6, 5, 1, 399.99),  -- Eve also bought 1 Monitor
    (11, 7, 6, 1, 79.99);   -- Charlie bought 1 Keyboard

-- -----------------------------------------------------------------------
-- 2. SELECT — Reading/querying data (the most important SQL operation!)
-- -----------------------------------------------------------------------

-- Select ALL columns
SELECT * FROM customers;

-- Select specific columns
SELECT first_name, last_name, city FROM customers;

-- WHERE clause — filtering rows
SELECT * FROM customers WHERE city = 'New York';

-- Multiple conditions with AND/OR
SELECT * FROM orders
WHERE status = 'delivered' AND total_amount > 100;

-- LIKE — pattern matching
SELECT * FROM customers WHERE email LIKE '%example.com';

-- IN — match against a list
SELECT * FROM customers WHERE city IN ('New York', 'Chicago');

-- BETWEEN — range queries
SELECT * FROM orders WHERE total_amount BETWEEN 50 AND 500;

-- ORDER BY — sorting results
SELECT * FROM orders ORDER BY total_amount DESC;

-- LIMIT — restrict number of results
SELECT * FROM orders ORDER BY total_amount DESC LIMIT 3;

-- DISTINCT — unique values only
SELECT DISTINCT city FROM customers;

-- COUNT, SUM, AVG, MIN, MAX — aggregate functions
SELECT
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    MIN(total_amount) AS smallest_order,
    MAX(total_amount) AS largest_order
FROM orders;

-- -----------------------------------------------------------------------
-- 3. UPDATE — Modifying existing data
-- -----------------------------------------------------------------------

-- Update a single row
UPDATE orders SET status = 'delivered' WHERE order_id = 3;

-- Update multiple rows
UPDATE products SET stock_quantity = stock_quantity - 1
WHERE product_id IN (1, 2);

-- ⚠️  ALWAYS use WHERE with UPDATE! Without it, ALL rows get updated.
-- ❌  UPDATE customers SET city = 'Unknown';  -- Updates EVERY customer!

-- -----------------------------------------------------------------------
-- 4. DELETE — Removing data
-- -----------------------------------------------------------------------

-- Delete specific rows
-- DELETE FROM orders WHERE status = 'cancelled';

-- ⚠️  ALWAYS use WHERE with DELETE! Without it, ALL rows get deleted.
-- ❌  DELETE FROM customers;  -- Deletes EVERY customer!

-- -----------------------------------------------------------------------
-- 5. USEFUL PATTERNS FOR DATA ENGINEERING
-- -----------------------------------------------------------------------

-- CASE expression (if/else in SQL)
SELECT
    first_name,
    city,
    CASE
        WHEN city = 'New York' THEN 'East Coast'
        WHEN city = 'San Francisco' THEN 'West Coast'
        ELSE 'Central'
    END AS region
FROM customers;

-- COALESCE — handle NULL values (very common in data cleaning!)
SELECT
    first_name,
    COALESCE(phone, 'No phone') AS phone_number
FROM customers;

-- String functions
SELECT
    first_name,
    UPPER(last_name) AS last_name_upper,
    LENGTH(email) AS email_length
FROM customers;

SELECT 'CRUD operations demo complete!' AS status;
