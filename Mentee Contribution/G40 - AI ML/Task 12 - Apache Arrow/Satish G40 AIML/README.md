# Apache Arrow Assignment

## Objective

This project demonstrates how to create, inspect, filter, convert, and save tabular data using **Apache Arrow (PyArrow)** and Python.

## Requirements

Install the required libraries:

```bash
pip install pyarrow pandas
```

## Files Included

* `apache_arrow_assignment.py`
* `employees.parquet`
* `employees.arrow`
* `it_employees.parquet` (bonus task)

## Tasks Performed

1. Create an Arrow table from employee data.
2. Display the schema and inspect table metadata.
3. Select specific columns.
4. Filter records by salary and department.
5. Perform aggregate calculations.
6. Add a computed `bonus` column.
7. Convert Arrow tables to Pandas DataFrames.
8. Convert Pandas DataFrames back to Arrow tables.
9. Save data as a Parquet file.
10. Read the Parquet file using PyArrow.
11. Save data as an Arrow IPC (`.arrow`) file.
12. Read the Arrow IPC file.
13. Execute bonus filtering and sorting tasks.

## How to Run

```bash
python apache_arrow_assignment.py
```

## Learning Outcomes

After completing this assignment, you will be able to:

* Create and inspect Apache Arrow tables
* Use Arrow Compute functions for filtering and aggregation
* Convert between Arrow and Pandas
* Read and write Parquet files
* Read and write Arrow IPC files
