# ⭐ E-Commerce ETL Pipeline — Starter Project

## 🎯 Overview
Build a complete data pipeline that processes e-commerce data:

```
CSV Files (raw) → Extract → Transform → Load → SQLite (analytics-ready)
```

This project ties together everything from Phases 1-4.

## 📂 Project Structure
```
ecommerce-pipeline/
├── data/raw/               # Source CSV files (provided)
│   ├── orders.csv
│   ├── customers.csv
│   └── products.csv
├── src/                    # Pipeline source code
│   ├── extract.py          # Read from CSV files
│   ├── transform.py        # Clean, validate, enrich
│   ├── load.py             # Write to SQLite
│   ├── models.py           # Database schema definitions
│   └── pipeline.py         # Orchestrate the full ETL
├── tests/                  # Unit tests
│   └── test_transform.py
└── notebooks/
    └── analysis.md         # Post-load analysis queries
```

## 🏁 Quick Start

```bash
# 1. Navigate to the project
cd projects/ecommerce-pipeline

# 2. Create virtual environment (if you haven't already)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the pipeline!
python -m src.pipeline

# 5. Run tests
python -m pytest tests/ -v
```

## 📊 What the Pipeline Does

### Extract
- Reads `orders.csv`, `customers.csv`, `products.csv`
- Returns raw data as lists of dictionaries

### Transform
- **Cleans**: strips whitespace, handles nulls, standardizes dates
- **Validates**: checks required fields, data types, business rules
- **Enriches**: calculates order totals, customer lifetime value, product categories

### Load
- Creates a star schema in SQLite (fact + dimension tables)
- Loads transformed data with proper foreign key relationships
- Logs the pipeline run for auditing

## 🎓 Learning Goals
By completing this project, you'll be able to:
- [ ] Read data from multiple CSV files
- [ ] Clean messy real-world data
- [ ] Design a star schema database
- [ ] Write a complete ETL pipeline
- [ ] Test your transformation logic
- [ ] Query the results for insights

## 🚀 Extensions (After you finish)
1. Add error handling for corrupt CSV files
2. Add a `data/processed/` output with cleaned CSVs
3. Build a simple report using the loaded data
4. Add command-line arguments (choose source files, database path)
5. Schedule the pipeline to run automatically with `cron`
