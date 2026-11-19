"""
Models module — Database schema definitions.

Defines the target database schema as SQL CREATE TABLE statements.
This follows a star schema design optimized for analytics.
"""

# ==========================================================================
# SCHEMA DEFINITIONS
# ==========================================================================

SCHEMA = {
    "dim_customers": """
        CREATE TABLE IF NOT EXISTS dim_customers (
            customer_id     INTEGER PRIMARY KEY,
            first_name      TEXT NOT NULL,
            last_name       TEXT,
            email           TEXT,
            email_domain    TEXT,
            city            TEXT,
            country         TEXT,
            signup_date     TEXT,
            loaded_at       TEXT DEFAULT (datetime('now'))
        )
    """,

    "dim_products": """
        CREATE TABLE IF NOT EXISTS dim_products (
            product_id      INTEGER PRIMARY KEY,
            product_name    TEXT NOT NULL,
            category        TEXT,
            price           REAL,
            cost_price      REAL,
            profit_margin   REAL,
            loaded_at       TEXT DEFAULT (datetime('now'))
        )
    """,

    "fact_orders": """
        CREATE TABLE IF NOT EXISTS fact_orders (
            order_id            INTEGER PRIMARY KEY,
            customer_id         INTEGER NOT NULL,
            product_id          INTEGER NOT NULL,
            quantity            INTEGER NOT NULL,
            unit_price          REAL,
            line_total          REAL,
            order_date          TEXT,
            status              TEXT,
            product_category    TEXT,
            loaded_at           TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
        )
    """,

    "pipeline_log": """
        CREATE TABLE IF NOT EXISTS pipeline_log (
            run_id              INTEGER PRIMARY KEY AUTOINCREMENT,
            pipeline_name       TEXT NOT NULL,
            started_at          TEXT,
            completed_at        TEXT,
            customers_loaded    INTEGER,
            products_loaded     INTEGER,
            orders_loaded       INTEGER,
            total_rejected      INTEGER,
            status              TEXT,
            error_message       TEXT
        )
    """,
}


def get_all_table_names():
    """Return ordered list of table names (creation order matters for FK)."""
    return ["dim_customers", "dim_products", "fact_orders", "pipeline_log"]
