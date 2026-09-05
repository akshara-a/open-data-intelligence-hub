"""
Simple DuckDB + Parquet Assignment
====================================
Steps:
  1. Create a DuckDB database with an employees table
  2. Save that table as a Parquet file
  3. Read the Parquet file back and filter high salary employees
  4. Save the filtered result as another Parquet file

Install:
    pip install duckdb

Run:
    python duckdb_parquet_assignment.py
"""

import duckdb

# 1. Connect to a database file (created automatically if it doesn't exist)
con = duckdb.connect("company.duckdb")

# 2. Create a table and add some sample employees
con.execute("DROP TABLE IF EXISTS employees")
con.execute("""
    CREATE TABLE employees (
        id INTEGER,
        name VARCHAR,
        department VARCHAR,
        salary INTEGER
    )
""")

con.execute("""
    INSERT INTO employees VALUES
        (1, 'Ava Thompson', 'Engineering', 118000),
        (2, 'Liam Chen', 'Engineering', 95000),
        (3, 'Sofia Rossi', 'Marketing', 72000),
        (4, 'Noah Martin', 'Sales', 68000),
        (5, 'Emma Wilson', 'Engineering', 132000),
        (6, 'Lucas Silva', 'Finance', 88000),
        (7, 'Mia Anderson', 'Marketing', 91000),
        (8, 'Ethan Brown', 'Sales', 76000)
""")

print("Employees table created:")
con.sql("SELECT * FROM employees").show()

# 3. Save the whole table as a Parquet file
con.execute("COPY employees TO 'employees.parquet' (FORMAT PARQUET)")
print("Saved employees.parquet")

# 4. Read the Parquet file directly and filter salary > 90000
print("Employees earning more than 90,000:")
con.sql("SELECT * FROM 'employees.parquet' WHERE salary > 90000").show()

# 5. Save that filtered result as a new Parquet file
con.execute("""
    COPY (
        SELECT * FROM 'employees.parquet' WHERE salary > 90000
    ) TO 'high_salary_employees.parquet' (FORMAT PARQUET)
""")
print("Saved high_salary_employees.parquet")

con.close()
print("Done!")
