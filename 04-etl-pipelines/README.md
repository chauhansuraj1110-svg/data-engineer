# Phase 4: ETL Pipelines

## 🎯 Goal
Learn the Extract-Transform-Load pattern — the bread and butter of data engineering.
Every data pipeline follows this fundamental pattern.

## 📚 Lessons

| # | File | What You'll Learn |
|---|------|-------------------|
| 1 | `01_extract.py` | Extracting data from files, APIs, and databases |
| 2 | `02_transform.py` | Data cleaning, validation, and enrichment |
| 3 | `03_load.py` | Loading data into databases |
| 4 | `04_full_pipeline.py` | Wiring it all together into a complete pipeline |

## 🔑 ETL vs. ELT

```
ETL (Traditional):
  Source → Extract → Transform → Load → Warehouse

ELT (Modern):
  Source → Extract → Load → Transform (in warehouse)
```

- **ETL**: Transform before loading (good when compute is cheap, storage is expensive)
- **ELT**: Load raw, transform in warehouse (modern approach with cloud warehouses)

## 🏃 How to Run

```bash
# Run each lesson
python 01_extract.py
python 02_transform.py
python 03_load.py
python 04_full_pipeline.py
```

## ✅ When You're Ready
- Move on to the **Starter Project** in `projects/ecommerce-pipeline/`
- Apply everything you've learned in a real end-to-end pipeline!
