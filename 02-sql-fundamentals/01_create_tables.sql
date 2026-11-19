-- ==========================================================================
-- LESSON 1: Creating Tables (DDL — Data Definition Language)
-- ==========================================================================
-- DDL is how you DEFINE the structure of your database.
-- Think of it as building the blueprint for your data warehouse.
-- ==========================================================================

-- -----------------------------------------------------------------------
-- 1. CREATE TABLE — Build your first table
-- -----------------------------------------------------------------------
-- Every table needs:
--   - A name (use snake_case)
--   - Columns with data types
--   - A PRIMARY KEY (unique identifier)

CREATE TABLE IF NOT EXISTS customers (
    customer_id     INTEGER PRIMARY KEY,       -- Unique identifier
    first_name      TEXT NOT NULL,              -- NOT NULL = required field
    last_name       TEXT NOT NULL,
    email           TEXT UNIQUE,                -- UNIQUE = no duplicates allowed
    city            TEXT DEFAULT 'Unknown',     -- DEFAULT value if not provided
    created_at      TEXT DEFAULT (datetime('now'))  -- Auto-set creation time
);

-- -----------------------------------------------------------------------
-- 2. MORE TABLE EXAMPLES — Products and Orders
-- -----------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS products (
    product_id      INTEGER PRIMARY KEY,
    product_name    TEXT NOT NULL,
    category        TEXT NOT NULL,
    price           REAL NOT NULL CHECK(price > 0),    -- CHECK constraint: price must be positive
    stock_quantity  INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    order_id        INTEGER PRIMARY KEY,
    customer_id     INTEGER NOT NULL,
    order_date      TEXT NOT NULL,
    total_amount    REAL NOT NULL,
    status          TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    -- FOREIGN KEY links this table to customers table
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Junction table for many-to-many relationship (order can have multiple products)
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id   INTEGER PRIMARY KEY,
    order_id        INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL CHECK(quantity > 0),
    unit_price      REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- -----------------------------------------------------------------------
-- 3. ALTER TABLE — Modify existing tables
-- -----------------------------------------------------------------------

-- Add a new column
ALTER TABLE customers ADD COLUMN phone TEXT;

-- Rename a table (SQLite syntax)
-- ALTER TABLE old_name RENAME TO new_name;

-- -----------------------------------------------------------------------
-- 4. DROP TABLE — Delete a table (⚠️ CAREFUL! Data is lost forever!)
-- -----------------------------------------------------------------------

-- DROP TABLE IF EXISTS temp_table;
-- ⚠️  Always use IF EXISTS to avoid errors

-- -----------------------------------------------------------------------
-- 5. INDEXES — Speed up queries on frequently searched columns
-- -----------------------------------------------------------------------

-- Create an index on email (used for lookups)
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);

-- Create an index on order_date (used for filtering by date)
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);

-- Composite index (for queries that filter on both columns)
CREATE INDEX IF NOT EXISTS idx_order_items_order_product
    ON order_items(order_id, product_id);

-- -----------------------------------------------------------------------
-- VERIFY: Check what we created
-- -----------------------------------------------------------------------
-- In SQLite, use these commands to inspect your schema:
--   .tables              → List all tables
--   .schema customers    → Show CREATE statement for a table
--   PRAGMA table_info(customers);  → Show column details

SELECT 'Tables created successfully!' AS status;
