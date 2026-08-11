# DuckDB Parquet Assignment

## Objective

This project demonstrates how to query, filter, aggregate, and export **Parquet** data using **DuckDB** and Python.

## Requirements

Install the required libraries:

```bash
pip install duckdb pandas pyarrow
```

## Files Included

* `duckdb_parquet_assignment.py`
* `employees.parquet`
* `high_salary_employees.parquet`
* `company.duckdb`

## Tasks Performed

1. Create a Parquet file using Pandas.
2. Read Parquet data directly with DuckDB.
3. Filter employee records using SQL.
4. Select specific columns and sort data.
5. Perform aggregate calculations.
6. Group data by department.
7. Create a persistent DuckDB database and table.
8. Export query results to a new Parquet file.
9. Verify the exported file.
10. Execute bonus analytical queries.

## How to Run

```bash
python duckdb_parquet_assignment.py
```

## Example Queries

```sql
SELECT *
FROM read_parquet('employees.parquet')
WHERE salary > 50000;
```

## Learning Outcomes

After completing this assignment, you will be able to:

* Query Parquet files using SQL
* Perform filtering and sorting
* Calculate aggregates and grouped summaries
* Create DuckDB database tables
* Export SQL results to Parquet format
