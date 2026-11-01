import pandas as pd
import duckdb

# -----------------------------
# Create Employee Data
# -----------------------------
employees = pd.DataFrame({
    "Employee_ID": [101, 102, 103, 104, 105, 106, 107, 108],
    "Name": ["Rahul", "Priya", "Amit", "Sneha", "Arjun", "Neha", "Kiran", "Divya"],
    "Department": ["IT", "HR", "Finance", "IT", "Marketing", "IT", "Finance", "HR"],
    "City": ["Delhi", "Mumbai", "Delhi", "Chennai", "Delhi", "Delhi", "Hyderabad", "Delhi"],
    "Salary": [70000, 45000, 60000, 80000, 55000, 90000, 50000, 65000]
})

print("\nOriginal Employee Data:\n")
print(employees)

# -----------------------------
# Save DataFrame as Parquet
# -----------------------------
employees.to_parquet("employees.parquet", index=False)
print("\nemployees.parquet created successfully!")

# -----------------------------
# Connect DuckDB
# -----------------------------
con = duckdb.connect("company.duckdb")

# Read Parquet
con.execute("""
CREATE OR REPLACE TABLE employees AS
SELECT * FROM 'employees.parquet'
""")

# -----------------------------
# Queries
# -----------------------------

print("\nEmployees with Salary > 50000:\n")
print(con.execute("""
SELECT * FROM employees
WHERE Salary > 50000
""").fetchdf())

print("\nIT Department Employees:\n")
print(con.execute("""
SELECT * FROM employees
WHERE Department='IT'
""").fetchdf())

print("\nEmployees from Delhi:\n")
print(con.execute("""
SELECT * FROM employees
WHERE City='Delhi'
""").fetchdf())

print("\nIT Employees with Salary > 65000:\n")
print(con.execute("""
SELECT * FROM employees
WHERE Department='IT' AND Salary > 65000
""").fetchdf())

print("\nName, Department and Salary:\n")
print(con.execute("""
SELECT Name, Department, Salary
FROM employees
""").fetchdf())

print("\nEmployees Sorted by Salary (Highest First):\n")
print(con.execute("""
SELECT *
FROM employees
ORDER BY Salary DESC
""").fetchdf())

print("\nSalary Statistics:\n")
print(con.execute("""
SELECT
AVG(Salary) AS Average_Salary,
MAX(Salary) AS Maximum_Salary,
MIN(Salary) AS Minimum_Salary
FROM employees
""").fetchdf())

print("\nEmployee Count & Total Salary:\n")
print(con.execute("""
SELECT
COUNT(*) AS Total_Employees,
SUM(Salary) AS Total_Salary
FROM employees
""").fetchdf())

print("\nDepartment Wise Salary Summary:\n")
print(con.execute("""
SELECT
Department,
COUNT(*) AS Employee_Count,
SUM(Salary) AS Total_Salary,
AVG(Salary) AS Average_Salary
FROM employees
GROUP BY Department
""").fetchdf())

# -----------------------------
# Export High Salary Employees
# -----------------------------
con.execute("""
COPY (
SELECT *
FROM employees
WHERE Salary > 60000
)
TO 'high_salary_employees.parquet'
(FORMAT PARQUET)
""")

print("\nhigh_salary_employees.parquet created successfully!")

print("\nVerifying Exported File:\n")
print(con.execute("""
SELECT *
FROM 'high_salary_employees.parquet'
""").fetchdf())

con.close()

print("\nTask 11 Completed Successfully!")