import sys
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.ipc as ipc
import pyarrow.parquet as pq


# Save generated files in the same folder as this Python script.
OUTPUT_DIRECTORY = Path(__file__).resolve().parent

PARQUET_FILE = OUTPUT_DIRECTORY / "employees.parquet"
ARROW_FILE = OUTPUT_DIRECTORY / "employees.arrow"
IT_PARQUET_FILE = OUTPUT_DIRECTORY / "it_employees.parquet"


def print_heading(title: str) -> None:
    """Print a clear heading for each assignment task."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def create_employee_table() -> pa.Table:
    """Create and return an Apache Arrow employee table."""
    employee_data = {
        "employee_id": [1, 2, 3, 4, 5, 6],
        "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
        "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
        "salary": [60000, 45000, 70000, 55000, 48000, 65000],
        "city": [
            "Delhi",
            "Mumbai",
            "Bengaluru",
            "Delhi",
            "Mumbai",
            "Chennai",
        ],
    }

    return pa.table(employee_data)


def main() -> None:
    """Complete all Apache Arrow assignment tasks."""

    # Task 1: Create an Arrow table
    employee_table = create_employee_table()

    print_heading("TASK 1: APACHE ARROW EMPLOYEE TABLE")
    print(employee_table)

    # Task 2: Display schema
    print_heading("TASK 2: TABLE SCHEMA")
    print(employee_table.schema)

    print("\nSchema answers:")
    print("employee_id data type:", employee_table.schema.field("employee_id").type)
    print("name data type:", employee_table.schema.field("name").type)
    print("salary data type:", employee_table.schema.field("salary").type)

    # Task 3: Inspect table
    print_heading("TASK 3: INSPECT THE TABLE")
    print("Number of rows:", employee_table.num_rows)
    print("Number of columns:", employee_table.num_columns)
    print("Column names:", employee_table.column_names)

    print("\nName column:")
    print(employee_table.column("name"))

    print("\nFirst three rows:")
    print(employee_table.slice(0, 3))

    # Task 4: Select specific columns
    print_heading("TASK 4: SELECTED COLUMNS")
    selected_table = employee_table.select(
        ["name", "department", "salary"]
    )
    print(selected_table)

    # Task 5: Employees with salary greater than 50000
    print_heading("TASK 5: SALARY GREATER THAN 50000")
    salary_filter = pc.greater(employee_table["salary"], 50000)
    high_salary_table = employee_table.filter(salary_filter)
    print(high_salary_table)

    # Task 6: Employees from IT department
    print_heading("TASK 6: IT DEPARTMENT EMPLOYEES")
    department_filter = pc.equal(employee_table["department"], "IT")
    it_employees = employee_table.filter(department_filter)
    print(it_employees)

    # Task 7: Salary calculations
    print_heading("TASK 7: SALARY CALCULATIONS")
    salary_column = employee_table["salary"]

    print("Average salary:", pc.mean(salary_column).as_py())
    print("Maximum salary:", pc.max(salary_column).as_py())
    print("Minimum salary:", pc.min(salary_column).as_py())
    print("Total salary:", pc.sum(salary_column).as_py())

    # Task 8: Add bonus column
    print_heading("TASK 8: ADD 10% BONUS COLUMN")
    bonus_column = pc.multiply(employee_table["salary"], 0.10)

    employee_table = employee_table.append_column(
        "bonus",
        bonus_column,
    )
    print(employee_table)

    # Task 9: Convert Arrow to Pandas
    print_heading("TASK 9: ARROW TABLE TO PANDAS")
    employee_df = employee_table.to_pandas()
    print(employee_df)

    # Task 10: Convert Pandas back to Arrow
    print_heading("TASK 10: PANDAS DATAFRAME TO ARROW")
    new_arrow_table = pa.Table.from_pandas(
        employee_df,
        preserve_index=False,
    )
    print(new_arrow_table)

    # Task 11: Save as Parquet
    print_heading("TASK 11: SAVE AS PARQUET")
    pq.write_table(employee_table, PARQUET_FILE)
    print(f"Parquet file created successfully: {PARQUET_FILE.name}")

    # Task 12: Read Parquet file
    print_heading("TASK 12: READ PARQUET FILE")
    loaded_table = pq.read_table(PARQUET_FILE)
    print(loaded_table)

    # Task 13: Save as Arrow IPC file
    print_heading("TASK 13: SAVE AS ARROW IPC FILE")
    with ipc.new_file(ARROW_FILE, employee_table.schema) as writer:
        writer.write_table(employee_table)

    print(f"Arrow IPC file created successfully: {ARROW_FILE.name}")

    # Task 14: Read Arrow IPC file
    print_heading("TASK 14: READ ARROW IPC FILE")
    with ipc.open_file(ARROW_FILE) as reader:
        ipc_table = reader.read_all()

    print(ipc_table)

    # Bonus Task 1: Employees who work in Delhi
    print_heading("BONUS 1: EMPLOYEES FROM DELHI")
    delhi_filter = pc.equal(employee_table["city"], "Delhi")
    delhi_employees = employee_table.filter(delhi_filter)
    print(delhi_employees)

    # Bonus Task 2: Salaries between 50000 and 65000
    print_heading("BONUS 2: SALARIES BETWEEN 50000 AND 65000")
    minimum_filter = pc.greater_equal(employee_table["salary"], 50000)
    maximum_filter = pc.less_equal(employee_table["salary"], 65000)
    salary_range_filter = pc.and_(minimum_filter, maximum_filter)

    salary_range_employees = employee_table.filter(
        salary_range_filter
    )
    print(salary_range_employees)

    # Bonus Task 3: Add annual salary column
    print_heading("BONUS 3: ADD ANNUAL SALARY COLUMN")
    annual_salary_column = pc.multiply(
        employee_table["salary"],
        12,
    )

    employee_table_with_annual_salary = employee_table.append_column(
        "annual_salary",
        annual_salary_column,
    )
    print(employee_table_with_annual_salary)

    # Bonus Task 4: Save IT employees to Parquet
    print_heading("BONUS 4: SAVE IT EMPLOYEES AS PARQUET")
    pq.write_table(it_employees, IT_PARQUET_FILE)
    print(f"File created successfully: {IT_PARQUET_FILE.name}")

    # Bonus Task 5: Read only name and salary
    print_heading("BONUS 5: READ NAME AND SALARY COLUMNS")
    selected_columns = pq.read_table(
        PARQUET_FILE,
        columns=["name", "salary"],
    )
    print(selected_columns)

    # Bonus Task 6: Sort salary highest to lowest
    print_heading("BONUS 6: SORT BY SALARY HIGHEST TO LOWEST")
    sorted_employee_table = employee_table.sort_by(
        [("salary", "descending")]
    )
    print(sorted_employee_table)

    print_heading("ASSIGNMENT COMPLETED SUCCESSFULLY")
    print("Generated files:")
    print(f"1. {PARQUET_FILE.name}")
    print(f"2. {ARROW_FILE.name}")
    print(f"3. {IT_PARQUET_FILE.name}")


if __name__ == "__main__":
    try:
        main()
    except (ImportError, OSError, ValueError, pa.ArrowException) as error:
        print(f"Assignment failed: {error}", file=sys.stderr)
        sys.exit(1)