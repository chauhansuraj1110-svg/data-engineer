"""
=============================================================================
 LESSON 4: Functions & Classes — Writing Reusable Pipeline Code
=============================================================================
 WHY THIS MATTERS:
   Real pipelines aren't one-off scripts. You'll write code that runs daily,
   gets maintained by a team, and needs to be tested. Functions and classes
   are how you organize that code.
=============================================================================
"""

# ---------------------------------------------------------------------------
# 1. FUNCTIONS — The building blocks of pipeline code
# ---------------------------------------------------------------------------
print("=" * 60)
print("1. Functions — clean, reusable, testable")
print("=" * 60)


def clean_email(email):
    """
    Clean and validate an email address.

    Args:
        email: Raw email string from data source

    Returns:
        Cleaned email (lowercase, stripped) or None if invalid
    """
    if not email or not isinstance(email, str):
        return None

    cleaned = email.strip().lower()

    if "@" not in cleaned:
        return None

    return cleaned


# Test it
test_emails = ["  Alice@Gmail.COM  ", "invalid-email", "", "bob@company.io", None]
for email in test_emails:
    result = clean_email(email)
    print(f"   '{email}' → '{result}'")


# ---------------------------------------------------------------------------
# 2. FUNCTIONS WITH DEFAULT ARGUMENTS
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. Default arguments and keyword arguments")
print("=" * 60)


def format_currency(amount, currency="USD", decimals=2):
    """Format a number as currency string."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.{decimals}f}"


print(f"   Default:    {format_currency(1234567.89)}")
print(f"   EUR:        {format_currency(1234567.89, currency='EUR')}")
print(f"   No decimals: {format_currency(1234567.89, decimals=0)}")
print(f"   INR:        {format_currency(1234567.89, currency='INR')}")


# ---------------------------------------------------------------------------
# 3. GENERATOR FUNCTIONS (memory-efficient for large datasets)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. Generators — process millions of rows without running out of memory")
print("=" * 60)


def read_records_in_batches(records, batch_size=3):
    """
    Yield records in batches. This is how you process large files
    without loading everything into memory at once.

    This is a GENERATOR — it uses 'yield' instead of 'return'.
    """
    batch = []
    for record in records:
        batch.append(record)
        if len(batch) == batch_size:
            yield batch    # Pause here, return the batch, resume on next call
            batch = []

    # Don't forget the last partial batch!
    if batch:
        yield batch


# Simulate a large dataset
all_records = [f"record_{i}" for i in range(10)]

for batch_num, batch in enumerate(read_records_in_batches(all_records, batch_size=3), 1):
    print(f"   Batch {batch_num}: {batch}")


# ---------------------------------------------------------------------------
# 4. CLASSES — Organize related pipeline logic
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. Classes — organize your pipeline components")
print("=" * 60)


class DataCleaner:
    """
    A reusable data cleaning utility.

    In real pipelines, you'd have cleaners for different data types:
    - CustomerCleaner
    - OrderCleaner
    - ProductCleaner
    """

    def __init__(self, null_placeholder="UNKNOWN"):
        """Initialize with configuration."""
        self.null_placeholder = null_placeholder
        self.records_cleaned = 0
        self.issues_found = 0

    def clean_string(self, value):
        """Clean a string field."""
        if value is None or value == "":
            self.issues_found += 1
            return self.null_placeholder
        return str(value).strip()

    def clean_number(self, value, default=0):
        """Clean a numeric field."""
        try:
            return float(value)
        except (ValueError, TypeError):
            self.issues_found += 1
            return default

    def clean_record(self, record):
        """Clean an entire record (dictionary)."""
        cleaned = {}
        for key, value in record.items():
            if isinstance(value, (int, float)):
                cleaned[key] = self.clean_number(value)
            else:
                cleaned[key] = self.clean_string(value)

        self.records_cleaned += 1
        return cleaned

    def get_stats(self):
        """Return cleaning statistics."""
        return {
            "records_cleaned": self.records_cleaned,
            "issues_found": self.issues_found,
        }


# Use the class
cleaner = DataCleaner(null_placeholder="N/A")

dirty_records = [
    {"name": "  Alice  ", "age": 30, "city": ""},
    {"name": None, "age": "invalid", "city": "  New York "},
    {"name": "Bob", "age": 25, "city": "London"},
]

print("   Cleaning records:")
for record in dirty_records:
    cleaned = cleaner.clean_record(record)
    print(f"   {record} → {cleaned}")

print(f"\n   📊 Stats: {cleaner.get_stats()}")


# ---------------------------------------------------------------------------
# 5. DATACLASSES (Modern Python — great for data models)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("5. Dataclasses — lightweight data models")
print("=" * 60)

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PipelineResult:
    """Stores the result of a pipeline run."""
    pipeline_name: str
    records_processed: int
    records_failed: int
    start_time: datetime = field(default_factory=datetime.now)
    errors: list = field(default_factory=list)

    @property
    def success_rate(self):
        """Calculate the success rate as a percentage."""
        total = self.records_processed + self.records_failed
        if total == 0:
            return 0.0
        return (self.records_processed / total) * 100


# Create a result
result = PipelineResult(
    pipeline_name="daily_orders",
    records_processed=950,
    records_failed=50,
    errors=["Row 42: invalid date", "Row 88: negative amount"],
)

print(f"   Pipeline: {result.pipeline_name}")
print(f"   Processed: {result.records_processed}")
print(f"   Failed: {result.records_failed}")
print(f"   Success rate: {result.success_rate:.1f}%")
print(f"   Errors: {result.errors}")


# ---------------------------------------------------------------------------
# 6. PUTTING IT TOGETHER — A mini pipeline using functions & classes
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("6. Mini pipeline — functions + classes working together")
print("=" * 60)


def extract(source_data):
    """Extract: Get raw data (simulated)."""
    print(f"   📥 Extracting {len(source_data)} records...")
    return source_data


def transform(records, cleaner):
    """Transform: Clean and enrich data."""
    print(f"   🔄 Transforming {len(records)} records...")
    return [cleaner.clean_record(r) for r in records]


def load(records, destination="database"):
    """Load: Store processed data (simulated)."""
    print(f"   📤 Loading {len(records)} records to {destination}...")
    return len(records)


# Run the mini pipeline!
raw_data = [
    {"name": "  Alice  ", "amount": 100},
    {"name": "", "amount": "invalid"},
    {"name": "Charlie", "amount": 250},
]

cleaner = DataCleaner()
extracted = extract(raw_data)
transformed = transform(extracted, cleaner)
loaded_count = load(transformed)

print(f"\n   ✅ Pipeline complete! {loaded_count} records loaded.")
print(f"   📊 Cleaning stats: {cleaner.get_stats()}")


print("\n✅ Lesson 4 complete! You can now write clean, reusable pipeline code.")
print("👉 Next: Try the exercises in exercises/README.md")
print("   Then move on to Phase 2: SQL Fundamentals!")
