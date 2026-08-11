"""
DuckDB Assignment Using Parquet
--------------------------------
This script demonstrates how to:
1. Create a Parquet file using Pandas.
2. Read and query Parquet data using DuckDB.
3. Filter, sort, aggregate, and group data.
4. Create a persistent DuckDB database.
5. Export query results back to Parquet.
6. Run bonus analytical SQL queries.

Required packages:
    pip install duckdb pandas pyarrow
"""

from pathlib import Path

import duckdb
import pandas as pd


# -----------------------------------------------------------------------------
# Project paths
# -----------------------------------------------------------------------------
# Path(__file__).parent gives the folder where this Python script is saved.
PROJECT_DIR = Path(__file__).parent
EMPLOYEES_PARQUET = PROJECT_DIR / "employees.parquet"
HIGH_SALARY_PARQUET = PROJECT_DIR / "high_salary_employees.parquet"
DUCKDB_DATABASE = PROJECT_DIR / "company.duckdb"


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def print_section(title: str) -> None:
    """Print a clear section header for each task."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_dataframe(df: pd.DataFrame) -> None:
    """Print a Pandas DataFrame in a clean table format."""
    print(df.to_string(index=False))


def run_duckdb_query(query: str) -> pd.DataFrame:
    """
    Run a SQL query using DuckDB and return the result as a Pandas DataFrame.

    DuckDB can directly query Parquet files with read_parquet().
    """
    return duckdb.sql(query).df()


# -----------------------------------------------------------------------------
# Task 1: Check required libraries
# -----------------------------------------------------------------------------
def task_1_check_libraries() -> None:
    """Confirm that the required libraries are available."""
    print_section("Task 1: Required Libraries")
    print("Required libraries imported successfully:")
    print("- duckdb")
    print("- pandas")
    print("- pyarrow, used internally by pandas for Parquet support")


# -----------------------------------------------------------------------------
# Tasks 2 and 3: Create employee dataset and save as Parquet
# -----------------------------------------------------------------------------
def task_2_and_3_create_employee_parquet() -> pd.DataFrame:
    """Create an employee DataFrame and save it as employees.parquet."""
    print_section("Tasks 2 and 3: Create Employee Dataset and Save as Parquet")

    # Dictionary containing employee data. Each key becomes a column name.
    data = {
        "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun", "Meera", "Karan"],
        "department": ["IT", "HR", "IT", "Finance", "HR", "Finance", "IT", "Sales"],
        "salary": [60000, 45000, 70000, 55000, 48000, 65000, 75000, 50000],
        "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai", "Bengaluru", "Delhi"],
    }

    # Convert the dictionary into a Pandas DataFrame.
    employee_df = pd.DataFrame(data)

    # Save the DataFrame as a Parquet file.
    # index=False prevents Pandas from writing row numbers as an extra column.
    employee_df.to_parquet(EMPLOYEES_PARQUET, index=False)

    print(f"Created dataset with {len(employee_df)} employee records.")
    print(f"Saved Parquet file: {EMPLOYEES_PARQUET}")
    print("\nEmployee dataset:")
    print_dataframe(employee_df)

    return employee_df


# -----------------------------------------------------------------------------
# Task 4: Read Parquet using DuckDB
# -----------------------------------------------------------------------------
def task_4_read_parquet_with_duckdb() -> None:
    """Read and display all records from employees.parquet using DuckDB."""
    print_section("Task 4: Read Parquet Using DuckDB")

    query = f"""
        SELECT *
        FROM read_parquet('{EMPLOYEES_PARQUET}')
    """

    result = run_duckdb_query(query)
    print("All employee records read directly from Parquet:")
    print_dataframe(result)


# -----------------------------------------------------------------------------
# Task 5: Filter employee records
# -----------------------------------------------------------------------------
def task_5_filter_employee_records() -> None:
    """Run filtering queries on the Parquet file using DuckDB SQL."""
    print_section("Task 5: Filter Employee Records")

    queries = {
        "Employees with salary > 50000": f"""
            SELECT *
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            WHERE salary > 50000
        """,
        "Employees in the IT department": f"""
            SELECT *
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            WHERE department = 'IT'
        """,
        "Employees working in Delhi": f"""
            SELECT *
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            WHERE city = 'Delhi'
        """,
        "IT employees with salary > 65000": f"""
            SELECT *
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            WHERE department = 'IT' AND salary > 65000
        """,
    }

    # Run each filter query and print its result.
    for title, query in queries.items():
        print(f"\n{title}:")
        result = run_duckdb_query(query)
        print_dataframe(result)


# -----------------------------------------------------------------------------
# Task 6: Select specific columns and sort by salary
# -----------------------------------------------------------------------------
def task_6_select_columns_and_sort() -> None:
    """Display selected columns sorted by salary from highest to lowest."""
    print_section("Task 6: Select Specific Columns and Sort by Salary")

    query = f"""
        SELECT name, department, salary
        FROM read_parquet('{EMPLOYEES_PARQUET}')
        ORDER BY salary DESC
    """

    result = run_duckdb_query(query)
    print("Name, department, and salary sorted by salary descending:")
    print_dataframe(result)


# -----------------------------------------------------------------------------
# Task 7: Perform aggregate operations
# -----------------------------------------------------------------------------
def task_7_aggregate_operations() -> None:
    """Calculate summary statistics for employee salaries."""
    print_section("Task 7: Aggregate Operations")

    query = f"""
        SELECT
            COUNT(*) AS total_employees,
            ROUND(AVG(salary), 2) AS average_salary,
            MAX(salary) AS maximum_salary,
            MIN(salary) AS minimum_salary,
            SUM(salary) AS total_salary_paid
        FROM read_parquet('{EMPLOYEES_PARQUET}')
    """

    result = run_duckdb_query(query)
    print("Salary summary:")
    print_dataframe(result)


# -----------------------------------------------------------------------------
# Task 8: Group employees by department
# -----------------------------------------------------------------------------
def task_8_group_by_department() -> None:
    """Group employees by department and calculate summary values."""
    print_section("Task 8: Group Data by Department")

    query = f"""
        SELECT
            department,
            COUNT(*) AS employee_count,
            ROUND(AVG(salary), 2) AS average_salary,
            MAX(salary) AS highest_salary,
            SUM(salary) AS total_salary
        FROM read_parquet('{EMPLOYEES_PARQUET}')
        GROUP BY department
        ORDER BY average_salary DESC
    """

    result = run_duckdb_query(query)
    print("Department-wise salary summary:")
    print_dataframe(result)


# -----------------------------------------------------------------------------
# Tasks 9 and 10: Create persistent DuckDB database and employees table
# -----------------------------------------------------------------------------
def task_9_and_10_create_duckdb_database() -> None:
    """Create company.duckdb and an employees table from the Parquet file."""
    print_section("Tasks 9 and 10: Create DuckDB Database and Employees Table")

    # Connect to a persistent DuckDB database file.
    connection = duckdb.connect(str(DUCKDB_DATABASE))

    # Create or replace the employees table using data from the Parquet file.
    connection.execute(
        f"""
        CREATE OR REPLACE TABLE employees AS
        SELECT *
        FROM read_parquet('{EMPLOYEES_PARQUET}')
        """
    )

    # Query the new persistent table to verify that it was created correctly.
    result = connection.execute("SELECT * FROM employees").df()

    print(f"Created DuckDB database: {DUCKDB_DATABASE}")
    print("Created table: employees")
    print("\nRecords stored in the DuckDB employees table:")
    print_dataframe(result)

    # Always close the connection when finished.
    connection.close()


# -----------------------------------------------------------------------------
# Task 11: Export query results to Parquet
# -----------------------------------------------------------------------------
def task_11_export_high_salary_to_parquet() -> None:
    """Export employees with salary greater than 50000 to a new Parquet file."""
    print_section("Task 11: Export High-Salary Employees to Parquet")

    duckdb.sql(
        f"""
        COPY (
            SELECT *
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            WHERE salary > 50000
        )
        TO '{HIGH_SALARY_PARQUET}'
        (FORMAT PARQUET)
        """
    )

    print(f"Filtered Parquet file created: {HIGH_SALARY_PARQUET}")


# -----------------------------------------------------------------------------
# Task 12: Verify exported Parquet file
# -----------------------------------------------------------------------------
def task_12_verify_exported_parquet() -> None:
    """Read and display high_salary_employees.parquet to verify the export."""
    print_section("Task 12: Verify Exported Parquet File")

    query = f"""
        SELECT *
        FROM read_parquet('{HIGH_SALARY_PARQUET}')
    """

    result = run_duckdb_query(query)
    print("Contents of high_salary_employees.parquet:")
    print_dataframe(result)


# -----------------------------------------------------------------------------
# Task 13: Bonus tasks
# -----------------------------------------------------------------------------
def task_13_bonus_tasks() -> None:
    """Run bonus analytical queries using DuckDB SQL."""
    print_section("Task 13: Bonus Tasks")

    bonus_queries = {
        "Second-highest-paid employee": f"""
            SELECT *
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            ORDER BY salary DESC
            LIMIT 1 OFFSET 1
        """,
        "Top 3 highest-paid employees": f"""
            SELECT *
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            ORDER BY salary DESC
            LIMIT 3
        """,
        "Average salary for each city": f"""
            SELECT
                city,
                ROUND(AVG(salary), 2) AS average_salary
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            GROUP BY city
            ORDER BY average_salary DESC
        """,
        "Departments with average salary > 55000": f"""
            SELECT
                department,
                ROUND(AVG(salary), 2) AS average_salary
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            GROUP BY department
            HAVING AVG(salary) > 55000
            ORDER BY average_salary DESC
        """,
        "Salary category using CASE statement": f"""
            SELECT
                employee_id,
                name,
                department,
                salary,
                CASE
                    WHEN salary >= 65000 THEN 'High'
                    WHEN salary >= 50000 THEN 'Medium'
                    ELSE 'Low'
                END AS salary_category
            FROM read_parquet('{EMPLOYEES_PARQUET}')
            ORDER BY salary DESC
        """,
    }

    # Execute and display every bonus query.
    for title, query in bonus_queries.items():
        print(f"\n{title}:")
        result = run_duckdb_query(query)
        print_dataframe(result)


# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------
def main() -> None:
    """Run all assignment tasks in order."""
    task_1_check_libraries()
    task_2_and_3_create_employee_parquet()
    task_4_read_parquet_with_duckdb()
    task_5_filter_employee_records()
    task_6_select_columns_and_sort()
    task_7_aggregate_operations()
    task_8_group_by_department()
    task_9_and_10_create_duckdb_database()
    task_11_export_high_salary_to_parquet()
    task_12_verify_exported_parquet()
    task_13_bonus_tasks()

    print_section("Assignment Completed")
    print("Generated files:")
    print(f"- {EMPLOYEES_PARQUET.name}")
    print(f"- {HIGH_SALARY_PARQUET.name}")
    print(f"- {DUCKDB_DATABASE.name}")


# This ensures main() runs only when this file is executed directly.
if __name__ == "__main__":
    main()
