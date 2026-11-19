"""
=============================================================================
 LESSON 2: CSV & JSON — The Data Formats You'll Use Every Day
=============================================================================
 WHY THIS MATTERS:
   CSV and JSON are the two most common formats for exchanging data.
   APIs return JSON. Databases export CSV. You MUST master both.
=============================================================================
"""

import csv
import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# PART A: WORKING WITH CSV FILES
# ---------------------------------------------------------------------------

print("=" * 60)
print("PART A: CSV (Comma-Separated Values)")
print("=" * 60)

# ---------------------------------------------------------------------------
# 1. WRITING CSV DATA
# ---------------------------------------------------------------------------
print("\n1. Writing CSV data")

# Sample data — imagine this came from an API or database
employees = [
    {"name": "Alice", "department": "Engineering", "salary": 95000},
    {"name": "Bob", "department": "Data", "salary": 88000},
    {"name": "Charlie", "department": "Engineering", "salary": 102000},
    {"name": "Diana", "department": "Data", "salary": 91000},
]

# Write using csv.DictWriter (recommended — handles headers automatically)
with open("employees.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "department", "salary"])
    writer.writeheader()        # Writes the header row
    writer.writerows(employees) # Writes all data rows

print("   ✅ Created employees.csv")

# ---------------------------------------------------------------------------
# 2. READING CSV DATA
# ---------------------------------------------------------------------------
print("\n2. Reading CSV data")

# Method 1: csv.DictReader (returns dictionaries — easiest to work with)
with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Each row is a dictionary: {"name": "Alice", "department": "Engineering", ...}
        print(f"   {row['name']} works in {row['department']}, earns ${row['salary']}")

# ⚠️  NOTE: csv.DictReader returns ALL values as strings!
#     You need to convert numbers manually: int(row['salary'])

# ---------------------------------------------------------------------------
# 3. FILTERING CSV DATA (a common DE task)
# ---------------------------------------------------------------------------
print("\n3. Filtering: Engineers only")

with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    engineers = [row for row in reader if row["department"] == "Engineering"]

for eng in engineers:
    print(f"   {eng['name']} — ${eng['salary']}")

print(f"   Found {len(engineers)} engineers")

# ---------------------------------------------------------------------------
# PART B: WORKING WITH JSON
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("PART B: JSON (JavaScript Object Notation)")
print("=" * 60)

# ---------------------------------------------------------------------------
# 4. WRITING JSON DATA
# ---------------------------------------------------------------------------
print("\n4. Writing JSON data")

# JSON maps perfectly to Python dicts and lists
api_response = {
    "status": "success",
    "total_records": 3,
    "data": [
        {"id": 1, "event": "page_view", "timestamp": "2024-01-15T10:30:00Z"},
        {"id": 2, "event": "purchase", "timestamp": "2024-01-15T10:31:00Z"},
        {"id": 3, "event": "page_view", "timestamp": "2024-01-15T10:32:00Z"},
    ]
}

# Write JSON to file (indent=2 makes it human-readable)
with open("events.json", "w") as f:
    json.dump(api_response, f, indent=2)

print("   ✅ Created events.json")

# ---------------------------------------------------------------------------
# 5. READING JSON DATA
# ---------------------------------------------------------------------------
print("\n5. Reading JSON data")

with open("events.json", "r") as f:
    data = json.load(f)    # Parses JSON → Python dict

print(f"   Status: {data['status']}")
print(f"   Total records: {data['total_records']}")
for event in data["data"]:
    print(f"   Event: {event['event']} at {event['timestamp']}")

# ---------------------------------------------------------------------------
# 6. JSON STRINGS (for APIs and logging)
# ---------------------------------------------------------------------------
print("\n6. JSON strings (without files)")

# Python dict → JSON string
log_entry = {"level": "INFO", "message": "Pipeline started", "step": 1}
json_string = json.dumps(log_entry)
print(f"   JSON string: {json_string}")

# JSON string → Python dict
parsed = json.loads(json_string)
print(f"   Parsed back: {parsed['message']}")

# ---------------------------------------------------------------------------
# 7. NESTED JSON (very common in real APIs)
# ---------------------------------------------------------------------------
print("\n7. Working with nested JSON")

nested_data = {
    "user": {
        "profile": {
            "name": "Alice",
            "settings": {
                "theme": "dark",
                "notifications": True
            }
        },
        "orders": [
            {"id": 101, "total": 59.99},
            {"id": 102, "total": 124.50}
        ]
    }
}

# Accessing nested values — you'll do this A LOT
user_name = nested_data["user"]["profile"]["name"]
theme = nested_data["user"]["profile"]["settings"]["theme"]
first_order = nested_data["user"]["orders"][0]["total"]

print(f"   User: {user_name}")
print(f"   Theme: {theme}")
print(f"   First order total: ${first_order}")

# Safe access with .get() (returns None instead of crashing)
email = nested_data["user"]["profile"].get("email", "not provided")
print(f"   Email: {email}")

# ---------------------------------------------------------------------------
# 8. CONVERTING BETWEEN CSV AND JSON (common pipeline task!)
# ---------------------------------------------------------------------------
print("\n8. CSV → JSON conversion")

# Read CSV and convert to list of dicts (already in JSON-friendly format)
with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    csv_data = list(reader)

# Write as JSON
with open("employees.json", "w") as f:
    json.dump(csv_data, f, indent=2)

print("   ✅ Converted employees.csv → employees.json")

# ---------------------------------------------------------------------------
# CLEANUP
# ---------------------------------------------------------------------------
for file in ["employees.csv", "events.json", "employees.json"]:
    if os.path.exists(file):
        os.remove(file)

print("\n✅ Lesson 2 complete! You can now work with CSV and JSON.")
print("👉 Next: Run 03_error_handling.py to learn about handling failures.")
