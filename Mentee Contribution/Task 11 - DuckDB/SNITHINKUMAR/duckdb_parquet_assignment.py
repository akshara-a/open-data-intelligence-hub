import pandas as pd
import duckdb

# ============================================================
# TASK 1: CREATE THE PARQUET FILE
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

print("\nTASK 1: Parquet file created successfully.")


# ============================================================
# TASK 2: READ PARQUET USING DUCKDB
# ============================================================

print("\nTASK 2: All Employee Records")

result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()

print(result)


# ============================================================
# TASK 3: FILTER EMPLOYEE RECORDS
# ============================================================

print("\nTASK 3A: Employees with salary greater than 50000")

high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

print(high_salary)


print("\nTASK 3B: Employees from IT Department")

it_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()

print(it_employees)


print("\nTASK 3C: Employees who work in Delhi")

delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()

print(delhi_employees)


print("\nTASK 3D: IT Employees with salary greater than 65000")

it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
    AND salary > 65000
""").df()

print(it_high_salary)


# ============================================================
# TASK 4: SELECT SPECIFIC COLUMNS AND SORT
# ============================================================

print("\nTASK 4: Name, Department and Salary sorted highest to lowest")

selected_columns = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()

print(selected_columns)


# ============================================================
# TASK 5: PERFORM AGGREGATIONS
# ============================================================

print("\nTASK 5: Salary Summary")

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


# ============================================================
# TASK 6: GROUP DATA BY DEPARTMENT
# ============================================================

print("\nTASK 6: Department-wise Salary Details")

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

print(department_summary)


# ============================================================
# TASK 7: CREATE A DUCKDB TABLE
# ============================================================

print("\nTASK 7: Creating company.duckdb and employees table")

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

print(result)

connection.close()

print("company.duckdb created successfully.")


# ============================================================
# TASK 8: EXPORT QUERY RESULTS TO PARQUET
# ============================================================

print("\nTASK 8: Export employees earning more than 50000")

duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("high_salary_employees.parquet created successfully.")


# ============================================================
# TASK 9: VERIFY THE EXPORTED FILE
# ============================================================

print("\nTASK 9: Verify Exported Parquet File")

result = duckdb.sql("""
    SELECT *
    FROM read_parquet('high_salary_employees.parquet')
""").df()

print(result)


# ============================================================
# BONUS TASK 1: SECOND-HIGHEST SALARY
# ============================================================

print("\nBONUS 1: Employee with Second-Highest Salary")

second_highest = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()

print(second_highest)


# ============================================================
# BONUS TASK 2: TOP THREE HIGHEST-PAID EMPLOYEES
# ============================================================

print("\nBONUS 2: Top Three Highest-Paid Employees")

top_three = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()

print(top_three)


# ============================================================
# BONUS TASK 3: AVERAGE SALARY FOR EACH CITY
# ============================================================

print("\nBONUS 3: Average Salary for Each City")

city_average = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()

print(city_average)


# ============================================================
# BONUS TASK 4: DEPARTMENTS WITH AVG SALARY > 55000
# ============================================================

print("\nBONUS 4: Departments with Average Salary Greater Than 55000")

department_average = duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS average_salary
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
    ORDER BY average_salary DESC
""").df()

print(department_average)


# ============================================================
# BONUS TASK 5: SALARY CATEGORY
# ============================================================

print("\nBONUS 5: Employee Salary Categories")

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

print(salary_category)


print("\n========================================")
print("ALL DUCKDB TASKS COMPLETED SUCCESSFULLY!")
print("========================================")