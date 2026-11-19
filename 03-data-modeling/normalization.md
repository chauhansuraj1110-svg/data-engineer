# 📐 Normalization — Organizing Data to Eliminate Redundancy

## What is Normalization?
Normalization is the process of organizing a database to:
- **Eliminate data redundancy** (same data stored in multiple places)
- **Ensure data integrity** (changes in one place don't cause inconsistencies)
- **Make updates efficient** (update once, not in 50 places)

## The Quick Guide

| Normal Form | Rule | Example Problem |
|-------------|------|-----------------|
| **1NF** | No repeating groups; every cell has one value | `phones: "555-1234, 555-5678"` |
| **2NF** | 1NF + every non-key column depends on the WHOLE key | Order has customer name (only depends on customer_id) |
| **3NF** | 2NF + no column depends on another non-key column | Storing city AND zip code (city depends on zip) |

## Unnormalized Data (The "Messy Spreadsheet")

```
| order_id | customer_name | customer_email       | product_names      | prices     | order_date |
|----------|--------------|----------------------|--------------------| -----------|------------|
| 1        | Alice        | alice@mail.com       | Laptop, Mouse      | 999, 29    | 2024-01-15 |
| 2        | Alice        | alice@mail.com       | Desk Chair         | 249        | 2024-01-20 |
| 3        | Bob          | bob@mail.com         | Mouse              | 29         | 2024-01-16 |
```

Problems:
- ❌ Alice's email is stored twice (redundancy)
- ❌ Products are comma-separated in one cell (not queryable)
- ❌ If Alice changes her email, you must update multiple rows

## First Normal Form (1NF)

**Rule:** Every cell contains a single value. No repeating groups.

```
| order_id | customer_name | customer_email  | product_name | price  | order_date |
|----------|--------------|-----------------|--------------|--------|------------|
| 1        | Alice        | alice@mail.com  | Laptop       | 999.99 | 2024-01-15 |
| 1        | Alice        | alice@mail.com  | Mouse        |  29.99 | 2024-01-15 |
| 2        | Alice        | alice@mail.com  | Desk Chair   | 249.99 | 2024-01-20 |
| 3        | Bob          | bob@mail.com    | Mouse        |  29.99 | 2024-01-16 |
```

✅ Fixed: Each cell now has exactly one value
❌ Still: Customer info is repeated on every row

## Second Normal Form (2NF)

**Rule:** 1NF + every non-key column must depend on the **entire** primary key.

Separate into distinct tables:

**customers:**
```
| customer_id | name  | email          |
|-------------|-------|----------------|
| 1           | Alice | alice@mail.com |
| 2           | Bob   | bob@mail.com   |
```

**orders:**
```
| order_id | customer_id | order_date |
|----------|-------------|------------|
| 1        | 1           | 2024-01-15 |
| 2        | 1           | 2024-01-20 |
| 3        | 2           | 2024-01-16 |
```

**order_items:**
```
| order_id | product_name | price  |
|----------|-------------|--------|
| 1        | Laptop      | 999.99 |
| 1        | Mouse       |  29.99 |
| 2        | Desk Chair  | 249.99 |
| 3        | Mouse       |  29.99 |
```

✅ Fixed: Customer info stored once
❌ Still: Product info (name + price) repeated in order_items

## Third Normal Form (3NF)

**Rule:** 2NF + no non-key column depends on another non-key column.

Add a products table:

**products:**
```
| product_id | product_name | price  |
|------------|-------------|--------|
| 1          | Laptop      | 999.99 |
| 2          | Mouse       |  29.99 |
| 3          | Desk Chair  | 249.99 |
```

**order_items (updated):**
```
| order_id | product_id | quantity |
|----------|-----------|----------|
| 1        | 1         | 1        |
| 1        | 2         | 1        |
| 2        | 3         | 1        |
| 3        | 2         | 1        |
```

✅ Now fully normalized! Change a product price in ONE place.

## When to Normalize vs. Denormalize

| Scenario | Approach | Why |
|----------|----------|-----|
| Transactional database (OLTP) | **Normalize** (3NF) | Fewer updates, data integrity |
| Data warehouse (OLAP) | **Denormalize** (star schema) | Faster reads, simpler queries |
| Reporting tables | **Denormalize** | Performance over storage |
| Source systems | **Normalize** | Consistency over speed |

**Rule of thumb for data engineers:**
> Normalize your source systems. Denormalize your analytics layer.

## Summary

```
Unnormalized → 1NF → 2NF → 3NF
   (messy)     (atomic  (no partial  (no transitive
                values)  dependency)   dependency)
```

In practice, most data engineers work with data at various normalization levels:
- **Extract** from normalized OLTP systems (3NF)
- **Load** into denormalized analytical models (star schema)
- Understanding both helps you design better pipelines!
