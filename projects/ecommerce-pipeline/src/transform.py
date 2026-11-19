"""
Transform module — Clean, validate, and enrich raw data.

This is the heart of the pipeline. Raw data is messy, and this module
applies cleaning rules, validates business constraints, and adds
calculated fields.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# ==========================================================================
# CLEANING FUNCTIONS
# ==========================================================================

def clean_string(value, default=""):
    """Strip whitespace and handle None/empty values."""
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip()


def clean_name(value):
    """Standardize a name: strip and title-case."""
    cleaned = clean_string(value)
    if not cleaned:
        return None
    return cleaned.title()


def clean_email(value):
    """Standardize email: strip and lowercase."""
    cleaned = clean_string(value)
    if not cleaned:
        return None
    return cleaned.lower()


def clean_numeric(value, cast_type=float, default=None):
    """Safely convert a value to a number."""
    try:
        return cast_type(value)
    except (ValueError, TypeError):
        return default


def clean_date(value, output_format="%Y-%m-%d"):
    """Parse and standardize a date string."""
    if value is None or str(value).strip() == "":
        return None

    value = str(value).strip()
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).strftime(output_format)
        except ValueError:
            continue
    return None


# ==========================================================================
# TRANSFORM FUNCTIONS (one per source)
# ==========================================================================

def transform_customers(raw_customers):
    """
    Clean and validate customer records.

    Cleaning rules:
    - Strip whitespace from all string fields
    - Standardize names to Title Case
    - Lowercase emails
    - Fill missing first names with 'Unknown'
    """
    logger.info(f"🔄 Transforming {len(raw_customers)} customers")
    valid = []
    rejected = []

    for record in raw_customers:
        try:
            cleaned = {
                "customer_id": clean_numeric(record.get("customer_id"), int),
                "first_name": clean_name(record.get("first_name")) or "Unknown",
                "last_name": clean_name(record.get("last_name")),
                "email": clean_email(record.get("email")),
                "city": clean_string(record.get("city"), default="Unknown").title(),
                "country": clean_string(record.get("country"), default="Unknown"),
                "signup_date": clean_date(record.get("signup_date")),
            }

            # Validate required fields
            if cleaned["customer_id"] is None:
                raise ValueError("Missing customer_id")
            if cleaned["last_name"] is None:
                raise ValueError("Missing last_name")

            # Enrich: derive email domain
            if cleaned["email"] and "@" in cleaned["email"]:
                cleaned["email_domain"] = cleaned["email"].split("@")[1]
            else:
                cleaned["email_domain"] = None

            valid.append(cleaned)

        except Exception as e:
            rejected.append({"record": record, "error": str(e)})
            logger.warning(f"Rejected customer: {e}")

    logger.info(f"🔄 Customers: {len(valid)} valid, {len(rejected)} rejected")
    return valid, rejected


def transform_products(raw_products):
    """
    Clean and validate product records.

    Cleaning rules:
    - Strip whitespace from names
    - Ensure price and cost are positive numbers
    - Calculate profit margin
    """
    logger.info(f"🔄 Transforming {len(raw_products)} products")
    valid = []
    rejected = []

    for record in raw_products:
        try:
            price = clean_numeric(record.get("price"))
            cost = clean_numeric(record.get("cost_price"))

            cleaned = {
                "product_id": clean_numeric(record.get("product_id"), int),
                "product_name": clean_string(record.get("product_name")),
                "category": clean_string(record.get("category"), default="Uncategorized"),
                "price": price,
                "cost_price": cost,
            }

            # Validate
            if cleaned["product_id"] is None:
                raise ValueError("Missing product_id")
            if cleaned["price"] is None or cleaned["price"] <= 0:
                raise ValueError(f"Invalid price: {record.get('price')}")

            # Enrich: calculate profit margin
            if cleaned["cost_price"] and cleaned["cost_price"] > 0:
                cleaned["profit_margin"] = round(
                    (cleaned["price"] - cleaned["cost_price"]) / cleaned["price"] * 100, 2
                )
            else:
                cleaned["profit_margin"] = None

            valid.append(cleaned)

        except Exception as e:
            rejected.append({"record": record, "error": str(e)})
            logger.warning(f"Rejected product: {e}")

    logger.info(f"🔄 Products: {len(valid)} valid, {len(rejected)} rejected")
    return valid, rejected


def transform_orders(raw_orders, valid_customers, valid_products):
    """
    Clean, validate, and enrich order records.

    Cleaning rules:
    - Validate customer_id and product_id exist in master data
    - Parse and standardize dates
    - Calculate line totals using product prices
    """
    logger.info(f"🔄 Transforming {len(raw_orders)} orders")
    valid = []
    rejected = []

    # Build lookup dictionaries for validation
    customer_ids = {c["customer_id"] for c in valid_customers}
    product_lookup = {p["product_id"]: p for p in valid_products}

    for record in raw_orders:
        try:
            customer_id = clean_numeric(record.get("customer_id"), int)
            product_id = clean_numeric(record.get("product_id"), int)
            quantity = clean_numeric(record.get("quantity"), int, default=1)

            cleaned = {
                "order_id": clean_numeric(record.get("order_id"), int),
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "order_date": clean_date(record.get("order_date")),
                "status": clean_string(record.get("status"), default="unknown").lower(),
            }

            # Validate
            if cleaned["order_id"] is None:
                raise ValueError("Missing order_id")
            if customer_id not in customer_ids:
                raise ValueError(f"Unknown customer_id: {customer_id}")
            if product_id not in product_lookup:
                raise ValueError(f"Unknown product_id: {product_id}")

            # Enrich: calculate order total from product price
            product = product_lookup[product_id]
            cleaned["unit_price"] = product["price"]
            cleaned["line_total"] = round(product["price"] * quantity, 2)

            # Enrich: add product category for denormalized analytics
            cleaned["product_category"] = product["category"]

            valid.append(cleaned)

        except Exception as e:
            rejected.append({"record": record, "error": str(e)})
            logger.warning(f"Rejected order: {e}")

    logger.info(f"🔄 Orders: {len(valid)} valid, {len(rejected)} rejected")
    return valid, rejected


# ==========================================================================
# MAIN TRANSFORM FUNCTION
# ==========================================================================

def transform_all(raw_data):
    """
    Transform all raw data sources.

    Processing order matters! Products and customers must be
    transformed first because orders reference them.

    Args:
        raw_data: Dict with keys 'orders', 'customers', 'products'

    Returns:
        Tuple of (transformed_data, all_rejections)
    """
    logger.info("🔄 Starting transformation")

    all_rejected = {}

    # Transform in dependency order
    customers, rej_cust = transform_customers(raw_data.get("customers", []))
    all_rejected["customers"] = rej_cust

    products, rej_prod = transform_products(raw_data.get("products", []))
    all_rejected["products"] = rej_prod

    orders, rej_ord = transform_orders(
        raw_data.get("orders", []), customers, products
    )
    all_rejected["orders"] = rej_ord

    transformed = {
        "customers": customers,
        "products": products,
        "orders": orders,
    }

    total_valid = sum(len(v) for v in transformed.values())
    total_rejected = sum(len(v) for v in all_rejected.values())
    logger.info(f"🔄 Transformation complete: {total_valid} valid, {total_rejected} rejected")

    return transformed, all_rejected
