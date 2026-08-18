import pandas as pd
# pyrefly: ignore [missing-import]
import duckdb
import os

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("database", exist_ok=True)

# =====================================================
# Task 1: Create Employee Data
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

df.to_parquet(
    "data/employees.parquet",
    index=False
)

print("employees.parquet created successfully.")

# =====================================================
# Task 2: Read Parquet File
# =====================================================

print("\n=== All Employees ===")

result = duckdb.sql("""
    SELECT *
    FROM read_parquet('data/employees.parquet')
""").df()

print(result)

# =====================================================
# Task 3: Filtering
# =====================================================

print("\n=== Salary > 50000 ===")

high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('data/employees.parquet')
    WHERE salary > 50000
""").df()

print(high_salary)

print("\n=== IT Department ===")

it_department = duckdb.sql("""
    SELECT *
    FROM read_parquet('data/employees.parquet')
    WHERE department = 'IT'
""").df()

print(it_department)

print("\n=== Delhi Employees ===")

delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('data/employees.parquet')
    WHERE city = 'Delhi'
""").df()

print(delhi_employees)

print("\n=== IT Department Salary > 65000 ===")

it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('data/employees.parquet')
    WHERE department = 'IT'
    AND salary > 65000
""").df()

print(it_high_salary)

# =====================================================
# Task 4: Select Columns
# =====================================================

print("\n=== Name, Department, Salary ===")

selected_columns = duckdb.sql("""
    SELECT
        name,
        department,
        salary
    FROM read_parquet('data/employees.parquet')
    ORDER BY salary DESC
""").df()

print(selected_columns)

# =====================================================
# Task 5: Aggregations
# =====================================================

print("\n=== Aggregation Results ===")

summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('data/employees.parquet')
""").df()

print(summary)

# =====================================================
# Task 6: Group By Department
# =====================================================

print("\n=== Department Summary ===")

department_summary = duckdb.sql("""
    SELECT
        department,
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS highest_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('data/employees.parquet')
    GROUP BY department
    ORDER BY average_salary DESC
""").df()

print(department_summary)

# =====================================================
# Task 7: Create DuckDB Database
# =====================================================

connection = duckdb.connect(
    "database/company.duckdb"
)

connection.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT *
    FROM read_parquet('data/employees.parquet')
""")

print("\nDuckDB table created successfully.")

employees_table = connection.execute("""
    SELECT *
    FROM employees
""").df()

print(employees_table)

# =====================================================
# Task 8: Export High Salary Employees
# =====================================================

connection.execute("""
    COPY (
        SELECT *
        FROM employees
        WHERE salary > 50000
    )
    TO 'data/high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("\nhigh_salary_employees.parquet created successfully.")

# =====================================================
# Task 9: Verify Export
# =====================================================

print("\n=== Exported File Contents ===")

exported_file = duckdb.sql("""
    SELECT *
    FROM read_parquet(
        'data/high_salary_employees.parquet'
    )
""").df()

print(exported_file)

# =====================================================
# Bonus Task 1
# =====================================================

print("\n=== Second Highest Salary Employee ===")

second_highest = duckdb.sql("""
    SELECT *
    FROM read_parquet('data/employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()

print(second_highest)

# =====================================================
# Bonus Task 2
# =====================================================

print("\n=== Top 3 Highest Paid Employees ===")

top_three = duckdb.sql("""
    SELECT *
    FROM read_parquet('data/employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()

print(top_three)

# =====================================================
# Bonus Task 3
# =====================================================

print("\n=== Average Salary By City ===")

city_average = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary
    FROM read_parquet('data/employees.parquet')
    GROUP BY city
""").df()

print(city_average)

# =====================================================
# Bonus Task 4
# =====================================================

print("\n=== Departments With Average Salary > 55000 ===")

high_avg_department = duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS average_salary
    FROM read_parquet('data/employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
""").df()

print(high_avg_department)

# =====================================================
# Bonus Task 5
# =====================================================

print("\n=== Salary Categories ===")

salary_category = duckdb.sql("""
    SELECT
        name,
        salary,
        CASE
            WHEN salary >= 65000 THEN 'High'
            WHEN salary >= 50000 THEN 'Medium'
            ELSE 'Low'
        END AS salary_category
    FROM read_parquet('data/employees.parquet')
""").df()

print(salary_category)

connection.close()

print("\nAssignment completed successfully.")