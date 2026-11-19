"""
Extract module — Read data from CSV source files.
"""

import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_csv(filepath):
    """
    Extract all records from a CSV file.

    Args:
        filepath: Path to the CSV file.

    Returns:
        List of dictionaries, one per row.

    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Source file not found: {filepath}")

    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    logger.info(f"Extracted {len(records)} records from {filepath.name}")
    return records


def extract_all(data_dir):
    """
    Extract data from all source CSV files.

    Args:
        data_dir: Path to the directory containing raw CSV files.

    Returns:
        Dictionary with keys 'orders', 'customers', 'products',
        each containing a list of record dictionaries.
    """
    data_dir = Path(data_dir)
    logger.info(f"📥 Starting extraction from {data_dir}")

    sources = {
        "orders": data_dir / "orders.csv",
        "customers": data_dir / "customers.csv",
        "products": data_dir / "products.csv",
    }

    extracted = {}
    for name, filepath in sources.items():
        try:
            extracted[name] = extract_csv(filepath)
        except FileNotFoundError as e:
            logger.error(f"❌ {e}")
            extracted[name] = []

    total = sum(len(v) for v in extracted.values())
    logger.info(f"📥 Extraction complete: {total} total records")
    return extracted
