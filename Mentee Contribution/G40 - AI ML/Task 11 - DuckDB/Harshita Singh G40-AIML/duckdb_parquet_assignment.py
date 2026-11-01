import pandas as pd
import duckdb

# ---------------------------------------------------------------------------
# Task 1: Create the Parquet File
# ---------------------------------------------------------------------------
data = {
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": [
        "Asha", "Rahul", "Neha", "Vikram",
        "Priya", "Arjun", "Meera", "Karan"
    ],
    "department": [
        "IT", "HR", "IT", "Finance",
        "HR", "Finance", "IT", "Sales"
    ],
    "salary": [
        60000, 45000, 70000, 55000,
        48000, 65000, 75000, 50000
    ],
    "city": [
        "Delhi", "Mumbai", "Bengaluru", "Delhi",
        "Mumbai", "Chennai", "Bengaluru", "Delhi"
    ]
}

df = pd.DataFrame(data)
df.to_parquet("employees.parquet", index=False)
print("Parquet file created successfully.\n")

# ---------------------------------------------------------------------------
# Task 2: Read Parquet Using DuckDB
# ---------------------------------------------------------------------------
print("=== Task 2: All employee records ===")
result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()
print(result, "\n")

# ---------------------------------------------------------------------------
# Task 3: Filter Employee Records
# ---------------------------------------------------------------------------
print("=== Task 3.1: Salary greater than 50000 ===")
high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()
print(high_salary, "\n")

print("=== Task 3.2: IT department employees ===")
it_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()
print(it_employees, "\n")

print("=== Task 3.3: Employees in Delhi ===")
delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()
print(delhi_employees, "\n")

print("=== Task 3.4: IT department with salary greater than 65000 ===")
it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT' AND salary > 65000
""").df()
print(it_high_salary, "\n")

# ---------------------------------------------------------------------------
# Task 4: Select Specific Columns
# ---------------------------------------------------------------------------
print("=== Task 4: name, department, salary sorted by salary DESC ===")
selected_columns = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()
print(selected_columns, "\n")

# ---------------------------------------------------------------------------
# Task 5: Perform Aggregations
# ---------------------------------------------------------------------------
print("=== Task 5: Aggregations ===")
summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
""").df()
print(summary, "\n")

# ---------------------------------------------------------------------------
# Task 6: Group Data
# ---------------------------------------------------------------------------
print("=== Task 6: Department-wise summary ===")
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
print(department_summary, "\n")

# ---------------------------------------------------------------------------
# Task 7: Create a DuckDB Table
# ---------------------------------------------------------------------------
print("=== Task 7: Persistent DuckDB table ===")
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
print(table_result, "\n")

connection.close()

# ---------------------------------------------------------------------------
# Task 8: Export Query Results to Parquet
# ---------------------------------------------------------------------------
duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")
print("Filtered Parquet file created.\n")

# ---------------------------------------------------------------------------
# Task 9: Verify the Exported File
# ---------------------------------------------------------------------------
print("=== Task 9: Verify high_salary_employees.parquet ===")
verify_result = duckdb.sql("""
    SELECT *
    FROM read_parquet('high_salary_employees.parquet')
""").df()
print(verify_result, "\n")

# ---------------------------------------------------------------------------
# Bonus Tasks
# ---------------------------------------------------------------------------
print("=== Bonus 1: Second-highest salary employee ===")
second_highest = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()
print(second_highest, "\n")

print("=== Bonus 2: Top 3 highest-paid employees ===")
top_three = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()
print(top_three, "\n")

print("=== Bonus 3: Average salary by city ===")
avg_by_city = duckdb.sql("""
    SELECT city, AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()
print(avg_by_city, "\n")

print("=== Bonus 4: Departments with average salary > 55000 ===")
dept_above_avg = duckdb.sql("""
    SELECT department, AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
    ORDER BY average_salary DESC
""").df()
print(dept_above_avg, "\n")

print("=== Bonus 5: Salary category column ===")
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
