import pandas as pd
import duckdb


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
print()

# Reading Parquet Using DuckDB

result = duckdb.sql("""SELECT * FROM read_parquet('employees.parquet')""").df()

print("=== All employee records ===")
print(result)
print()


# Filter Employee Records

high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

print("=== Task 3.1: Employees with salary > 50000 ===")
print(high_salary)
print()

it_department = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()

print("=== Task 3.2: Employees in IT department ===")
print(it_department)
print()

delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()

print("=== Task 3.3: Employees who work in Delhi ===")
print(delhi_employees)
print()

it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT' AND salary > 65000
""").df()

print("=== Task 3.4: IT employees with salary > 65000 ===")
print(it_high_salary)
print()


# Select Specific Columns

selected_columns = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()

print("=== Task 4: Name, department, salary sorted by salary DESC ===")
print(selected_columns)
print()


# Perform Aggregations

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


# Group Data

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

print("=== Task 6: Department summary ===")
print(department_summary)
print()


# Create a DuckDB Table

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


# Export Query Results to Parquet

duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("Filtered Parquet file created.")
print()


#  Verify the Exported File

verify_result = duckdb.sql("""
    SELECT *
    FROM read_parquet(
        'high_salary_employees.parquet'
    )
""").df()

print("=== Task 9: Verify high_salary_employees.parquet ===")
print(verify_result)
print()



# Employee with the second-highest salary
second_highest = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()

print("=== Second-highest paid employee ===")
print(second_highest)
print()

# 2. Top three highest-paid employees
top_three = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()

print("=== Top three highest-paid employees ===")
print(top_three)
print()

# 3. Average salary for each city
avg_salary_by_city = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()

print("=== Average salary by city ===")
print(avg_salary_by_city)
print()

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

print("=== Departments with average salary > 55000 ===")
print(high_avg_departments)
print()

# 5. Calculated column: salary_category
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

print("=== Salary category per employee ===")
print(salary_category)
