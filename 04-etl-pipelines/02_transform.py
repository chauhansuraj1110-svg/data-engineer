"""
=============================================================================
 ETL LESSON 2: Transform — Cleaning and Reshaping Data
=============================================================================
 The heart of ETL. Raw data is ALWAYS messy. Your job is to:
   - Clean nulls and invalid values
   - Standardize formats (dates, currencies, names)
   - Enrich data (add calculated fields)
   - Validate data quality
=============================================================================
"""

from datetime import datetime


# ---------------------------------------------------------------------------
# 1. DATA CLEANING — Handle nulls, whitespace, types
# ---------------------------------------------------------------------------
print("=" * 60)
print("1. Data Cleaning")
print("=" * 60)

raw_records = [
    {"name": "  Alice Johnson  ", "email": "ALICE@GMAIL.COM", "amount": "150.00", "date": "2024-01-15"},
    {"name": "bob smith", "email": "", "amount": "invalid", "date": "01/20/2024"},
    {"name": None, "email": "charlie@mail.com", "amount": "210.75", "date": "2024-02-01"},
    {"name": "Diana Ross  ", "email": "diana@mail.com", "amount": "-50", "date": "2024-02-10"},
]


def clean_string(value, default="UNKNOWN"):
    """Clean a string: strip whitespace, handle nulls."""
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip()


def clean_name(value):
    """Standardize name: title case, stripped."""
    cleaned = clean_string(value)
    return cleaned.title()  # "alice johnson" → "Alice Johnson"


def clean_email(value):
    """Standardize email: lowercase, stripped."""
    cleaned = clean_string(value, default=None)
    if cleaned is None:
        return None
    return cleaned.lower()


def clean_amount(value, default=0.0):
    """Convert amount to float, reject negatives."""
    try:
        amount = float(value)
        if amount < 0:
            return default  # Reject negative amounts
        return amount
    except (ValueError, TypeError):
        return default


def clean_date(value, output_format="%Y-%m-%d"):
    """Parse dates in various formats and standardize."""
    if value is None:
        return None

    # Try common date formats
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            parsed = datetime.strptime(value.strip(), fmt)
            return parsed.strftime(output_format)
        except ValueError:
            continue

    return None  # Could not parse


# Apply cleaning to each record
print("\n   Cleaning records:")
for record in raw_records:
    cleaned = {
        "name": clean_name(record["name"]),
        "email": clean_email(record["email"]),
        "amount": clean_amount(record["amount"]),
        "date": clean_date(record["date"]),
    }
    print(f"   RAW:   {record}")
    print(f"   CLEAN: {cleaned}")
    print()


# ---------------------------------------------------------------------------
# 2. DATA VALIDATION — Ensure quality standards
# ---------------------------------------------------------------------------
print("=" * 60)
print("2. Data Validation")
print("=" * 60)


def validate_record(record):
    """
    Validate a cleaned record. Returns (is_valid, errors).
    """
    errors = []

    if record.get("name") in (None, "UNKNOWN", ""):
        errors.append("name is required")

    if record.get("email") is None:
        errors.append("email is missing")
    elif "@" not in record.get("email", ""):
        errors.append("email is invalid")

    if record.get("amount", 0) == 0:
        errors.append("amount is zero or invalid")

    if record.get("date") is None:
        errors.append("date could not be parsed")

    return len(errors) == 0, errors


# Validate sample data
sample = [
    {"name": "Alice Johnson", "email": "alice@gmail.com", "amount": 150.0, "date": "2024-01-15"},
    {"name": "UNKNOWN", "email": None, "amount": 0.0, "date": None},
    {"name": "Charlie", "email": "charlie@mail.com", "amount": 210.75, "date": "2024-02-01"},
]

valid_records = []
invalid_records = []

for record in sample:
    is_valid, errors = validate_record(record)
    if is_valid:
        valid_records.append(record)
        print(f"   ✅ {record['name']}: VALID")
    else:
        invalid_records.append({"record": record, "errors": errors})
        print(f"   ❌ {record.get('name', '?')}: {errors}")

print(f"\n   📊 Valid: {len(valid_records)}, Invalid: {len(invalid_records)}")


# ---------------------------------------------------------------------------
# 3. DATA ENRICHMENT — Add calculated fields
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. Data Enrichment")
print("=" * 60)


def enrich_record(record):
    """Add calculated/derived fields to a record."""
    enriched = record.copy()

    # Add processing metadata
    enriched["processed_at"] = datetime.now().isoformat()

    # Derive name parts
    if enriched.get("name"):
        parts = enriched["name"].split()
        enriched["first_name"] = parts[0] if len(parts) > 0 else None
        enriched["last_name"] = parts[-1] if len(parts) > 1 else None

    # Derive email domain
    if enriched.get("email") and "@" in enriched["email"]:
        enriched["email_domain"] = enriched["email"].split("@")[1]

    # Categorize amount
    amount = enriched.get("amount", 0)
    if amount >= 200:
        enriched["tier"] = "high"
    elif amount >= 100:
        enriched["tier"] = "medium"
    else:
        enriched["tier"] = "low"

    return enriched


for record in valid_records:
    enriched = enrich_record(record)
    print(f"   {enriched['name']}: tier={enriched['tier']}, domain={enriched.get('email_domain')}")


# ---------------------------------------------------------------------------
# 4. FULL TRANSFORM PIPELINE
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. Full Transform Pipeline")
print("=" * 60)


def transform(raw_records):
    """
    Complete transformation pipeline:
    1. Clean each record
    2. Validate
    3. Enrich valid records
    4. Return results with stats
    """
    cleaned = []
    valid = []
    invalid = []
    enriched = []

    # Step 1: Clean
    for record in raw_records:
        cleaned_record = {
            "name": clean_name(record.get("name")),
            "email": clean_email(record.get("email")),
            "amount": clean_amount(record.get("amount")),
            "date": clean_date(record.get("date")),
        }
        cleaned.append(cleaned_record)

    # Step 2: Validate
    for record in cleaned:
        is_valid, errors = validate_record(record)
        if is_valid:
            valid.append(record)
        else:
            invalid.append({"record": record, "errors": errors})

    # Step 3: Enrich
    for record in valid:
        enriched.append(enrich_record(record))

    # Stats
    stats = {
        "total_input": len(raw_records),
        "cleaned": len(cleaned),
        "valid": len(valid),
        "invalid": len(invalid),
        "enriched": len(enriched),
    }

    return enriched, invalid, stats


# Run it!
results, rejects, stats = transform(raw_records)

print(f"   📊 Transform Stats:")
for key, value in stats.items():
    print(f"      {key}: {value}")

print(f"\n   ✅ Output records:")
for r in results:
    print(f"      {r['name']} | {r['email']} | ${r['amount']} | tier={r['tier']}")

if rejects:
    print(f"\n   ❌ Rejected records:")
    for r in rejects:
        print(f"      {r['record'].get('name', '?')}: {r['errors']}")

print("\n✅ Transform lesson complete!")
print("👉 Next: Run 03_load.py")
