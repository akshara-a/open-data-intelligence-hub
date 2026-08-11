import pandas as pd
import duckdb

# ============================================================
# Task 1: Create the Parquet File
# ============================================================

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
# ============================================================
# Task 2: Read Parquet Using DuckDB
# ============================================================

all_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()

print("\nAll Employee Records:")
print(all_employees)

# ============================================================
# Task 3: Filter Employee Records
# ============================================================

# 1. Employees with salary greater than 50000
high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

print("\nEmployees with Salary > 50000:")
print(high_salary)


# 2. Employees from IT department
it_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()

print("\nIT Department Employees:")
print(it_employees)


# 3. Employees who work in Delhi
delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()

print("\nEmployees Working in Delhi:")
print(delhi_employees)


# 4. IT employees with salary greater than 65000
it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
      AND salary > 65000
""").df()

print("\nIT Employees with Salary > 65000:")
print(it_high_salary)

# ============================================================
# Task 4: Select Specific Columns
# ============================================================

selected_columns = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()

print("\nEmployees Sorted by Salary:")
print(selected_columns)

# ============================================================
# Task 5: Perform Aggregations
# ============================================================

summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
""").df()

print("\nEmployee Salary Summary:")
print(summary)

# ============================================================
# Task 6: Group Data by Department
# ============================================================

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

print("\nDepartment Summary:")
print(department_summary)
# ============================================================
# Task 7: Create a DuckDB Table
# ============================================================

connection = duckdb.connect("company.duckdb")

connection.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT *
    FROM read_parquet('employees.parquet')
""")

database_employees = connection.execute("""
    SELECT *
    FROM employees
""").df()

print("\nEmployees from DuckDB Table:")
print(database_employees)

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

print("\nFiltered Parquet file created successfully.")

# ============================================================
# Task 9: Verify the Exported File
# ============================================================

verified_data = duckdb.sql("""
    SELECT *
    FROM read_parquet('high_salary_employees.parquet')
""").df()

print("\nHigh Salary Employees from Exported Parquet:")
print(verified_data)

# Bonus 1: Employee with the second-highest salary
second_highest = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()

print("\nEmployee with Second-Highest Salary:")
print(second_highest)


# Bonus 2: Top three highest-paid employees
top_three = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()

print("\nTop Three Highest-Paid Employees:")
print(top_three)


# Bonus 3: Average salary for each city
city_average = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()

print("\nAverage Salary by City:")
print(city_average)


# Bonus 4: Departments with average salary greater than 55000
department_average = duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
    ORDER BY average_salary DESC
""").df()

print("\nDepartments with Average Salary > 55000:")
print(department_average)


# Bonus 5: Add salary category
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
    ORDER BY salary DESC
""").df()

print("\nEmployee Salary Categories:")
print(salary_category)