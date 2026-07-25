import pandas as pd
import duckdb

# Task 1: Create Parquet File
data = {
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun", "Meera", "Karan"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance", "IT", "Sales"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000, 75000, 50000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai", "Bengaluru", "Delhi"]
}
df = pd.DataFrame(data)
df.to_parquet("employees.parquet", index=False)

# Task 2: Read Parquet Using DuckDB
print("All Employees:")
print(duckdb.sql("SELECT * FROM read_parquet('employees.parquet')").df())

# Task 3: Filter Employee Records
print("\nEmployees with Salary > 50000:")
print(duckdb.sql("SELECT * FROM read_parquet('employees.parquet') WHERE salary > 50000").df())

# Task 4: Select Specific Columns
print("\nSelected Columns Sorted:")
print(duckdb.sql("SELECT name, department, salary FROM read_parquet('employees.parquet') ORDER BY salary DESC").df())

# Task 5: Aggregations
print("\nAggregations Summary:")
print(duckdb.sql("SELECT COUNT(*) AS count, AVG(salary) AS avg_sal, MAX(salary) AS max_sal, MIN(salary) AS min_sal, SUM(salary) AS total_sal FROM read_parquet('employees.parquet')").df())

# Task 6: Group Data
print("\nGroup by Department:")
print(duckdb.sql("SELECT department, COUNT(*) AS count, AVG(salary) AS avg_sal, MAX(salary) AS max_sal, SUM(salary) AS total_sal FROM read_parquet('employees.parquet') GROUP BY department ORDER BY avg_sal DESC").df())

# Task 7: Create DuckDB Table
conn = duckdb.connect("company.duckdb")
conn.execute("CREATE OR REPLACE TABLE employees AS SELECT * FROM read_parquet('employees.parquet')")
conn.close()

# Task 8: Export Query Results
duckdb.sql("COPY (SELECT * FROM read_parquet('employees.parquet') WHERE salary > 50000) TO 'high_salary_employees.parquet' (FORMAT PARQUET)")

# Task 9: Verify Exported File
print("\nVerified Exported High Salary Employees:")
print(duckdb.sql("SELECT * FROM read_parquet('high_salary_employees.parquet')").df())

# Bonus: Salary Categories
print("\nSalary Categories:")
print(duckdb.sql("""
    SELECT name, salary,
        CASE
            WHEN salary >= 65000 THEN 'High'
            WHEN salary >= 50000 THEN 'Medium'
            ELSE 'Low'
        END AS salary_category
    FROM read_parquet('employees.parquet')
""").df())
