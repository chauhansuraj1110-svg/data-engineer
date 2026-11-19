"""
=============================================================================
 LESSON 1: File I/O — Reading and Writing Files
=============================================================================
 WHY THIS MATTERS:
   Data engineers constantly read data from files (CSVs, logs, configs)
   and write output to files. Mastering file I/O is fundamental.
=============================================================================
"""

import os

# ---------------------------------------------------------------------------
# 1. WRITING TO A FILE
# ---------------------------------------------------------------------------
# The `with` statement (context manager) automatically closes the file
# even if an error occurs. ALWAYS use this pattern.

print("=" * 60)
print("1. Writing to a file")
print("=" * 60)

# Create a sample data file
with open("sample_output.txt", "w") as f:
    f.write("Hello, Data Engineering!\n")
    f.write("This is line 2\n")
    f.write("This is line 3\n")

print("✅ File 'sample_output.txt' created successfully!")

# ---------------------------------------------------------------------------
# 2. READING A FILE — All at once
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. Reading entire file at once")
print("=" * 60)

with open("sample_output.txt", "r") as f:
    content = f.read()         # Reads the ENTIRE file into memory
    print(content)

# ⚠️  WARNING: Don't use .read() on huge files (1GB+)!
#     It loads everything into memory. Use line-by-line reading instead.

# ---------------------------------------------------------------------------
# 3. READING A FILE — Line by line (memory efficient)
# ---------------------------------------------------------------------------
print("=" * 60)
print("3. Reading line by line (best for large files)")
print("=" * 60)

with open("sample_output.txt", "r") as f:
    for line_number, line in enumerate(f, start=1):
        # .strip() removes the trailing newline character
        print(f"  Line {line_number}: {line.strip()}")

# ---------------------------------------------------------------------------
# 4. READING INTO A LIST
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. Reading all lines into a list")
print("=" * 60)

with open("sample_output.txt", "r") as f:
    lines = f.readlines()       # Returns a list of strings
    print(f"  Total lines: {len(lines)}")
    print(f"  First line: {lines[0].strip()}")

# ---------------------------------------------------------------------------
# 5. APPENDING TO A FILE
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("5. Appending to a file (mode='a')")
print("=" * 60)

with open("sample_output.txt", "a") as f:
    f.write("This line was appended!\n")

# Verify the append worked
with open("sample_output.txt", "r") as f:
    lines = f.readlines()
    print(f"  Total lines after append: {len(lines)}")
    print(f"  Last line: {lines[-1].strip()}")

# ---------------------------------------------------------------------------
# 6. WORKING WITH FILE PATHS (using os module)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("6. Working with file paths")
print("=" * 60)

# Get the current working directory
current_dir = os.getcwd()
print(f"  Current directory: {current_dir}")

# Build paths safely (works on any OS)
file_path = os.path.join(current_dir, "sample_output.txt")
print(f"  Full file path: {file_path}")

# Check if a file exists before reading
if os.path.exists("sample_output.txt"):
    file_size = os.path.getsize("sample_output.txt")
    print(f"  File exists! Size: {file_size} bytes")

# ---------------------------------------------------------------------------
# 7. USING pathlib (Modern Python — recommended!)
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("7. Using pathlib (modern approach)")
print("=" * 60)

from pathlib import Path

# pathlib provides an object-oriented approach to file paths
data_dir = Path("data_example")
data_dir.mkdir(exist_ok=True)      # Create directory if it doesn't exist

# Write a file using pathlib
output_file = data_dir / "output.txt"
output_file.write_text("Written with pathlib!\n")
print(f"  Created: {output_file}")
print(f"  Content: {output_file.read_text().strip()}")

# ---------------------------------------------------------------------------
# CLEANUP
# ---------------------------------------------------------------------------
# Remove the files we created (good practice in tutorials)
os.remove("sample_output.txt")
if output_file.exists():
    output_file.unlink()
if data_dir.exists():
    data_dir.rmdir()

print("\n✅ Lesson 1 complete! You now know how to read/write files.")
print("👉 Next: Run 02_csv_json.py to learn about data formats.")
