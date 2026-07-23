# DuckDB Assignment Using Parquet

## Objective

Learn how to query, filter, aggregate, and export Parquet data using DuckDB.

## Requirements

Install DuckDB:

```bash
pip install duckdb pandas pyarrow
```

## Dataset

Create a Parquet file containing employee information with these columns:

* `employee_id`
* `name`
* `department`
* `salary`
* `city`

Use at least eight employee records.

## Task 1: Create the Parquet File

Use Python and Pandas to create a DataFrame and save it as:

```text
employees.parquet
```

Starter code:

```python
import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": [
        "Asha",
        "Rahul",
        "Neha",
        "Vikram",
        "Priya",
        "Arjun",
        "Meera",
        "Karan"
    ],
    "department": [
        "IT",
        "HR",
        "IT",
        "Finance",
        "HR",
        "Finance",
        "IT",
        "Sales"
    ],
    "salary": [
        60000,
        45000,
        70000,
        55000,
        48000,
        65000,
        75000,
        50000
    ],
    "city": [
        "Delhi",
        "Mumbai",
        "Bengaluru",
        "Delhi",
        "Mumbai",
        "Chennai",
        "Bengaluru",
        "Delhi"
    ]
}

df = pd.DataFrame(data)

df.to_parquet(
    "employees.parquet",
    index=False
)

print("Parquet file created successfully.")
```

## Task 2: Read Parquet Using DuckDB

Use DuckDB to read and display all employee records.

```python
import duckdb

result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()

print(result)
```

## Task 3: Filter Employee Records

Write DuckDB SQL queries to display:

1. Employees with a salary greater than `50000`
2. Employees from the `IT` department
3. Employees who work in `Delhi`
4. Employees from the `IT` department with a salary greater than `65000`

Example:

```python
high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

print(high_salary)
```

## Task 4: Select Specific Columns

Display only the following columns:

* `name`
* `department`
* `salary`

Sort the result by salary from highest to lowest.

```sql
SELECT name, department, salary
FROM read_parquet('employees.parquet')
ORDER BY salary DESC;
```

## Task 5: Perform Aggregations

Write queries to calculate:

1. Average salary of all employees
2. Maximum salary
3. Minimum salary
4. Total number of employees
5. Total salary paid to all employees

Example:

```python
summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
""").df()

print(summary)
```

## Task 6: Group Data

Display the following information for each department:

* Number of employees
* Average salary
* Highest salary
* Total salary

```sql
SELECT
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS average_salary,
    MAX(salary) AS highest_salary,
    SUM(salary) AS total_salary
FROM read_parquet('employees.parquet')
GROUP BY department
ORDER BY average_salary DESC;
```

## Task 7: Create a DuckDB Table

Create a persistent DuckDB database named:

```text
company.duckdb
```

Create an `employees` table using the Parquet file.

```python
import duckdb

connection = duckdb.connect("company.duckdb")

connection.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT *
    FROM read_parquet('employees.parquet')
""")

result = connection.execute("""
    SELECT *
    FROM employees
""").df()

print(result)

connection.close()
```

## Task 8: Export Query Results to Parquet

Export employees earning more than `50000` to:

```text
high_salary_employees.parquet
```

```python
import duckdb

duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("Filtered Parquet file created.")
```

## Task 9: Verify the Exported File

Read and display the contents of `high_salary_employees.parquet`.

```python
result = duckdb.sql("""
    SELECT *
    FROM read_parquet(
        'high_salary_employees.parquet'
    )
""").df()

print(result)
```

## Bonus Tasks

1. Find the employee with the second-highest salary.
2. Display the top three highest-paid employees.
3. Calculate the average salary for each city.
4. Find departments with an average salary greater than `55000`.
5. Add a calculated column named `salary_category`:

```text
High     — salary greater than or equal to 65000
Medium   — salary between 50000 and 64999
Low      — salary below 50000
```

Example:

```sql
SELECT
    name,
    salary,
    CASE
        WHEN salary >= 65000 THEN 'High'
        WHEN salary >= 50000 THEN 'Medium'
        ELSE 'Low'
    END AS salary_category
FROM read_parquet('employees.parquet');
```

## Submission Files

Submit the following files:

```text
duckdb_parquet_assignment.py
employees.parquet
high_salary_employees.parquet
company.duckdb
```

## Expected Learning Outcomes

After completing this assignment, you should be able to:

* Read Parquet files directly with DuckDB
* Run SQL queries on Parquet data
* Filter and sort records
* Perform aggregate calculations
* Group data by categories
* Create a DuckDB database table
* Export SQL query results to Parquet
