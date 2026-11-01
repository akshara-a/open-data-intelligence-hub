import pandas as pd
import duckdb

# ============================================================
# Task 1: Create the Parquet File
# ============================================================
data = {
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun", "Meera", "Karan"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance", "IT", "Sales"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000, 75000, 50000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai", "Bengaluru", "Delhi"]
}

df = pd.DataFrame(data)
df.to_parquet("employees.parquet", index=False)
print("Parquet file created successfully.\n")

# ============================================================
# Task 2: Read Parquet Using DuckDB
# ============================================================
print("=== Task 2: All Employee Records ===")
result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()
print(result)
print()

# ============================================================
# Task 3: Filter Employee Records
# ============================================================
print("=== Task 3.1: Salary > 50000 ===")
high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()
print(high_salary)
print()

print("=== Task 3.2: IT Department ===")
it_dept = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()
print(it_dept)
print()

print("=== Task 3.3: Employees in Delhi ===")
delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()
print(delhi_employees)
print()

print("=== Task 3.4: IT Department with Salary > 65000 ===")
it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT' AND salary > 65000
""").df()
print(it_high_salary)
print()

# ============================================================
# Task 4: Select Specific Columns, Sorted by Salary Descending
# ============================================================
print("=== Task 4: Name, Department, Salary (sorted desc) ===")
selected_cols = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()
print(selected_cols)
print()

# ============================================================
# Task 5: Aggregations
# ============================================================
print("=== Task 5: Aggregate Summary ===")
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
print()

# ============================================================
# Task 6: Group Data by Department
# ============================================================
print("=== Task 6: Department-wise Summary ===")
dept_summary = duckdb.sql("""
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
print(dept_summary)
print()

# ============================================================
# Task 7: Create a Persistent DuckDB Table
# ============================================================
connection = duckdb.connect("company.duckdb")

connection.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT *
    FROM read_parquet('employees.parquet')
""")

print("=== Task 7: Employees Table in company.duckdb ===")
table_result = connection.execute("""
    SELECT *
    FROM employees
""").df()
print(table_result)
print()

connection.close()

# ============================================================
# Task 8: Export Query Results to Parquet
# ============================================================
duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")
print("Task 8: Filtered Parquet file created (high_salary_employees.parquet).\n")

# ============================================================
# Task 9: Verify the Exported File
# ============================================================
print("=== Task 9: Contents of high_salary_employees.parquet ===")
verify_result = duckdb.sql("""
    SELECT *
    FROM read_parquet('high_salary_employees.parquet')
""").df()
print(verify_result)
print()

# ============================================================
# Bonus Tasks
# ============================================================
print("=== Bonus 1: Second-Highest Salary ===")
second_highest = duckdb.sql("""
    SELECT DISTINCT salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()
print(second_highest)
print()

print("=== Bonus 2: Top 3 Highest-Paid Employees ===")
top_three = duckdb.sql("""
    SELECT name, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()
print(top_three)
print()

print("=== Bonus 3: Average Salary by City ===")
avg_by_city = duckdb.sql("""
    SELECT city, AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()
print(avg_by_city)
print()

print("=== Bonus 4: Departments with Avg Salary > 55000 ===")
high_avg_depts = duckdb.sql("""
    SELECT department, AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
    ORDER BY average_salary DESC
""").df()
print(high_avg_depts)
print()

print("=== Bonus 5: Salary Category Column ===")
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
print(salary_category)