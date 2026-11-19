# 🗺️ Data Engineering Learning Path

## Detailed Roadmap with Resources

### Phase 1: Python Foundations (Week 1-2)

**Topics:**
- Variables, data types, control flow
- File I/O (reading/writing CSV, JSON, text)
- Error handling (try/except, logging)
- Functions and classes
- List comprehensions, generators

**Free Resources:**
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/) — Free online book
- [Real Python](https://realpython.com/) — Excellent tutorials

---

### Phase 2: SQL Fundamentals (Week 3-4)

**Topics:**
- DDL: CREATE, ALTER, DROP
- DML: SELECT, INSERT, UPDATE, DELETE
- JOINs: INNER, LEFT, RIGHT, FULL, CROSS
- Aggregations: GROUP BY, HAVING
- Window functions: ROW_NUMBER, RANK, LAG, LEAD
- Subqueries and CTEs

**Free Resources:**
- [SQLBolt](https://sqlbolt.com/) — Interactive SQL lessons
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/)
- [LeetCode SQL Problems](https://leetcode.com/problemset/database/)
- [W3Schools SQL](https://www.w3schools.com/sql/)

---

### Phase 3: Data Modeling (Week 5)

**Topics:**
- OLTP vs OLAP systems
- Normalization (1NF, 2NF, 3NF)
- Star schema and snowflake schema
- Fact tables and dimension tables
- Slowly Changing Dimensions (SCD)

**Free Resources:**
- [Kimball Group Design Tips](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [Data Modeling Wikipedia](https://en.wikipedia.org/wiki/Dimensional_modeling)

---

### Phase 4: ETL Pipelines (Week 6-7)

**Topics:**
- Extract: reading from files, APIs, databases
- Transform: cleaning, validating, enriching data
- Load: batch inserts, upserts, idempotency
- Pipeline orchestration
- Error handling and retry logic

---

### Phase 5: Starter Project (Week 8-10)

**Apply everything in the e-commerce pipeline project!**

---

## What Comes Next? (After This Course)

### Intermediate Topics
| Topic | Tools to Learn | Why |
|-------|---------------|-----|
| Cloud Data Warehouses | BigQuery, Snowflake, Redshift | Where real data lives |
| Orchestration | Apache Airflow, Prefect, Dagster | Schedule & monitor pipelines |
| Data Quality | Great Expectations, dbt tests | Catch data issues early |
| Version Control | Git, GitHub | Collaborate & track changes |
| Containers | Docker | Reproducible environments |

### Advanced Topics
| Topic | Tools to Learn | Why |
|-------|---------------|-----|
| Streaming | Apache Kafka, Spark Streaming | Real-time data processing |
| Big Data | Apache Spark, Hadoop | Process terabytes of data |
| Infrastructure as Code | Terraform | Manage cloud resources |
| CI/CD | GitHub Actions, Jenkins | Automate testing & deployment |
| Data Governance | Apache Atlas, Datahub | Metadata management & lineage |

### Recommended Learning Order After This Course
1. **Git & GitHub** — Essential for any engineering role
2. **Docker** — Makes your pipelines reproducible
3. **Apache Airflow** — The most popular orchestration tool
4. **A cloud warehouse** — BigQuery (free tier) or Snowflake
5. **dbt** — Transform data inside the warehouse (ELT)
6. **Spark** — When your data gets really big
