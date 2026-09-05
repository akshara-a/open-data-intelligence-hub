import pandas as pd
import duckdb

data = {
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun", "Meera", "Karan"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance", "IT", "Sales"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000, 75000, 50000],
    "city": [
        "Delhi",
        "Mumbai",
        "Bengaluru",
        "Delhi",
        "Mumbai",
        "Chennai",
        "Bengaluru",
        "Delhi",
    ],
}

df = pd.DataFrame(data)

df.to_parquet("employees.parquet", index=False)

print("Parquet file created successfully.")


# Task 2: Read Parquet using DuckDB

result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()

print("\nAll employee records:")
print(result)

# Task 3.1: Employees with salary greater than 50000

high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

print("\nEmployees with salary greater than 50000:")
print(high_salary)


# Task 3.2: Employees from the IT department

it_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()

print("\nEmployees from the IT department:")
print(it_employees)

# Task 3.3: Employees who work in Delhi

delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()

print("\nEmployees who work in Delhi:")
print(delhi_employees)


# Task 3.4: IT employees with salary greater than 65000

it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
      AND salary > 65000
""").df()

print("\nIT employees with salary greater than 65000:")
print(it_high_salary)


# Task 4: Select specific columns and sort by salary

sorted_employees = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()

print("\nEmployees sorted by salary (highest to lowest):")
print(sorted_employees)

# Task 5: Perform aggregations

summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
""").df()

print("\nEmployee salary summary:")
print(summary)


# Task 6: Group data by department

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

print("\nDepartment-wise salary summary:")
print(department_summary)

# Task 7: Create persistent DuckDB database

connection = duckdb.connect("company.duckdb")

connection.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT *
    FROM read_parquet('employees.parquet')
""")

result = connection.execute("""
    SELECT *
    FROM employees
""").df()

print("\nEmployees table from DuckDB:")
print(result)

connection.close()

print("\nDuckDB database created successfully.")

# Task 8: Export high-salary employees to a new Parquet file

duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("\nHigh-salary Parquet file created successfully.")

# Task 9: Verify the exported Parquet file

result = duckdb.sql("""
    SELECT *
    FROM read_parquet('high_salary_employees.parquet')
""").df()

print("\nHigh-salary employees:")
print(result)


# Bonus 1: Find the second-highest salary

second_highest = duckdb.sql("""
    SELECT MAX(salary) AS second_highest_salary
    FROM read_parquet('employees.parquet')
    WHERE salary < (
        SELECT MAX(salary)
        FROM read_parquet('employees.parquet')
    )
""").df()

print("\nSecond-highest salary:")
print(second_highest)

# Bonus 2: Top 3 highest-paid employees

top_3 = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()

print("\nTop 3 highest-paid employees:")
print(top_3)

# Bonus 3: Average salary per city

city_summary = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()

print("\nAverage salary per city:")
print(city_summary)

# Bonus 4: Departments with average salary greater than 55000

high_paying_departments = duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
    ORDER BY average_salary DESC
""").df()

print("\nDepartments with average salary > 55000:")
print(high_paying_departments)


# Bonus 5: Categorize employees based on salary

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
    ORDER BY salary DESC
""").df()

print("\nEmployees with salary categories:")
print(salary_categories)
