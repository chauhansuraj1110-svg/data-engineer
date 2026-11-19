# 📊 Post-Load Analysis Queries

After running the pipeline, use these queries to explore the loaded data.
Connect to the database with:

```bash
sqlite3 data/ecommerce.db
```

---

## 1. Overview — How much data did we load?

```sql
SELECT 'dim_customers' AS table_name, COUNT(*) AS row_count FROM dim_customers
UNION ALL
SELECT 'dim_products', COUNT(*) FROM dim_products
UNION ALL
SELECT 'fact_orders', COUNT(*) FROM fact_orders;
```

## 2. Revenue Summary

```sql
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(line_total), 2) AS total_revenue,
    ROUND(AVG(line_total), 2) AS avg_order_value,
    ROUND(MIN(line_total), 2) AS smallest_order,
    ROUND(MAX(line_total), 2) AS largest_order
FROM fact_orders;
```

## 3. Top 5 Customers by Lifetime Value

```sql
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    c.country,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.line_total), 2) AS lifetime_value
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY o.customer_id
ORDER BY lifetime_value DESC
LIMIT 5;
```

## 4. Revenue by Product Category

```sql
SELECT
    product_category,
    COUNT(*) AS num_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(line_total), 2) AS total_revenue,
    ROUND(AVG(line_total), 2) AS avg_order_value
FROM fact_orders
GROUP BY product_category
ORDER BY total_revenue DESC;
```

## 5. Monthly Revenue Trend

```sql
SELECT
    substr(order_date, 1, 7) AS month,
    COUNT(*) AS orders,
    ROUND(SUM(line_total), 2) AS revenue,
    ROUND(SUM(line_total) * 1.0 / COUNT(*), 2) AS revenue_per_order
FROM fact_orders
WHERE order_date IS NOT NULL
GROUP BY month
ORDER BY month;
```

## 6. Product Performance with Profit Margins

```sql
SELECT
    p.product_name,
    p.category,
    p.profit_margin || '%' AS margin,
    COUNT(o.order_id) AS times_ordered,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.line_total), 2) AS revenue
FROM dim_products p
LEFT JOIN fact_orders o ON p.product_id = o.product_id
GROUP BY p.product_id
ORDER BY revenue DESC;
```

## 7. Customer Geography

```sql
SELECT
    c.country,
    c.city,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(o.order_id) AS orders,
    ROUND(SUM(o.line_total), 2) AS revenue
FROM dim_customers c
LEFT JOIN fact_orders o ON c.customer_id = o.customer_id
GROUP BY c.country, c.city
ORDER BY revenue DESC;
```

## 8. Order Status Breakdown

```sql
SELECT
    status,
    COUNT(*) AS count,
    ROUND(SUM(line_total), 2) AS total_value,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_orders), 1) AS percentage
FROM fact_orders
GROUP BY status
ORDER BY count DESC;
```

## 9. Pipeline Audit Log

```sql
SELECT
    run_id,
    pipeline_name,
    started_at,
    completed_at,
    customers_loaded,
    products_loaded,
    orders_loaded,
    total_rejected,
    status
FROM pipeline_log
ORDER BY run_id DESC;
```
