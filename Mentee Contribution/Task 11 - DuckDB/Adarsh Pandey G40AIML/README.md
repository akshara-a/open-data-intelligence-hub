# DuckDB + Parquet Assignment (Simple Version)

A small project that shows how DuckDB and Parquet work together.

## What it does

1. Creates a database file `company.duckdb` with an `employees` table
2. Saves that table to `employees.parquet`
3. Reads the Parquet file back and filters employees earning > 90,000
4. Saves the filtered result to `high_salary_employees.parquet`

## How to run

```bash
pip install duckdb
python duckdb_parquet_assignment.py
```

That's it. After running, you'll have 3 new files in the folder:
- `company.duckdb`
- `employees.parquet`
- `high_salary_employees.parquet`
