import pandas as pd
import duckdb

# -------------------------------
# Task 1: Create Employee Data
# -------------------------------

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

df.to_parquet("employees.parquet", index=False)

print("\nEmployees Parquet File Created Successfully.\n")

# -------------------------------
# Task 2: Read Parquet
# -------------------------------

print("Task 2: Read Parquet")

result = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
""").df()

print(result)

# -------------------------------
# Task 3: Filter Queries
# -------------------------------

print("\nTask 3.1 Salary > 50000")

print(
duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE salary > 50000
""").df()
)

print("\nTask 3.2 IT Department")

print(
duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE department='IT'
""").df()
)

print("\nTask 3.3 Delhi Employees")

print(
duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE city='Delhi'
""").df()
)

print("\nTask 3.4 IT Department and Salary > 65000")

print(
duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE department='IT'
AND salary>65000
""").df()
)

# -------------------------------
# Task 4
# -------------------------------

print("\nTask 4")

print(
duckdb.sql("""
SELECT
name,
department,
salary
FROM read_parquet('employees.parquet')
ORDER BY salary DESC
""").df()
)

# -------------------------------
# Task 5
# -------------------------------

print("\nTask 5")

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

# -------------------------------
# Task 6
# -------------------------------

print("\nTask 6")

group = duckdb.sql("""
SELECT
department,
COUNT(*) AS employee_count,
AVG(salary) AS average_salary,
MAX(salary) AS highest_salary,
SUM(salary) AS total_salary
FROM read_parquet('employees.parquet')
GROUP BY department
ORDER BY average_salary DESC
""").df()

print(group)

# -------------------------------
# Task 7
# -------------------------------

print("\nTask 7")

connection = duckdb.connect("company.duckdb")

connection.execute("""
CREATE OR REPLACE TABLE employees AS
SELECT *
FROM read_parquet('employees.parquet')
""")

print(
connection.execute("""
SELECT *
FROM employees
""").df()
)

connection.close()

# -------------------------------
# Task 8
# -------------------------------

print("\nTask 8")

duckdb.sql("""
COPY(
SELECT *
FROM read_parquet('employees.parquet')
WHERE salary>50000
)
TO 'high_salary_employees.parquet'
(FORMAT PARQUET)
""")

print("High Salary Parquet File Created.")

# -------------------------------
# Task 9
# -------------------------------

print("\nTask 9")

verify = duckdb.sql("""
SELECT *
FROM read_parquet('high_salary_employees.parquet')
""").df()

print(verify)

print("\nAssignment Completed Successfully.")