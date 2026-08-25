import pandas as pd
import duckdb

# ==========================================
# Task 1: Create Employee Data
# ==========================================

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

print("=" * 60)
print("Employee Data")
print("=" * 60)
print(df)

# ==========================================
# Save as Parquet
# ==========================================

df.to_parquet(
    "employees.parquet",
    index=False
)

print("\nemployees.parquet created successfully.")

# ==========================================
# Task 2: Read Parquet Using DuckDB
# ==========================================

result = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
""").df()

print("\nAll Employees")
print(result)

# ==========================================
# Task 3: Filter Employee Records
# ==========================================

print("\nEmployees with Salary > 50000")

high_salary = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE salary > 50000
""").df()

print(high_salary)

print("\nEmployees from IT Department")

it_department = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE department='IT'
""").df()

print(it_department)

print("\nEmployees from Delhi")

delhi = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE city='Delhi'
""").df()

print(delhi)

print("\nIT Employees with Salary > 65000")

it_high = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
WHERE department='IT'
AND salary>65000
""").df()

print(it_high)

# ==========================================
# Task 4: Select Columns
# ==========================================

print("\nSelected Columns")

selected = duckdb.sql("""
SELECT
name,
department,
salary
FROM read_parquet('employees.parquet')
ORDER BY salary DESC
""").df()

print(selected)

# ==========================================
# Task 5: Aggregations
# ==========================================

print("\nSummary Statistics")

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

# ==========================================
# Task 6: Group By Department
# ==========================================

print("\nDepartment Summary")

department_summary = duckdb.sql("""
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

print(department_summary)

# ==========================================
# Task 7: Create DuckDB Database
# ==========================================

connection = duckdb.connect("company.duckdb")

connection.execute("""
CREATE OR REPLACE TABLE employees AS
SELECT *
FROM read_parquet('employees.parquet')
""")

print("\nEmployees Table Created")

employees_table = connection.execute("""
SELECT *
FROM employees
""").df()

print(employees_table)

connection.close()

# ==========================================
# Task 8: Export High Salary Employees
# ==========================================

duckdb.sql("""
COPY (
SELECT *
FROM read_parquet('employees.parquet')
WHERE salary>50000
)
TO 'high_salary_employees.parquet'
(FORMAT PARQUET)
""")

print("\nhigh_salary_employees.parquet created successfully.")

# ==========================================
# Task 9: Verify Export
# ==========================================

verify = duckdb.sql("""
SELECT *
FROM read_parquet('high_salary_employees.parquet')
""").df()

print("\nVerified Exported File")
print(verify)

# ==========================================
# Bonus Task 1
# ==========================================

print("\nSecond Highest Salary")

second_highest = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
ORDER BY salary DESC
LIMIT 1 OFFSET 1
""").df()

print(second_highest)

# ==========================================
# Bonus Task 2
# ==========================================

print("\nTop 3 Highest Paid Employees")

top3 = duckdb.sql("""
SELECT *
FROM read_parquet('employees.parquet')
ORDER BY salary DESC
LIMIT 3
""").df()

print(top3)

# ==========================================
# Bonus Task 3
# ==========================================

print("\nAverage Salary by City")

city_avg = duckdb.sql("""
SELECT
city,
AVG(salary) AS average_salary
FROM read_parquet('employees.parquet')
GROUP BY city
""").df()

print(city_avg)

# ==========================================
# Bonus Task 4
# ==========================================

print("\nDepartments with Average Salary > 55000")

dept_avg = duckdb.sql("""
SELECT
department,
AVG(salary) AS average_salary
FROM read_parquet('employees.parquet')
GROUP BY department
HAVING AVG(salary)>55000
""").df()

print(dept_avg)

# ==========================================
# Bonus Task 5
# ==========================================

print("\nSalary Category")

salary_category = duckdb.sql("""
SELECT
name,
salary,
CASE
WHEN salary>=65000 THEN 'High'
WHEN salary>=50000 THEN 'Medium'
ELSE 'Low'
END AS salary_category
FROM read_parquet('employees.parquet')
""").df()

print(salary_category)

print("\nAssignment Completed Successfully.")