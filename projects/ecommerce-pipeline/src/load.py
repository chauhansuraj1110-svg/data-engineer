"""
Load module — Write transformed data into SQLite database.

Creates the star schema tables and loads data using batch inserts
with proper error handling and transaction management.
"""

import sqlite3
import logging
from datetime import datetime
from . import models

logger = logging.getLogger(__name__)


def create_database(db_path):
    """
    Create the target database and all tables.

    Args:
        db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)

    for table_name in models.get_all_table_names():
        sql = models.SCHEMA[table_name]
        conn.execute(sql)
        logger.info(f"   Created table: {table_name}")

    conn.commit()
    conn.close()
    logger.info(f"📤 Database schema created at {db_path}")


def load_customers(db_path, customers):
    """Load customer records into dim_customers."""
    conn = sqlite3.connect(db_path)
    loaded = 0

    for record in customers:
        try:
            conn.execute(
                """INSERT OR REPLACE INTO dim_customers
                   (customer_id, first_name, last_name, email, email_domain, city, country, signup_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record["customer_id"],
                    record["first_name"],
                    record["last_name"],
                    record["email"],
                    record["email_domain"],
                    record["city"],
                    record["country"],
                    record["signup_date"],
                ),
            )
            loaded += 1
        except Exception as e:
            logger.warning(f"Failed to load customer {record.get('customer_id')}: {e}")

    conn.commit()
    conn.close()
    logger.info(f"   Loaded {loaded} customers into dim_customers")
    return loaded


def load_products(db_path, products):
    """Load product records into dim_products."""
    conn = sqlite3.connect(db_path)
    loaded = 0

    for record in products:
        try:
            conn.execute(
                """INSERT OR REPLACE INTO dim_products
                   (product_id, product_name, category, price, cost_price, profit_margin)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    record["product_id"],
                    record["product_name"],
                    record["category"],
                    record["price"],
                    record["cost_price"],
                    record["profit_margin"],
                ),
            )
            loaded += 1
        except Exception as e:
            logger.warning(f"Failed to load product {record.get('product_id')}: {e}")

    conn.commit()
    conn.close()
    logger.info(f"   Loaded {loaded} products into dim_products")
    return loaded


def load_orders(db_path, orders):
    """Load order records into fact_orders."""
    conn = sqlite3.connect(db_path)
    loaded = 0

    for record in orders:
        try:
            conn.execute(
                """INSERT OR REPLACE INTO fact_orders
                   (order_id, customer_id, product_id, quantity, unit_price,
                    line_total, order_date, status, product_category)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record["order_id"],
                    record["customer_id"],
                    record["product_id"],
                    record["quantity"],
                    record["unit_price"],
                    record["line_total"],
                    record["order_date"],
                    record["status"],
                    record["product_category"],
                ),
            )
            loaded += 1
        except Exception as e:
            logger.warning(f"Failed to load order {record.get('order_id')}: {e}")

    conn.commit()
    conn.close()
    logger.info(f"   Loaded {loaded} orders into fact_orders")
    return loaded


def log_pipeline_run(db_path, pipeline_name, stats, status="success", error_message=None):
    """Record this pipeline run in the audit log."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """INSERT INTO pipeline_log
           (pipeline_name, started_at, completed_at,
            customers_loaded, products_loaded, orders_loaded,
            total_rejected, status, error_message)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            pipeline_name,
            stats.get("started_at"),
            datetime.now().isoformat(),
            stats.get("customers_loaded", 0),
            stats.get("products_loaded", 0),
            stats.get("orders_loaded", 0),
            stats.get("total_rejected", 0),
            status,
            error_message,
        ),
    )
    conn.commit()
    conn.close()
    logger.info(f"   Pipeline run logged to pipeline_log table")


def load_all(db_path, transformed_data):
    """
    Load all transformed data into the database.

    Args:
        db_path: Path to the SQLite database.
        transformed_data: Dict with 'customers', 'products', 'orders'.

    Returns:
        Dict with load counts.
    """
    logger.info(f"📤 Starting load into {db_path}")

    # Create schema first
    create_database(db_path)

    # Load in dependency order (dimensions before facts)
    customers_loaded = load_customers(db_path, transformed_data.get("customers", []))
    products_loaded = load_products(db_path, transformed_data.get("products", []))
    orders_loaded = load_orders(db_path, transformed_data.get("orders", []))

    stats = {
        "customers_loaded": customers_loaded,
        "products_loaded": products_loaded,
        "orders_loaded": orders_loaded,
    }

    total = sum(stats.values())
    logger.info(f"📤 Load complete: {total} total records loaded")
    return stats
