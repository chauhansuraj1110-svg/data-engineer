"""
Unit tests for the transform module.

Run with:
    python -m pytest tests/test_transform.py -v
"""

import pytest
from src.transform import (
    clean_string,
    clean_name,
    clean_email,
    clean_numeric,
    clean_date,
    transform_customers,
    transform_products,
    transform_orders,
)


# ==========================================================================
# TESTS FOR CLEANING FUNCTIONS
# ==========================================================================

class TestCleanString:
    def test_strips_whitespace(self):
        assert clean_string("  hello  ") == "hello"

    def test_handles_none(self):
        assert clean_string(None, default="N/A") == "N/A"

    def test_handles_empty_string(self):
        assert clean_string("", default="N/A") == "N/A"

    def test_handles_normal_string(self):
        assert clean_string("hello") == "hello"


class TestCleanName:
    def test_title_cases(self):
        assert clean_name("alice johnson") == "Alice Johnson"

    def test_strips_whitespace(self):
        assert clean_name("  bob  ") == "Bob"

    def test_handles_none(self):
        assert clean_name(None) is None

    def test_handles_empty(self):
        assert clean_name("") is None

    def test_handles_uppercase(self):
        assert clean_name("ALICE JOHNSON") == "Alice Johnson"


class TestCleanEmail:
    def test_lowercases(self):
        assert clean_email("ALICE@GMAIL.COM") == "alice@gmail.com"

    def test_strips_whitespace(self):
        assert clean_email("  bob@mail.com  ") == "bob@mail.com"

    def test_handles_none(self):
        assert clean_email(None) is None

    def test_handles_empty(self):
        assert clean_email("") is None


class TestCleanNumeric:
    def test_converts_string_to_float(self):
        assert clean_numeric("42.5") == 42.5

    def test_converts_string_to_int(self):
        assert clean_numeric("42", cast_type=int) == 42

    def test_handles_invalid(self):
        assert clean_numeric("abc", default=0) == 0

    def test_handles_none(self):
        assert clean_numeric(None, default=0) == 0


class TestCleanDate:
    def test_standard_format(self):
        assert clean_date("2024-01-15") == "2024-01-15"

    def test_us_format(self):
        assert clean_date("01/15/2024") == "2024-01-15"

    def test_handles_whitespace(self):
        assert clean_date(" 2024-01-15 ") == "2024-01-15"

    def test_handles_none(self):
        assert clean_date(None) is None

    def test_handles_empty(self):
        assert clean_date("") is None

    def test_handles_invalid(self):
        assert clean_date("not-a-date") is None


# ==========================================================================
# TESTS FOR TRANSFORM FUNCTIONS
# ==========================================================================

class TestTransformCustomers:
    def test_valid_customer(self):
        raw = [{"customer_id": "1", "first_name": "Alice", "last_name": "Johnson",
                "email": "alice@gmail.com", "city": "New York", "country": "USA",
                "signup_date": "2024-01-15"}]
        valid, rejected = transform_customers(raw)
        assert len(valid) == 1
        assert len(rejected) == 0
        assert valid[0]["first_name"] == "Alice"

    def test_missing_last_name_rejected(self):
        raw = [{"customer_id": "1", "first_name": "Alice", "last_name": "",
                "email": "alice@gmail.com", "city": "NYC", "country": "USA",
                "signup_date": "2024-01-15"}]
        valid, rejected = transform_customers(raw)
        assert len(valid) == 0
        assert len(rejected) == 1

    def test_email_lowercased(self):
        raw = [{"customer_id": "1", "first_name": "Alice", "last_name": "J",
                "email": "ALICE@GMAIL.COM", "city": "NYC", "country": "USA",
                "signup_date": "2024-01-15"}]
        valid, _ = transform_customers(raw)
        assert valid[0]["email"] == "alice@gmail.com"

    def test_email_domain_extracted(self):
        raw = [{"customer_id": "1", "first_name": "Alice", "last_name": "J",
                "email": "alice@gmail.com", "city": "NYC", "country": "USA",
                "signup_date": "2024-01-15"}]
        valid, _ = transform_customers(raw)
        assert valid[0]["email_domain"] == "gmail.com"


class TestTransformProducts:
    def test_valid_product(self):
        raw = [{"product_id": "101", "product_name": "Laptop", "category": "Electronics",
                "price": "999.99", "cost_price": "500.00"}]
        valid, rejected = transform_products(raw)
        assert len(valid) == 1
        assert valid[0]["price"] == 999.99

    def test_profit_margin_calculated(self):
        raw = [{"product_id": "101", "product_name": "Laptop", "category": "Electronics",
                "price": "100", "cost_price": "60"}]
        valid, _ = transform_products(raw)
        assert valid[0]["profit_margin"] == 40.0  # (100-60)/100 * 100

    def test_invalid_price_rejected(self):
        raw = [{"product_id": "101", "product_name": "Laptop", "category": "Electronics",
                "price": "invalid", "cost_price": "500"}]
        valid, rejected = transform_products(raw)
        assert len(valid) == 0
        assert len(rejected) == 1


class TestTransformOrders:
    def test_valid_order(self):
        customers = [{"customer_id": 1}]
        products = [{"product_id": 101, "price": 999.99, "category": "Electronics"}]
        raw = [{"order_id": "1001", "customer_id": "1", "product_id": "101",
                "quantity": "2", "order_date": "2024-01-15", "status": "completed"}]
        valid, rejected = transform_orders(raw, customers, products)
        assert len(valid) == 1
        assert valid[0]["line_total"] == 1999.98  # 999.99 * 2

    def test_unknown_customer_rejected(self):
        customers = [{"customer_id": 1}]
        products = [{"product_id": 101, "price": 999.99, "category": "Electronics"}]
        raw = [{"order_id": "1001", "customer_id": "999", "product_id": "101",
                "quantity": "1", "order_date": "2024-01-15", "status": "completed"}]
        valid, rejected = transform_orders(raw, customers, products)
        assert len(valid) == 0
        assert len(rejected) == 1
