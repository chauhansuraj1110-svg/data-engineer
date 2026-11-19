# Phase 3: Data Modeling

## 🎯 Goal
Learn how to design databases that are optimized for analytics.
Data modeling is the bridge between raw data and useful insights.

## 📚 Lessons

| # | File | What You'll Learn |
|---|------|-------------------|
| 1 | `star_schema.md` | Fact tables, dimension tables, star schema design |
| 2 | `normalization.md` | 1NF, 2NF, 3NF — when and why to normalize |

## 🔑 Key Concepts

### OLTP vs. OLAP
- **OLTP** (Online Transaction Processing): Optimized for WRITING (e-commerce checkout)
- **OLAP** (Online Analytical Processing): Optimized for READING (business reports)
- Data engineers build pipelines from OLTP → OLAP

### The Data Warehouse Layers
```
Raw Data → Staging → Data Warehouse → Data Marts → Reports
                     (star schema)    (department-  (dashboards)
                                       specific)
```

## ✅ When You're Ready
- Understand fact vs. dimension tables
- Know when to normalize vs. denormalize
- Move on to **Phase 4: ETL Pipelines**
