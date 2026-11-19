"""
=============================================================================
 ETL LESSON 3: Load — Storing Data in Databases
=============================================================================
 The final step: load your transformed data into a target database.
 We'll use SQLite (built into Python) — same concepts apply to
 PostgreSQL, MySQL, BigQuery, Snowflake, etc.
=============================================================================
"""

import sqlite3
import os
from datetime import datetime


# ---------------------------------------------------------------------------
# 1. CREATE DATABASE AND TABLES
# ---------------------------------------------------------------------------
print("=" * 60)
print("1. Creating database schema")
print("=" * 60)

DB_PATH = "lesson_load.db"


def create_schema(db_path):
    """Create the target database schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE,
            email_domain  TEXT,
            tier          TEXT,
            created_at    TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            run_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            pipeline_name TEXT NOT NULL,
            started_at    TEXT,
            completed_at  TEXT,
            records_loaded INTEGER,
            records_failed INTEGER,
            status        TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("   ✅ Schema created!")


create_schema(DB_PATH)


# ---------------------------------------------------------------------------
# 2. INSERT RECORDS — One at a time
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. Loading records one at a time")
print("=" * 60)


def load_single(db_path, record):
    """Insert a single record. Returns True on success."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """INSERT INTO customers (name, email, email_domain, tier)
               VALUES (?, ?, ?, ?)""",
            (record["name"], record["email"], record.get("email_domain"), record.get("tier"))
        )
        conn.commit()
        print(f"   ✅ Loaded: {record['name']}")
        return True
    except sqlite3.IntegrityError as e:
        print(f"   ⚠️  Duplicate skipped: {record['name']} ({e})")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        conn.close()


# Load some records
records = [
    {"name": "Alice Johnson", "email": "alice@gmail.com", "email_domain": "gmail.com", "tier": "high"},
    {"name": "Bob Smith", "email": "bob@company.com", "email_domain": "company.com", "tier": "medium"},
    {"name": "Charlie Brown", "email": "charlie@mail.com", "email_domain": "mail.com", "tier": "high"},
]

for record in records:
    load_single(DB_PATH, record)


# ---------------------------------------------------------------------------
# 3. BATCH INSERT — Much faster for large datasets
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. Batch loading (faster!)")
print("=" * 60)


def load_batch(db_path, records):
    """
    Insert multiple records in a single transaction.
    This is MUCH faster than inserting one at a time.
    """
    conn = sqlite3.connect(db_path)
    loaded = 0
    failed = 0

    try:
        for record in records:
            try:
                conn.execute(
                    """INSERT INTO customers (name, email, email_domain, tier)
                       VALUES (?, ?, ?, ?)""",
                    (record["name"], record["email"], record.get("email_domain"), record.get("tier"))
                )
                loaded += 1
            except sqlite3.IntegrityError:
                failed += 1  # Skip duplicates

        conn.commit()  # Commit ALL at once (much faster!)
        print(f"   ✅ Batch loaded: {loaded} records ({failed} skipped)")

    except Exception as e:
        conn.rollback()  # Undo ALL changes if something goes wrong
        print(f"   ❌ Batch failed, rolled back: {e}")

    finally:
        conn.close()

    return loaded, failed


batch_records = [
    {"name": "Diana Ross", "email": "diana@work.com", "email_domain": "work.com", "tier": "low"},
    {"name": "Eve Davis", "email": "eve@startup.io", "email_domain": "startup.io", "tier": "medium"},
    {"name": "Alice Johnson", "email": "alice@gmail.com", "email_domain": "gmail.com", "tier": "high"},  # Duplicate!
]

load_batch(DB_PATH, batch_records)


# ---------------------------------------------------------------------------
# 4. UPSERT PATTERN — Insert or Update if exists
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. Upsert (Insert or Update)")
print("=" * 60)


def upsert(db_path, record):
    """Insert a record, or update it if the email already exists."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """INSERT INTO customers (name, email, email_domain, tier)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(email) DO UPDATE SET
                   name = excluded.name,
                   tier = excluded.tier""",
            (record["name"], record["email"], record.get("email_domain"), record.get("tier"))
        )
        conn.commit()
        print(f"   ✅ Upserted: {record['name']}")
    finally:
        conn.close()


# Update Alice's tier
upsert(DB_PATH, {"name": "Alice Johnson", "email": "alice@gmail.com", "email_domain": "gmail.com", "tier": "premium"})


# ---------------------------------------------------------------------------
# 5. VERIFY THE LOADED DATA
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("5. Verify loaded data")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.execute("SELECT * FROM customers ORDER BY customer_id")
rows = cursor.fetchall()

print(f"   Total customers in database: {len(rows)}")
for row in rows:
    print(f"   ID={row['customer_id']} | {row['name']} | {row['email']} | tier={row['tier']}")

conn.close()


# ---------------------------------------------------------------------------
# 6. LOG PIPELINE RUNS (good practice!)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("6. Logging pipeline runs")
print("=" * 60)


def log_pipeline_run(db_path, pipeline_name, loaded, failed, status="success"):
    """Record this pipeline run for auditing."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """INSERT INTO pipeline_runs (pipeline_name, started_at, completed_at, records_loaded, records_failed, status)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (pipeline_name, datetime.now().isoformat(), datetime.now().isoformat(), loaded, failed, status)
    )
    conn.commit()
    conn.close()
    print(f"   ✅ Pipeline run logged: {pipeline_name} ({loaded} loaded, {failed} failed)")


log_pipeline_run(DB_PATH, "customer_pipeline", loaded=5, failed=1)


# ---------------------------------------------------------------------------
# CLEANUP
# ---------------------------------------------------------------------------
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

print("\n✅ Load lesson complete!")
print("👉 Next: Run 04_full_pipeline.py to see it all connected!")
