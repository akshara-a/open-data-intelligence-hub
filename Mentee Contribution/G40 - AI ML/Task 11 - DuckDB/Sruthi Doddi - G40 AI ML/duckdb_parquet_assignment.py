import pandas as pd
import duckdb

print("="*50)
print("DUCKDB PARQUET ASSIGNMENT")
print("="*50)

# Task 1: Create DataFrame and save as Parquet
data = {
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun", "Meera", "Karan"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance", "IT", "Sales"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000, 75000, 50000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai", "Bengaluru", "Delhi"]
}

df = pd.DataFrame(data)
df.to_parquet("employees.parquet", index=False)
print("\n Task 1: Parquet file created successfully!")
print(df)
print("\n" + "="*50 + "\n")

# Task 2: Read Parquet using DuckDB
result = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
""").df()

print("Task 2: All Employee Records")
print(result)
print("\n" + "="*50 + "\n")

# Task 3.1: Employees with salary > 50000
high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE salary > 50000
""").df()

print("Task 3.1: Employees with salary > 50000")
print(high_salary)
print("\n")

# Task 3.2: IT Department Employees
it_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT'
""").df()

print("Task 3.2: IT Department Employees")
print(it_employees)
print("\n")

# Task 3.3: Employees in Delhi
delhi_employees = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE city = 'Delhi'
""").df()

print("Task 3.3: Employees in Delhi")
print(delhi_employees)
print("\n")

# Task 3.4: IT Employees with salary > 65000
it_high_salary = duckdb.sql("""
    SELECT *
    FROM read_parquet('employees.parquet')
    WHERE department = 'IT' AND salary > 65000
""").df()

print("Task 3.4: IT Employees with salary > 65000")
print(it_high_salary)
print("\n" + "="*50 + "\n")

# Task 4: Select specific columns and sort
sorted_employees = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
""").df()

print("Task 4: Name, Department, Salary (Sorted by Salary DESC)")
print(sorted_employees)
print("\n" + "="*50 + "\n")

# Task 5: Aggregations
summary = duckdb.sql("""
    SELECT
        COUNT(*) AS employee_count,
        AVG(salary) AS average_salary,
        MAX(salary) AS maximum_salary,
        MIN(salary) AS minimum_salary,
        SUM(salary) AS total_salary
    FROM read_parquet('employees.parquet')
""").df()

print("Task 5: Aggregations Summary")
print(summary)
print("\n" + "="*50 + "\n")

# Task 6: Group by Department
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

print("Task 6: Department Summary")
print(dept_summary)
print("\n" + "="*50 + "\n")

# Task 7: Create DuckDB Table
connection = duckdb.connect("company.duckdb")
connection.execute("""
    CREATE OR REPLACE TABLE employees AS
    SELECT *
    FROM read_parquet('employees.parquet')
""")

table_data = connection.execute("""
    SELECT *
    FROM employees
""").df()

print("Task 7: Data from DuckDB Table")
print(table_data)
connection.close()
print(" company.duckdb created successfully!")
print("\n" + "="*50 + "\n")

# Task 8: Export High Salary to Parquet
duckdb.sql("""
    COPY (
        SELECT *
        FROM read_parquet('employees.parquet')
        WHERE salary > 50000
    )
    TO 'high_salary_employees.parquet'
    (FORMAT PARQUET)
""")

print("Task 8:  Filtered Parquet file created: high_salary_employees.parquet")
print("\n" + "="*50 + "\n")

# Task 9: Verify Exported File
verify_result = duckdb.sql("""
    SELECT *
    FROM read_parquet('high_salary_employees.parquet')
""").df()

print("Task 9: Contents of high_salary_employees.parquet")
print(verify_result)
print("\n" + "="*50 + "\n")

# Bonus Tasks
print("BONUS TASKS")
print("="*50)

# Bonus 1: Second Highest Salary
second_highest = duckdb.sql("""
    SELECT name, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
""").df()
print("\nBonus 1: Employee with Second Highest Salary")
print(second_highest)

# Bonus 2: Top 3 Highest Paid
top_3 = duckdb.sql("""
    SELECT name, department, salary
    FROM read_parquet('employees.parquet')
    ORDER BY salary DESC
    LIMIT 3
""").df()
print("\nBonus 2: Top 3 Highest Paid Employees")
print(top_3)

# Bonus 3: Average Salary by City
city_avg = duckdb.sql("""
    SELECT
        city,
        AVG(salary) AS average_salary,
        COUNT(*) AS employee_count
    FROM read_parquet('employees.parquet')
    GROUP BY city
    ORDER BY average_salary DESC
""").df()
print("\nBonus 3: Average Salary by City")
print(city_avg)

# Bonus 4: Departments with Avg Salary > 55000
high_avg_dept = duckdb.sql("""
    SELECT
        department,
        AVG(salary) AS average_salary,
        COUNT(*) AS employee_count
    FROM read_parquet('employees.parquet')
    GROUP BY department
    HAVING AVG(salary) > 55000
    ORDER BY average_salary DESC
""").df()
print("\nBonus 4: Departments with Average Salary > 55000")
print(high_avg_dept)

# Bonus 5: Salary Category
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
print("\nBonus 5: Employees with Salary Categories")
print(salary_categories)

print("\n" + "="*50)
print("="*50)

# Verify all files created
import os
print("\n Files Created:")
print("-"*40)
files = ['employees.parquet', 'high_salary_employees.parquet', 'company.duckdb']
for file in files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f" {file} - {size:,} bytes")
    else:
        print(f" {file} - NOT FOUND")