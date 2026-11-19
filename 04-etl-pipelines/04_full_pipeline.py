"""
=============================================================================
 ETL LESSON 4: Full Pipeline — Extract → Transform → Load
=============================================================================
 Putting it all together! This is a complete, runnable ETL pipeline
 that demonstrates how extract, transform, and load work together.
=============================================================================
"""

import csv
import json
import sqlite3
import os
import logging
from datetime import datetime

# ---------------------------------------------------------------------------
# SETUP LOGGING
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("etl_pipeline")

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
CONFIG = {
    "source_file": "pipeline_source.csv",
    "database": "pipeline_output.db",
    "pipeline_name": "demo_full_pipeline",
}


# ===========================================================================
# STEP 1: EXTRACT
# ===========================================================================
def extract(filepath):
    """Extract records from a CSV file."""
    logger.info(f"📥 EXTRACT: Reading from {filepath}")
    records = []

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    logger.info(f"📥 EXTRACT: Got {len(records)} records")
    return records


# ===========================================================================
# STEP 2: TRANSFORM
# ===========================================================================
def transform(records):
    """Clean, validate, and enrich records."""
    logger.info(f"🔄 TRANSFORM: Processing {len(records)} records")

    transformed = []
    rejected = []

    for record in records:
        try:
            # --- CLEAN ---
            cleaned = {
                "name": (record.get("name") or "").strip().title(),
                "email": (record.get("email") or "").strip().lower(),
                "amount": _safe_float(record.get("amount", "0")),
                "date": _parse_date(record.get("date", "")),
            }

            # --- VALIDATE ---
            if not cleaned["name"] or cleaned["name"] == "":
                raise ValueError("Name is required")
            if "@" not in cleaned.get("email", ""):
                raise ValueError("Invalid email")
            if cleaned["amount"] <= 0:
                raise ValueError(f"Invalid amount: {cleaned['amount']}")

            # --- ENRICH ---
            cleaned["email_domain"] = cleaned["email"].split("@")[1]
            cleaned["tier"] = _classify_tier(cleaned["amount"])
            cleaned["processed_at"] = datetime.now().isoformat()

            transformed.append(cleaned)

        except Exception as e:
            rejected.append({"record": record, "error": str(e)})
            logger.warning(f"🔄 TRANSFORM: Rejected record — {e}")

    logger.info(
        f"🔄 TRANSFORM: {len(transformed)} valid, {len(rejected)} rejected"
    )
    return transformed, rejected


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _parse_date(value):
    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y"]:
        try:
            return datetime.strptime(value.strip(), fmt).strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            continue
    return None


def _classify_tier(amount):
    if amount >= 200:
        return "gold"
    elif amount >= 100:
        return "silver"
    return "bronze"


# ===========================================================================
# STEP 3: LOAD
# ===========================================================================
def load(records, db_path):
    """Load transformed records into SQLite database."""
    logger.info(f"📤 LOAD: Writing {len(records)} records to {db_path}")

    conn = sqlite3.connect(db_path)

    # Create table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT,
            email_domain  TEXT,
            amount        REAL,
            date          TEXT,
            tier          TEXT,
            processed_at  TEXT
        )
    """)

    # Batch insert
    loaded = 0
    for record in records:
        conn.execute(
            """INSERT INTO transactions (name, email, email_domain, amount, date, tier, processed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                record["name"],
                record["email"],
                record["email_domain"],
                record["amount"],
                record["date"],
                record["tier"],
                record["processed_at"],
            ),
        )
        loaded += 1

    conn.commit()
    conn.close()

    logger.info(f"📤 LOAD: Successfully loaded {loaded} records")
    return loaded


# ===========================================================================
# ORCHESTRATOR — Wire it all together
# ===========================================================================
def run_pipeline(config):
    """
    Main pipeline orchestrator.
    Runs Extract → Transform → Load and reports results.
    """
    pipeline_name = config["pipeline_name"]
    start_time = datetime.now()
    logger.info(f"🚀 PIPELINE '{pipeline_name}' STARTED")

    try:
        # EXTRACT
        raw_records = extract(config["source_file"])

        # TRANSFORM
        clean_records, rejected = transform(raw_records)

        # LOAD
        loaded_count = load(clean_records, config["database"])

        # SUMMARY
        duration = (datetime.now() - start_time).total_seconds()
        logger.info("=" * 50)
        logger.info(f"✅ PIPELINE '{pipeline_name}' COMPLETED in {duration:.2f}s")
        logger.info(f"   📥 Extracted:    {len(raw_records)}")
        logger.info(f"   🔄 Transformed:  {len(clean_records)}")
        logger.info(f"   ❌ Rejected:     {len(rejected)}")
        logger.info(f"   📤 Loaded:       {loaded_count}")
        logger.info("=" * 50)

        return {
            "status": "success",
            "extracted": len(raw_records),
            "transformed": len(clean_records),
            "rejected": len(rejected),
            "loaded": loaded_count,
            "duration_seconds": duration,
        }

    except Exception as e:
        logger.error(f"💥 PIPELINE FAILED: {e}")
        return {"status": "failed", "error": str(e)}


# ===========================================================================
# CREATE SAMPLE DATA & RUN
# ===========================================================================
if __name__ == "__main__":
    # Create sample source data
    source_file = CONFIG["source_file"]
    with open(source_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email", "amount", "date"])
        writer.writeheader()
        writer.writerows([
            {"name": "  Alice Johnson  ", "email": "ALICE@gmail.com", "amount": "250.00", "date": "2024-01-15"},
            {"name": "Bob Smith", "email": "bob@company.com", "amount": "89.99", "date": "01/20/2024"},
            {"name": "Charlie Brown", "email": "charlie@mail.com", "amount": "175.50", "date": "2024-02-01"},
            {"name": "", "email": "nobody@test.com", "amount": "100", "date": "2024-02-05"},  # Will be rejected (no name)
            {"name": "Eve Davis", "email": "eve@startup.io", "amount": "invalid", "date": "2024-02-10"},  # Will be rejected
            {"name": "Frank Wilson", "email": "frank@work.com", "amount": "320.00", "date": "2024-02-15"},
        ])

    # Run the pipeline!
    result = run_pipeline(CONFIG)

    # Show what's in the database
    if result["status"] == "success":
        print("\n📊 Database contents:")
        conn = sqlite3.connect(CONFIG["database"])
        conn.row_factory = sqlite3.Row
        for row in conn.execute("SELECT * FROM transactions"):
            print(f"   {row['name']:20s} | {row['email']:25s} | ${row['amount']:>8.2f} | {row['tier']}")
        conn.close()

    # Cleanup
    for f in [CONFIG["source_file"], CONFIG["database"]]:
        if os.path.exists(f):
            os.remove(f)

    print("\n✅ Full pipeline lesson complete!")
    print("👉 Next: Build the starter project in projects/ecommerce-pipeline/!")
