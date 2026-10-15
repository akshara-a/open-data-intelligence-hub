import pandas as pd
import duckdb


# ==========================================
# TASK 1: Create the Parquet File
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

df.to_parquet(
    "employees.parquet",
    index=False
)

print("Parquet file created successfully.")

# ==========================================
# TASK 2: Read Parquet Using DuckDB
# ==========================================

result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()

print("\n=== All Employee Records ===")
print(result)

# ==========================================
# TASK 3: Filter Employee Records
# ==========================================

# 1. Salary greater than 50000

high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

print("\n=== Salary Greater Than 50000 ===")
print(high_salary)


# 2. Employees from IT department

it_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()

print("\n=== IT Employees ===")
print(it_employees)


# 3. Employees from Delhi

delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()

print("\n=== Delhi Employees ===")
print(delhi_employees)


# 4. IT employees with salary greater than 65000

it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
      AND salary > 65000
""").df()

print("\n=== IT Employees with Salary Greater Than 65000 ===")
print(it_high_salary)

# ==========================================
# TASK 4: Select Specific Columns
# ==========================================

selected_columns = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()

print("\n=== Employees Sorted by Salary ===")
print(selected_columns)

# ==========================================
# TASK 5: Perform Aggregations
# ==========================================

summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
""").df()

print("\n=== Salary Summary ===")
print(summary)


# ==========================================
# TASK 6: Group Data by Department
# ==========================================

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

print("\n=== Department Summary ===")
print(department_summary)

# ==========================================
# TASK 8: Export Query Results to Parquet
# ==========================================

duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("\nhigh_salary_employees.parquet created successfully.")

# ==========================================
# TASK 9: Verify Exported File
# ==========================================

exported_result = duckdb.sql("""
    SELECT *
    FROM read_parquet('high_salary_employees.parquet')
""").df()

print("\n=== High Salary Employees from Exported File ===")
print(exported_result)

# ==========================================
# BONUS 1: Second Highest Salary
# ==========================================

second_highest = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()

print("\n=== Second Highest Paid Employee ===")
print(second_highest)

# ==========================================
# BONUS 2: Top 3 Highest Paid Employees
# ==========================================

top_three = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()

print("\n=== Top 3 Highest Paid Employees ===")
print(top_three)

# ==========================================
# BONUS 3: Average Salary by City
# ==========================================

city_salary = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()

print("\n=== Average Salary by City ===")
print(city_salary)
# ==========================================
# BONUS 4: Departments with Average Salary > 55000
# ==========================================

high_average_departments = duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
""").df()

print("\n=== Departments with Average Salary > 55000 ===")
print(high_average_departments)
# ==========================================
# BONUS 5: Salary Category
# ==========================================

salary_categories = duckdb.sql("""
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

print("\n=== Salary Categories ===")
print(salary_categories)