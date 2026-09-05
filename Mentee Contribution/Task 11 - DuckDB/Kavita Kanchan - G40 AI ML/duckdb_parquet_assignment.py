import os
import duckdb
import pandas as pd

# ==========================================
# Task 1: Create the Parquet File
# ==========================================
data = {
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun", "Meera", "Karan"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance", "IT", "Sales"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000, 75000, 50000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai", "Bengaluru", "Delhi"]
}

df = pd.DataFrame(data)
df.to_parquet("employees.parquet", index=False)
print("--- Task 1: employees.parquet created ---")


# ==========================================
# Task 2: Read Parquet Using DuckDB
# ==========================================
print("\n--- Task 2: Read All Employees ---")
all_employees = duckdb.sql("SELECT * FROM read_parquet('employees.parquet')").df()
print(all_employees)


# ==========================================
# Task 3: Filter Employee Records
# ==========================================
print("\n--- Task 3.1: Salary > 50000 ---")
print(duckdb.sql("SELECT * FROM read_parquet('employees.parquet') WHERE salary > 50000").df())

print("\n--- Task 3.2: IT Department ---")
print(duckdb.sql("SELECT * FROM read_parquet('employees.parquet') WHERE department = 'IT'").df())

print("\n--- Task 3.3: City is Delhi ---")
print(duckdb.sql("SELECT * FROM read_parquet('employees.parquet') WHERE city = 'Delhi'").df())

print("\n--- Task 3.4: IT Department AND Salary > 65000 ---")
print(duckdb.sql("SELECT * FROM read_parquet('employees.parquet') WHERE department = 'IT' AND salary > 65000").df())


# ==========================================
# Task 4: Select Specific Columns & Sort
# ==========================================
print("\n--- Task 4: Select Name, Department, Salary Sorted DESC ---")
print(duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df())


# ==========================================
# Task 5: Aggregations
# ==========================================
print("\n--- Task 5: Overall Aggregations ---")
print(duckdb.sql("""
    SELECT
        COUNT(*) AS total_employees,
        AVG(salary) AS avg_salary,
        MAX(salary) AS max_salary,
        MIN(salary) AS min_salary,
        SUM(salary) AS total_payroll
    FROM read_parquet('employees.parquet')
""").df())


# ==========================================
# Task 6: Group Data by Department
# ==========================================
print("\n--- Task 6: Group by Department ---")
print(duckdb.sql("""
    SELECT
        department,
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS highest_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    ORDER BY average_salary DESC
""").df())


# ==========================================
# Task 7: Create a DuckDB Table & Database
# ==========================================
print("\n--- Task 7: Persistent DuckDB Database ---")
conn = duckdb.connect("company.duckdb")

conn.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT * FROM read_parquet('employees.parquet')
""")

db_result = conn.execute("SELECT * FROM employees").df()
print(db_result)
conn.close()


# ==========================================
# Task 8: Export Query Results to Parquet
# ==========================================
print("\n--- Task 8: Export High Salary Employees ---")
duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")
print("Export complete: high_salary_employees.parquet")


# ==========================================
# Task 9: Verify the Exported File
# ==========================================
print("\n--- Task 9: Verify Exported File ---")
exported_data = duckdb.sql("SELECT * FROM read_parquet('high_salary_employees.parquet')").df()
print(exported_data)


# ==========================================
# Bonus Tasks
# ==========================================
print("\n==========================================")
print("               BONUS TASKS                ")
print("==========================================")

# Bonus 1: Second-highest salary employee
print("\n--- Bonus 1: Second-Highest Salary Employee ---")
print(duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df())

# Bonus 2: Top 3 highest-paid employees
print("\n--- Bonus 2: Top 3 Highest-Paid Employees ---")
print(duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df())

# Bonus 3: Average salary for each city
print("\n--- Bonus 3: Average Salary by City ---")
print(duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS avg_salary,
        COUNT(*) AS employee_count
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY avg_salary DESC
""").df())

# Bonus 4: Departments with average salary > 55000
print("\n--- Bonus 4: Departments with Avg Salary > 55000 ---")
print(duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS avg_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
""").df())

# Bonus 5: Categorize employees by salary tiers
print("\n--- Bonus 5: Salary Categorization ---")
print(duckdb.sql("""
    SELECT
        name,
        department,
        salary,
        CASE
            WHEN salary >= 65000 THEN 'High'
            WHEN salary >= 50000 THEN 'Medium'
            ELSE 'Low'
        END AS salary_category
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df())