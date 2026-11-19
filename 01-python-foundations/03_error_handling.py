"""
=============================================================================
 LESSON 3: Error Handling & Logging
=============================================================================
 WHY THIS MATTERS:
   Pipelines run at 2 AM. When they break, good error handling and logging
   are the difference between a 5-minute fix and a 5-hour nightmare.
=============================================================================
"""

import logging
import sys

# ---------------------------------------------------------------------------
# 1. BASIC TRY/EXCEPT
# ---------------------------------------------------------------------------
print("=" * 60)
print("1. Basic try/except")
print("=" * 60)

# Without error handling — this would CRASH your pipeline:
#   result = 10 / 0  # 💥 ZeroDivisionError

# With error handling — graceful failure:
try:
    result = 10 / 0
except ZeroDivisionError:
    print("   ⚠️  Cannot divide by zero! Using default value.")
    result = 0

print(f"   Result: {result}")

# ---------------------------------------------------------------------------
# 2. CATCHING SPECIFIC EXCEPTIONS (always be specific!)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. Catching specific exceptions")
print("=" * 60)

def parse_record(record):
    """Parse a data record — demonstrates multiple exception types."""
    try:
        name = record["name"]                # Could raise KeyError
        age = int(record["age"])             # Could raise ValueError
        salary = record["salary"] / 12       # Could raise TypeError/ZeroDivisionError
        return {"name": name, "age": age, "monthly_salary": salary}
    except KeyError as e:
        print(f"   ❌ Missing field: {e}")
        return None
    except ValueError as e:
        print(f"   ❌ Invalid value: {e}")
        return None
    except TypeError as e:
        print(f"   ❌ Wrong type: {e}")
        return None

# Test with good data
good_record = {"name": "Alice", "age": "30", "salary": 96000}
print(f"   Good record: {parse_record(good_record)}")

# Test with bad data
bad_record_1 = {"name": "Bob"}  # Missing 'age' and 'salary'
print(f"   Bad record 1: {parse_record(bad_record_1)}")

bad_record_2 = {"name": "Charlie", "age": "not_a_number", "salary": 80000}
print(f"   Bad record 2: {parse_record(bad_record_2)}")

# ---------------------------------------------------------------------------
# 3. THE FINALLY BLOCK (cleanup code that ALWAYS runs)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. The finally block")
print("=" * 60)

def process_file(filepath):
    """Demonstrates finally for cleanup."""
    f = None
    try:
        f = open(filepath, "r")
        data = f.read()
        print(f"   Read {len(data)} characters")
    except FileNotFoundError:
        print(f"   ⚠️  File '{filepath}' not found")
    finally:
        # This ALWAYS runs, even if there was an error
        if f:
            f.close()
            print("   🧹 File handle closed (cleanup done)")
        print("   ✅ Finally block executed")

process_file("nonexistent_file.txt")

# 💡 TIP: Using `with open(...)` is better because it handles cleanup
#    automatically. But `finally` is useful for other resources (DB connections, etc.)

# ---------------------------------------------------------------------------
# 4. RAISING EXCEPTIONS (validate your data!)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. Raising exceptions for validation")
print("=" * 60)

def validate_order(order):
    """Validate an order before processing — raise on bad data."""
    if not isinstance(order, dict):
        raise TypeError(f"Expected dict, got {type(order).__name__}")

    if "amount" not in order:
        raise ValueError("Order must have an 'amount' field")

    if order["amount"] < 0:
        raise ValueError(f"Order amount cannot be negative: {order['amount']}")

    print(f"   ✅ Order valid: ${order['amount']:.2f}")
    return True

# Valid order
validate_order({"amount": 49.99})

# Invalid order — caught gracefully
try:
    validate_order({"amount": -10})
except ValueError as e:
    print(f"   ❌ Validation failed: {e}")

# ---------------------------------------------------------------------------
# 5. LOGGING (professional alternative to print statements)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("5. Logging (the professional way)")
print("=" * 60)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pipeline")

# Log levels (from least to most severe):
logger.debug("This is a DEBUG message — very detailed, for development")
logger.info("Pipeline started — processing 1000 records")
logger.warning("⚠️  Found 5 records with missing email addresses")
logger.error("❌ Failed to connect to database")
logger.critical("🔥 Pipeline crashed — all retries exhausted!")

# 💡 In production, you'd configure:
#    - DEBUG level for development
#    - INFO level for production
#    - Write logs to files, not just console
#    - Use structured logging (JSON format) for log analysis tools

# ---------------------------------------------------------------------------
# 6. RETRY PATTERN (very common in data engineering)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("6. Retry pattern for unreliable operations")
print("=" * 60)

import time

def fetch_with_retry(url, max_retries=3, delay=1):
    """
    Simulate fetching data with retries.
    In real pipelines, APIs and databases can be temporarily unavailable.
    """
    for attempt in range(1, max_retries + 1):
        try:
            # Simulate: first 2 attempts fail, third succeeds
            if attempt < 3:
                raise ConnectionError(f"Connection refused (attempt {attempt})")

            print(f"   ✅ Success on attempt {attempt}!")
            return {"data": "fetched successfully"}

        except ConnectionError as e:
            print(f"   ⚠️  Attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                print(f"   ⏳ Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print("   ❌ All retries exhausted!")
                raise  # Re-raise the last exception

result = fetch_with_retry("https://api.example.com/data")
print(f"   Result: {result}")

# ---------------------------------------------------------------------------
# 7. PUTTING IT ALL TOGETHER — A robust data processing function
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("7. Putting it all together")
print("=" * 60)

def process_batch(records):
    """
    Process a batch of records with full error handling.
    This is a pattern you'll use in every pipeline.
    """
    successful = 0
    failed = 0
    errors = []

    logger.info(f"Processing batch of {len(records)} records")

    for i, record in enumerate(records):
        try:
            # Validate
            if "id" not in record:
                raise ValueError("Missing 'id' field")

            # Transform (example: ensure name is uppercase)
            record["name"] = record.get("name", "UNKNOWN").upper()

            # Count success
            successful += 1

        except Exception as e:
            failed += 1
            errors.append({"index": i, "error": str(e), "record": record})
            logger.warning(f"Record {i} failed: {e}")

    # Summary
    logger.info(f"Batch complete: {successful} succeeded, {failed} failed")

    if errors:
        logger.warning(f"Failed records: {errors}")

    return {"successful": successful, "failed": failed, "errors": errors}


# Test batch processing
test_records = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"name": "No ID Charlie"},     # Will fail — missing 'id'
    {"id": 4, "name": "Diana"},
]

result = process_batch(test_records)
print(f"\n   📊 Results: {result['successful']} OK, {result['failed']} failed")

print("\n✅ Lesson 3 complete! You now know how to handle errors like a pro.")
print("👉 Next: Run 04_functions_classes.py to learn about reusable code.")
