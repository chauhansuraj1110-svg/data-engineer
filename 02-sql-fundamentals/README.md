# Phase 2: SQL Fundamentals

## 🎯 Goal
Learn SQL — the universal language for working with data. Every data engineer
uses SQL daily to query, transform, and manage data.

## 📚 Lessons

| # | File | What You'll Learn |
|---|------|-------------------|
| 1 | `01_create_tables.sql` | DDL: CREATE, ALTER, DROP — building database schema |
| 2 | `02_crud_operations.sql` | DML: INSERT, SELECT, UPDATE, DELETE |
| 3 | `03_joins.sql` | Combining tables with JOINs |
| 4 | `04_aggregations.sql` | GROUP BY, HAVING, window functions |

## 🏃 How to Run

You can practice these SQL queries using **SQLite** (pre-installed on macOS/Linux):

```bash
# Open SQLite shell
sqlite3 practice.db

# Run a SQL file
sqlite3 practice.db < 01_create_tables.sql

# Or paste queries interactively
sqlite3 practice.db
sqlite> SELECT * FROM customers;
```

Alternatively, use an online tool like [SQLite Online](https://sqliteonline.com/).

## ✅ When You're Ready
- Complete the exercises in `exercises/README.md`
- Move on to **Phase 3: Data Modeling**

## 🔑 Key Takeaways
- SQL is declarative: you tell the database WHAT you want, not HOW to get it
- JOINs are the most important concept — master them
- Window functions are a superpower for analytics
- Always think about data types and constraints when designing tables
