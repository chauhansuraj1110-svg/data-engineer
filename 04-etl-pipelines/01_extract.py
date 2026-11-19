"""
=============================================================================
 ETL LESSON 1: Extract — Getting Data From Sources
=============================================================================
 The first step in any pipeline: get the data.
 Common sources: CSV files, JSON files, APIs, databases.
=============================================================================
"""

import csv
import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# 1. EXTRACT FROM CSV
# ---------------------------------------------------------------------------
print("=" * 60)
print("1. Extract from CSV")
print("=" * 60)


def extract_csv(filepath):
    """
    Extract data from a CSV file.
    Returns a list of dictionaries (one per row).
    """
    records = []
    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))  # Convert OrderedDict → dict
        print(f"   ✅ Extracted {len(records)} records from {filepath}")
    except FileNotFoundError:
        print(f"   ❌ File not found: {filepath}")
    except Exception as e:
        print(f"   ❌ Error reading CSV: {e}")
    return records


# Create a sample CSV to extract from
sample_csv = "sample_extract.csv"
with open(sample_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "amount"])
    writer.writeheader()
    writer.writerows([
        {"id": "1", "name": "Alice", "amount": "150.00"},
        {"id": "2", "name": "Bob", "amount": "89.50"},
        {"id": "3", "name": "Charlie", "amount": "210.75"},
    ])

data = extract_csv(sample_csv)
for row in data:
    print(f"   {row}")


# ---------------------------------------------------------------------------
# 2. EXTRACT FROM JSON
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. Extract from JSON")
print("=" * 60)


def extract_json(filepath):
    """
    Extract data from a JSON file.
    Handles both JSON arrays and objects with a 'data' key.
    """
    try:
        with open(filepath, "r") as f:
            raw = json.load(f)

        # Handle different JSON structures
        if isinstance(raw, list):
            records = raw
        elif isinstance(raw, dict) and "data" in raw:
            records = raw["data"]
        else:
            records = [raw]

        print(f"   ✅ Extracted {len(records)} records from {filepath}")
        return records
    except FileNotFoundError:
        print(f"   ❌ File not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        print(f"   ❌ Invalid JSON: {e}")
        return []


# Create a sample JSON to extract from
sample_json = "sample_extract.json"
with open(sample_json, "w") as f:
    json.dump({
        "status": "ok",
        "data": [
            {"id": 1, "event": "login", "timestamp": "2024-01-15T10:00:00Z"},
            {"id": 2, "event": "purchase", "timestamp": "2024-01-15T10:05:00Z"},
        ]
    }, f)

events = extract_json(sample_json)
for event in events:
    print(f"   {event}")


# ---------------------------------------------------------------------------
# 3. EXTRACT FROM SQLITE DATABASE
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. Extract from SQLite database")
print("=" * 60)


def extract_from_db(db_path, query):
    """
    Extract data by running a SQL query against a SQLite database.
    Returns a list of dictionaries.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
        cursor = conn.execute(query)
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        print(f"   ✅ Extracted {len(records)} records from {db_path}")
        return records
    except sqlite3.Error as e:
        print(f"   ❌ Database error: {e}")
        return []


# Create a sample database
db_path = "sample_extract.db"
conn = sqlite3.connect(db_path)
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, age INTEGER)")
conn.execute("INSERT INTO users VALUES (1, 'Alice', 30)")
conn.execute("INSERT INTO users VALUES (2, 'Bob', 25)")
conn.commit()
conn.close()

users = extract_from_db(db_path, "SELECT * FROM users")
for user in users:
    print(f"   {user}")


# ---------------------------------------------------------------------------
# 4. EXTRACT PATTERN: Source Registry
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. Source registry pattern")
print("=" * 60)


class DataExtractor:
    """
    A reusable extractor that handles multiple source types.
    This pattern is common in production pipelines.
    """

    def extract(self, source_type, source_path, **kwargs):
        """Route to the correct extraction method."""
        extractors = {
            "csv": self._extract_csv,
            "json": self._extract_json,
            "sqlite": self._extract_sqlite,
        }

        if source_type not in extractors:
            raise ValueError(f"Unknown source type: {source_type}")

        return extractors[source_type](source_path, **kwargs)

    def _extract_csv(self, path, **kwargs):
        return extract_csv(path)

    def _extract_json(self, path, **kwargs):
        return extract_json(path)

    def _extract_sqlite(self, path, **kwargs):
        query = kwargs.get("query", "SELECT * FROM main")
        return extract_from_db(path, query)


# Usage
extractor = DataExtractor()
csv_data = extractor.extract("csv", sample_csv)
json_data = extractor.extract("json", sample_json)
db_data = extractor.extract("sqlite", db_path, query="SELECT * FROM users")

print(f"\n   📊 Total extracted: CSV={len(csv_data)}, JSON={len(json_data)}, DB={len(db_data)}")


# ---------------------------------------------------------------------------
# CLEANUP
# ---------------------------------------------------------------------------
for f in [sample_csv, sample_json, db_path]:
    if os.path.exists(f):
        os.remove(f)

print("\n✅ Extract lesson complete!")
print("👉 Next: Run 02_transform.py")
