"""
Pipeline orchestrator — Wires Extract → Transform → Load together.

Run with:
    python -m src.pipeline
"""

import logging
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

from .extract import extract_all
from .transform import transform_all
from .load import load_all, log_pipeline_run

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"
DB_PATH = PROJECT_DIR / "data" / "ecommerce.db"
PIPELINE_NAME = "ecommerce_etl"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(PIPELINE_NAME)


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================
def run():
    """
    Run the complete E-Commerce ETL pipeline.

    Steps:
        1. Extract raw data from CSV files
        2. Transform (clean, validate, enrich)
        3. Load into SQLite star schema
        4. Log the pipeline run
        5. Print a summary report
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info(f"🚀 PIPELINE '{PIPELINE_NAME}' STARTED")
    logger.info(f"   Source: {DATA_DIR}")
    logger.info(f"   Target: {DB_PATH}")
    logger.info("=" * 60)

    try:
        # ------------------------------------------------------------------
        # STEP 1: EXTRACT
        # ------------------------------------------------------------------
        raw_data = extract_all(DATA_DIR)

        # ------------------------------------------------------------------
        # STEP 2: TRANSFORM
        # ------------------------------------------------------------------
        transformed_data, rejected = transform_all(raw_data)

        # ------------------------------------------------------------------
        # STEP 3: LOAD
        # ------------------------------------------------------------------
        load_stats = load_all(DB_PATH, transformed_data)

        # ------------------------------------------------------------------
        # STEP 4: LOG PIPELINE RUN
        # ------------------------------------------------------------------
        total_rejected = sum(len(v) for v in rejected.values())
        run_stats = {
            **load_stats,
            "started_at": start_time.isoformat(),
            "total_rejected": total_rejected,
        }
        log_pipeline_run(DB_PATH, PIPELINE_NAME, run_stats)

        # ------------------------------------------------------------------
        # STEP 5: SUMMARY REPORT
        # ------------------------------------------------------------------
        duration = (datetime.now() - start_time).total_seconds()

        logger.info("")
        logger.info("=" * 60)
        logger.info(f"✅ PIPELINE COMPLETED in {duration:.2f}s")
        logger.info("=" * 60)
        logger.info(f"   📥 Extracted:")
        for source, records in raw_data.items():
            logger.info(f"      {source}: {len(records)} records")
        logger.info(f"   🔄 Transformed:")
        for source, records in transformed_data.items():
            logger.info(f"      {source}: {len(records)} valid")
        logger.info(f"   ❌ Rejected: {total_rejected} total")
        for source, recs in rejected.items():
            if recs:
                logger.info(f"      {source}: {len(recs)}")
                for r in recs:
                    logger.info(f"         → {r['error']}")
        logger.info(f"   📤 Loaded:")
        for key, count in load_stats.items():
            logger.info(f"      {key}: {count}")
        logger.info("=" * 60)

        # ------------------------------------------------------------------
        # BONUS: Quick data quality check
        # ------------------------------------------------------------------
        _print_sample_queries(DB_PATH)

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"💥 PIPELINE FAILED after {duration:.2f}s: {e}")
        try:
            log_pipeline_run(
                DB_PATH, PIPELINE_NAME,
                {"started_at": start_time.isoformat(), "total_rejected": 0},
                status="failed", error_message=str(e)
            )
        except Exception:
            pass
        sys.exit(1)


def _print_sample_queries(db_path):
    """Run a few quick queries to verify the loaded data."""
    logger.info("")
    logger.info("📊 SAMPLE QUERIES (verifying loaded data)")
    logger.info("-" * 60)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Query 1: Top customers by revenue
    logger.info("Top 5 Customers by Revenue:")
    rows = conn.execute("""
        SELECT c.first_name || ' ' || c.last_name AS name,
               c.city,
               COUNT(o.order_id) AS total_orders,
               ROUND(SUM(o.line_total), 2) AS total_revenue
        FROM fact_orders o
        JOIN dim_customers c ON o.customer_id = c.customer_id
        GROUP BY o.customer_id
        ORDER BY total_revenue DESC
        LIMIT 5
    """).fetchall()
    for row in rows:
        logger.info(f"   {row['name']:25s} | {row['city']:15s} | {row['total_orders']} orders | ${row['total_revenue']:>10.2f}")

    # Query 2: Revenue by category
    logger.info("")
    logger.info("Revenue by Product Category:")
    rows = conn.execute("""
        SELECT product_category,
               COUNT(*) AS num_orders,
               ROUND(SUM(line_total), 2) AS total_revenue
        FROM fact_orders
        GROUP BY product_category
        ORDER BY total_revenue DESC
    """).fetchall()
    for row in rows:
        logger.info(f"   {row['product_category']:20s} | {row['num_orders']} orders | ${row['total_revenue']:>10.2f}")

    # Query 3: Monthly trend
    logger.info("")
    logger.info("Monthly Revenue Trend:")
    rows = conn.execute("""
        SELECT substr(order_date, 1, 7) AS month,
               COUNT(*) AS num_orders,
               ROUND(SUM(line_total), 2) AS revenue
        FROM fact_orders
        WHERE order_date IS NOT NULL
        GROUP BY month
        ORDER BY month
    """).fetchall()
    for row in rows:
        logger.info(f"   {row['month']} | {row['num_orders']:3d} orders | ${row['revenue']:>10.2f}")

    conn.close()
    logger.info("-" * 60)


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    run()
