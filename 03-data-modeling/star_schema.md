# ⭐ Star Schema — The Foundation of Data Warehousing

## What is a Star Schema?
A star schema organizes data into two types of tables:
- **Fact tables** — Store measurable events (sales, clicks, transactions)
- **Dimension tables** — Store descriptive context (who, what, when, where)

When you draw the relationships, it looks like a star ⭐ — the fact table
in the center, with dimensions radiating outward.

## Visual Diagram

```
                    ┌──────────────┐
                    │  dim_date    │
                    │──────────────│
                    │ date_key     │
                    │ full_date    │
                    │ day_of_week  │
                    │ month        │
                    │ quarter      │
                    │ year         │
                    └──────┬───────┘
                           │
  ┌──────────────┐   ┌─────┴──────────┐   ┌──────────────┐
  │ dim_customer │   │  fact_orders   │   │ dim_product  │
  │──────────────│   │────────────────│   │──────────────│
  │ customer_key │◄──│ customer_key   │──►│ product_key  │
  │ name         │   │ product_key    │   │ product_name │
  │ email        │   │ date_key       │   │ category     │
  │ city         │   │ quantity       │   │ price        │
  │ segment      │   │ unit_price     │   │ brand        │
  └──────────────┘   │ total_amount   │   └──────────────┘
                     │ discount       │
                     └────────────────┘
```

## Fact Tables — "What Happened?"

Fact tables store **measurable business events**:

| Property | Description |
|----------|-------------|
| **Grain** | The most atomic level of detail (e.g., one line item per order) |
| **Measures** | Numeric values you aggregate (quantity, amount, duration) |
| **Foreign Keys** | Links to dimension tables |
| **Typically** | Very large (millions/billions of rows), narrow (few columns) |

```sql
CREATE TABLE fact_orders (
    order_key       INTEGER PRIMARY KEY,
    -- Foreign keys to dimensions
    customer_key    INTEGER REFERENCES dim_customer(customer_key),
    product_key     INTEGER REFERENCES dim_product(product_key),
    date_key        INTEGER REFERENCES dim_date(date_key),
    -- Measures (things you SUM, AVG, COUNT)
    quantity        INTEGER,
    unit_price      REAL,
    total_amount    REAL,
    discount        REAL
);
```

## Dimension Tables — "Who / What / When / Where?"

Dimension tables provide **context** for the facts:

| Property | Description |
|----------|-------------|
| **Attributes** | Descriptive fields (name, category, region) |
| **Hierarchy** | Natural levels (city → state → country) |
| **Typically** | Small (thousands of rows), wide (many columns) |

```sql
CREATE TABLE dim_customer (
    customer_key    INTEGER PRIMARY KEY,
    customer_id     TEXT,        -- Original source system ID
    first_name      TEXT,
    last_name       TEXT,
    email           TEXT,
    city            TEXT,
    state           TEXT,
    country         TEXT,
    segment         TEXT         -- 'Premium', 'Regular', 'New'
);

CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,  -- e.g., 20240115
    full_date       TEXT,                 -- '2024-01-15'
    day_of_week     TEXT,                 -- 'Monday'
    day_of_month    INTEGER,              -- 15
    month           INTEGER,              -- 1
    month_name      TEXT,                 -- 'January'
    quarter         INTEGER,              -- 1
    year            INTEGER,              -- 2024
    is_weekend      INTEGER               -- 0 or 1
);
```

## Why Star Schema?

1. **Fast queries** — JOINs are simple (fact → dimension, never dimension → dimension)
2. **Easy to understand** — Business users can read it
3. **Aggregation friendly** — SUM/COUNT/AVG on fact measures, GROUP BY on dimensions
4. **Standard** — Every BI tool (Tableau, Power BI, Looker) expects this structure

## Example Query on Star Schema

```sql
-- "Total revenue by product category, by month, for premium customers"
SELECT
    d.month_name,
    p.category,
    SUM(f.total_amount) AS total_revenue,
    COUNT(*) AS num_orders
FROM fact_orders f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE c.segment = 'Premium'
  AND d.year = 2024
GROUP BY d.month_name, p.category
ORDER BY total_revenue DESC;
```

## Star Schema vs. Snowflake Schema

| Feature | Star Schema | Snowflake Schema |
|---------|-------------|------------------|
| Dimensions | Denormalized (flat) | Normalized (sub-tables) |
| Joins needed | Fewer | More |
| Query speed | Faster | Slower |
| Storage | More (some redundancy) | Less |
| Complexity | Simpler | More complex |
| **Best for** | **Most analytics** | Very large dimensions |

**Start with star schema.** Only snowflake if you have a specific reason.

## Design Tips

1. **Define the grain first** — "one row = one ___"
2. **Identify dimensions** — Who, what, when, where, how?
3. **Identify measures** — What numbers do you want to aggregate?
4. **Use surrogate keys** — Auto-increment integers, not source system IDs
5. **Build a date dimension** — ALWAYS. Include day, week, month, quarter, year.
