# 🏋️ Phase 1 Exercises

Test your Python foundations by completing these exercises.
Create a new `.py` file for each exercise.

---

## Exercise 1: Log File Analyzer
**File:** `ex1_log_analyzer.py`

Write a script that:
1. Creates a sample log file with 20+ lines (mix of INFO, WARNING, ERROR levels)
2. Reads the file and counts how many lines are INFO, WARNING, and ERROR
3. Prints a summary report
4. Writes only the ERROR lines to a new file called `errors_only.txt`

**Hint:** Use `line.startswith()` or `"ERROR" in line` for filtering.

---

## Exercise 2: CSV Data Merger
**File:** `ex2_csv_merger.py`

Write a script that:
1. Creates two CSV files:
   - `users.csv` with columns: `user_id, name, email`
   - `orders.csv` with columns: `order_id, user_id, product, amount`
2. Reads both files and "joins" them on `user_id` (combine user info with their orders)
3. Writes the merged result to `merged_report.csv`

**Hint:** Load users into a dictionary keyed by `user_id` for fast lookup.

---

## Exercise 3: JSON Config Reader
**File:** `ex3_config_reader.py`

Write a script that:
1. Creates a JSON config file for a pipeline with settings like:
   - `database_host`, `database_port`, `batch_size`, `retry_count`
2. Writes a function `load_config(filepath)` that reads the config with error handling
3. If the file doesn't exist, creates a default config
4. Validates that all required fields are present

---

## Exercise 4: Robust Data Processor
**File:** `ex4_data_processor.py`

Write a `DataProcessor` class that:
1. Takes a list of dictionaries (records)
2. Validates each record (check for required fields)
3. Cleans string fields (strip whitespace, handle nulls)
4. Converts numeric fields from strings to numbers
5. Tracks statistics: total processed, successful, failed
6. Uses logging instead of print statements
7. Has a `.process()` method and a `.report()` method

---

## 🎯 Bonus Challenge
Combine exercises 2 and 4: read CSVs, process them through your `DataProcessor`, 
and write clean output. Add retry logic for the file reading step.

## ✅ Self-Check
Before moving to Phase 2, make sure you can:
- [ ] Read and write CSV and JSON files confidently
- [ ] Handle errors without crashing
- [ ] Write functions with clear inputs/outputs
- [ ] Use a class to organize related logic
- [ ] Use logging instead of print for production code
