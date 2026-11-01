import pandas as pd
import duckdb

# =========================================================
# Task 1: Create the Parquet File
# =========================================================
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

print("=== Task 1: Parquet file created successfully ===")
print()

# =========================================================
# Task 2: Read Parquet Using DuckDB
# =========================================================
result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()

print("=== Task 2: All employee records (via DuckDB) ===")
print(result)
print()

# =========================================================
# Task 3: Filter Employee Records
# =========================================================
high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

it_department = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()

delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()

it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT' AND salary > 65000
""").df()

print("=== Task 3: Filter Employee Records ===")
print("\n1. Employees with salary > 50000:")
print(high_salary)
print("\n2. Employees from IT department:")
print(it_department)
print("\n3. Employees who work in Delhi:")
print(delhi_employees)
print("\n4. IT department employees with salary > 65000:")
print(it_high_salary)
print()

# =========================================================
# Task 4: Select Specific Columns
# =========================================================
selected_columns = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()

print("=== Task 4: name, department, salary (sorted by salary desc) ===")
print(selected_columns)
print()

# =========================================================
# Task 5: Perform Aggregations
# =========================================================
summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
""").df()

print("=== Task 5: Aggregations ===")
print(summary)
print()

# =========================================================
# Task 6: Group Data
# =========================================================
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

print("=== Task 6: Department-wise summary ===")
print(department_summary)
print()

# =========================================================
# Task 7: Create a DuckDB Table
# =========================================================
connection = duckdb.connect("company.duckdb")

connection.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT *
    FROM read_parquet('employees.parquet')
""")

table_result = connection.execute("""
    SELECT *
    FROM employees
""").df()

print("=== Task 7: employees table in company.duckdb ===")
print(table_result)
print()

connection.close()

# =========================================================
# Task 8: Export Query Results to Parquet
# =========================================================
duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("=== Task 8: Filtered Parquet file created (high_salary_employees.parquet) ===")
print()

# =========================================================
# Task 9: Verify the Exported File
# =========================================================
verify_result = duckdb.sql("""
    SELECT *
    FROM read_parquet(
        'high_salary_employees.parquet'
    )
""").df()

print("=== Task 9: Verifying high_salary_employees.parquet ===")
print(verify_result)
print()

# =========================================================
# Bonus Tasks
# =========================================================
print("=== Bonus Tasks ===")

# 1. Second-highest salary employee
second_highest = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()
print("\n1. Employee with second-highest salary:")
print(second_highest)

# 2. Top three highest-paid employees
top_three = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()
print("\n2. Top three highest-paid employees:")
print(top_three)

# 3. Average salary per city
avg_salary_city = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()
print("\n3. Average salary per city:")
print(avg_salary_city)

# 4. Departments with average salary > 55000
high_avg_departments = duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
    ORDER BY average_salary DESC
""").df()
print("\n4. Departments with average salary > 55000:")
print(high_avg_departments)

# 5. Salary category calculated column
salary_category = duckdb.sql("""
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
print("\n5. Salary category for each employee:")
print(salary_category)
