# 🚀 Data Engineering — From Zero to Hero

A hands-on, project-based learning path for aspiring data engineers.

## 📋 Prerequisites

- Python 3.10+ installed ([download](https://www.python.org/downloads/))
- A code editor (VS Code recommended)
- Basic command line familiarity
- Curiosity and patience! 🎯

## 🗺️ Learning Phases

| Phase | Topic | Estimated Time | Status |
|-------|-------|---------------|--------|
| 1 | [Python Foundations](./01-python-foundations/) | 1-2 weeks | ⬜ |
| 2 | [SQL Fundamentals](./02-sql-fundamentals/) | 1-2 weeks | ⬜ |
| 3 | [Data Modeling](./03-data-modeling/) | 1 week | ⬜ |
| 4 | [ETL Pipelines](./04-etl-pipelines/) | 1-2 weeks | ⬜ |
| 5 | [Starter Project](./projects/ecommerce-pipeline/) | 2-3 weeks | ⬜ |

## 🏁 Quick Start

```bash
# 1. Clone or navigate to this repo
cd data-engineer

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux

# 3. Install dependencies (for the starter project)
pip install -r projects/ecommerce-pipeline/requirements.txt

# 4. Start with Phase 1
cd 01-python-foundations
python 01_file_io.py
```

## 📂 Project Structure

```
data-engineer/
├── 01-python-foundations/     # Phase 1: Python for Data Engineering
├── 02-sql-fundamentals/       # Phase 2: SQL from basics to advanced
├── 03-data-modeling/          # Phase 3: Designing data warehouses
├── 04-etl-pipelines/          # Phase 4: Extract-Transform-Load patterns
├── projects/
│   └── ecommerce-pipeline/   # ⭐ Hands-on starter project
└── resources/                 # Extra learning materials & links
```

## 💡 How to Use This Repo

1. **Follow the phases in order** — each builds on the previous one
2. **Type the code yourself** — don't just copy-paste (muscle memory matters!)
3. **Do the exercises** — they reinforce what you learned
4. **Break things** — modify the code, see what happens, learn from errors
5. **Build the project** — apply everything in the starter project

## 🎯 What is Data Engineering?

Data Engineering is about building the **infrastructure and pipelines** that move, 
transform, and store data so that analysts and data scientists can use it.

```
Raw Data Sources  →  Extract  →  Transform  →  Load  →  Data Warehouse  →  Analytics
   (APIs, CSVs,       (Pull       (Clean,        (Store      (Structured,      (Dashboards,
    Databases)         data)       reshape)       it)         queryable)         ML models)
```

**Key skills you'll build:**
- 🐍 Python programming for data tasks
- 🗄️ SQL for querying and managing databases
- 📐 Data modeling (star schemas, normalization)
- 🔄 ETL/ELT pipeline design
- ✅ Data quality and testing

Happy learning! 🎓
