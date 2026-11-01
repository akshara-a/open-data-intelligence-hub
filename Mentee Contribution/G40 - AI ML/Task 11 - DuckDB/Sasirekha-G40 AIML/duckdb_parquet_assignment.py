# =====================================================
# DuckDB Employee Data Analysis
# =====================================================

import pandas as pd
import duckdb

# =====================================================
# Create Employee Data and Save as Parquet
# =====================================================

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

print("=" * 60)
print("Employee Parquet File Created Successfully")
print("=" * 60)

# =====================================================
# Read Employee Data
# =====================================================

print("\nEmployee Records")

result = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
""").df()

print(result)

# =====================================================
# Filter Employee Information
# =====================================================

print("\nEmployees with Salary Greater Than 50000")

high_salary = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE salary > 50000
""").df()

print(high_salary)

print("\nEmployees in IT Department")

it = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE department='IT'
""").df()

print(it)

print("\nEmployees Working in Delhi")

delhi = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE city='Delhi'
""").df()

print(delhi)

print("\nIT Employees with Salary Above 65000")

it_high = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE department='IT'
AND salary > 65000
""").df()

print(it_high)

# =====================================================
# Display Required Employee Details
# =====================================================

print("\nEmployee Details Sorted by Salary")

selected = duckdb.sql("""
SELECT
    name,
    department,
    salary
FROM read_parquet('employees.parquet')
ORDER BY salary DESC
""").df()

print(selected)

# =====================================================
# Salary Summary
# =====================================================

print("\nOverall Salary Statistics")

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

# =====================================================
# Department-wise Report
# =====================================================

print("\nDepartment-wise Employee Summary")

grouped = duckdb.sql("""
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

print(grouped)

# =====================================================
# Store Data in DuckDB Database
# =====================================================

print("\nCreating Employee Database")

connection = duckdb.connect("company.duckdb")

connection.execute("""
CREATE OR REPLACE TABLE employees AS
SELECT *
FROM read_parquet('employees.parquet')
""")

table = connection.execute("""
SELECT *
FROM employees
""").df()

print(table)

connection.close()

# =====================================================
# Export Filtered Employee Records
# =====================================================

print("\nExporting Employees with High Salary")

duckdb.sql("""
COPY
(
SELECT *
FROM read_parquet('employees.parquet')
WHERE salary > 50000
)
TO 'high_salary_employees.parquet'
(FORMAT PARQUET)
""")

print("Export completed successfully.")

# =====================================================
# Verify Exported Parquet File
# =====================================================

print("\nVerifying Exported Employee Data")

verify = duckdb.sql("""
SELECT *
FROM read_parquet('high_salary_employees.parquet')
""").df()

print(verify)

# =====================================================
# Additional SQL Analysis
# =====================================================

print("\nSecond Highest Paid Employee")

second = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
ORDER BY salary DESC
LIMIT 1 OFFSET 1
""").df()

print(second)

print("\nTop Three Highest Paid Employees")

top3 = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
ORDER BY salary DESC
LIMIT 3
""").df()

print(top3)

print("\nAverage Salary by City")

city_avg = duckdb.sql("""
SELECT
city,
AVG(salary) AS average_salary
FROM read_parquet('employees.parquet')
GROUP BY city
ORDER BY average_salary DESC
""").df()

print(city_avg)

print("\nDepartments with Average Salary Above 55000")

dept_avg = duckdb.sql("""
SELECT
department,
AVG(salary) AS average_salary
FROM read_parquet('employees.parquet')
GROUP BY department
HAVING AVG(salary) > 55000
""").df()

print(dept_avg)

print("\nEmployee Salary Categories")

category = duckdb.sql("""
SELECT
name,
salary,
CASE
WHEN salary >= 65000 THEN 'High'
WHEN salary >= 50000 THEN 'Medium'
ELSE 'Low'
END AS salary_category
FROM read_parquet('employees.parquet')
""").df()

print(category)

print("\nProgram Executed Successfully!")