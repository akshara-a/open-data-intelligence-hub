# Apache Arrow Assignment

## Objective

Learn how to create, inspect, filter, convert, and save tabular data using Apache Arrow and Python.

## Requirements

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Dataset

| employee_id | name   | department | salary | city      |
| ----------- | ------ | ---------- | ------ | --------- |
| 1           | Asha   | IT         | 60000  | Delhi     |
| 2           | Rahul  | HR         | 45000  | Mumbai    |
| 3           | Neha   | IT         | 70000  | Bangalore |
| 4           | Vikram | Finance    | 80000  | Chennai   |
| 5           | Priya  | Marketing  | 55000  | Hyderabad |

## Tasks Performed

1. Create an Apache Arrow Table.
2. Display schema information.
3. Filter employees from the IT department.
4. Convert Arrow Table to Pandas DataFrame.
5. Save data as a Parquet file.
6. Save data as an Arrow IPC file.
7. Read and verify both files.

## Run the Program

```bash
python apache_arrow_assignment.py
```

## Output Files

* employees.parquet
* employees.arrow

## Author

Harshitha
