"""
Apache Arrow Assignment Using Python
------------------------------------
Create, inspect, filter, convert, calculate, and save tabular data
using Apache Arrow, Pandas, Parquet, and Arrow IPC.
"""

from __future__ import annotations

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc


# ---------------------------------------------------------------------------
# Source data
# ---------------------------------------------------------------------------

DATA = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"],
}

PARQUET_PATH = "employees.parquet"
ARROW_IPC_PATH = "employees.arrow"


def section(title: str) -> None:
    """Print a clear section header for console output."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# === Task 1: Create Arrow Table ===
def task1_create_table() -> pa.Table:
    section("Task 1: Create an Arrow Table")
    employee_table = pa.table(DATA)
    print(employee_table)
    return employee_table


# === Task 2: Display Schema ===
def task2_display_schema(employee_table: pa.Table) -> None:
    section("Task 2: Display the Schema")
    print(employee_table.schema)
    print("\nSchema Q&A:")
    field_map = {field.name: field.type for field in employee_table.schema}
    print(f"1. Data type of employee_id: {field_map['employee_id']}")
    print(f"2. Data type of name:        {field_map['name']}")
    print(f"3. Data type of salary:      {field_map['salary']}")


# === Task 3: Inspect the Table ===
def task3_inspect_table(employee_table: pa.Table) -> None:
    section("Task 3: Inspect the Table")
    print("Rows:", employee_table.num_rows)
    print("Columns:", employee_table.num_columns)
    print("Column names:", employee_table.column_names)
    print("\nName column:")
    print(employee_table.column("name"))
    print("\nFirst three rows:")
    print(employee_table.slice(0, 3))


# === Task 4: Select Specific Columns ===
def task4_select_columns(employee_table: pa.Table) -> pa.Table:
    section("Task 4: Select Specific Columns (name, department, salary)")
    selected_table = employee_table.select(["name", "department", "salary"])
    print(selected_table)
    return selected_table


# === Task 5: Filter by Salary > 50000 ===
def task5_filter_high_salary(employee_table: pa.Table) -> pa.Table:
    section("Task 5: Filter Records (salary > 50000)")
    salary_filter = pc.greater(employee_table["salary"], 50000)
    high_salary_table = employee_table.filter(salary_filter)
    print(high_salary_table)
    return high_salary_table


# === Task 6: Filter by Department == IT ===
def task6_filter_it_department(employee_table: pa.Table) -> pa.Table:
    section("Task 6: Filter by Department (IT)")
    department_filter = pc.equal(employee_table["department"], "IT")
    it_employees = employee_table.filter(department_filter)
    print(it_employees)
    return it_employees


# === Task 7: Perform Calculations ===
def task7_salary_calculations(employee_table: pa.Table) -> None:
    section("Task 7: Perform Calculations on salary")
    salary_column = employee_table["salary"]
    print("Average salary:", pc.mean(salary_column).as_py())
    print("Maximum salary:", pc.max(salary_column).as_py())
    print("Minimum salary:", pc.min(salary_column).as_py())
    print("Total salary:", pc.sum(salary_column).as_py())


# === Task 8: Add Bonus Column ===
def task8_add_bonus_column(employee_table: pa.Table) -> pa.Table:
    section("Task 8: Add a New Column (bonus = 10% of salary)")
    bonus_column = pc.multiply(employee_table["salary"], 0.10)
    employee_table = employee_table.append_column("bonus", bonus_column)
    print(employee_table)
    return employee_table


# === Task 9: Convert Arrow to Pandas ===
def task9_arrow_to_pandas(employee_table: pa.Table):
    section("Task 9: Convert Arrow to Pandas")
    employee_df = employee_table.to_pandas()
    print(employee_df)
    return employee_df


# === Task 10: Convert Pandas to Arrow ===
def task10_pandas_to_arrow(employee_df) -> pa.Table:
    section("Task 10: Convert Pandas to Arrow")
    new_arrow_table = pa.Table.from_pandas(employee_df, preserve_index=False)
    print(new_arrow_table)
    return new_arrow_table


# === Task 11: Save as Parquet ===
def task11_save_parquet(employee_table: pa.Table, path: str = PARQUET_PATH) -> None:
    section("Task 11: Save as a Parquet File")
    pq.write_table(employee_table, path)
    print(f"Parquet file created successfully: {path}")


# === Task 12: Read the Parquet File ===
def task12_read_parquet(path: str = PARQUET_PATH) -> pa.Table:
    section("Task 12: Read the Parquet File")
    loaded_table = pq.read_table(path)
    print(loaded_table)
    return loaded_table


# === Task 13: Save as Arrow IPC File ===
def task13_save_arrow_ipc(employee_table: pa.Table, path: str = ARROW_IPC_PATH) -> None:
    section("Task 13: Save as an Arrow IPC File")
    with ipc.new_file(path, employee_table.schema) as writer:
        writer.write_table(employee_table)
    print(f"Arrow IPC file created successfully: {path}")


# === Task 14: Read the Arrow IPC File ===
def task14_read_arrow_ipc(path: str = ARROW_IPC_PATH) -> pa.Table:
    section("Task 14: Read the Arrow IPC File")
    with ipc.open_file(path) as reader:
        ipc_table = reader.read_all()
    print(ipc_table)
    return ipc_table


# === Bonus Tasks ===
def bonus_tasks(employee_table: pa.Table) -> None:
    """Run optional bonus exercises on the enriched employee table."""

    # Bonus 1: Employees in Delhi
    section("Bonus 1: Employees who work in Delhi")
    delhi_filter = pc.equal(employee_table["city"], "Delhi")
    delhi_employees = employee_table.filter(delhi_filter)
    print(delhi_employees)

    # Bonus 2: Salaries between 50000 and 65000 (inclusive)
    section("Bonus 2: Employees with salary between 50000 and 65000 (inclusive)")
    lower = pc.greater_equal(employee_table["salary"], 50000)
    upper = pc.less_equal(employee_table["salary"], 65000)
    range_filter = pc.and_(lower, upper)
    range_employees = employee_table.filter(range_filter)
    print(range_employees)

    # Bonus 3: Add annual_salary = salary * 12
    section("Bonus 3: Add annual_salary column (salary * 12)")
    annual_salary = pc.multiply(employee_table["salary"], 12)
    table_with_annual = employee_table.append_column("annual_salary", annual_salary)
    print(table_with_annual)

    # Bonus 4: IT employees only (in-memory display)
    section("Bonus 4: IT employees only")
    it_filter = pc.equal(employee_table["department"], "IT")
    it_only = employee_table.filter(it_filter)
    print(it_only)

    # Bonus 5: Read only name and salary from employees.parquet
    section("Bonus 5: Read only name and salary columns from Parquet")
    selected_columns = pq.read_table(PARQUET_PATH, columns=["name", "salary"])
    print(selected_columns)

    # Bonus 6: Sort employees by salary highest to lowest
    section("Bonus 6: Sort employees by salary (highest to lowest)")
    sort_indices = pc.sort_indices(
        employee_table,
        sort_keys=[("salary", "descending")],
    )
    sorted_table = employee_table.take(sort_indices)
    print(sorted_table)


def main() -> None:
    # Tasks 1–7 operate on the base 5-column table
    employee_table = task1_create_table()
    task2_display_schema(employee_table)
    task3_inspect_table(employee_table)
    task4_select_columns(employee_table)
    task5_filter_high_salary(employee_table)
    task6_filter_it_department(employee_table)
    task7_salary_calculations(employee_table)

    # Task 8 enriches the main table used for IO
    employee_table = task8_add_bonus_column(employee_table)

    # Tasks 9–10: Pandas round-trip (verification branch)
    employee_df = task9_arrow_to_pandas(employee_table)
    task10_pandas_to_arrow(employee_df)

    # Tasks 11–14: Persist and reload enriched table
    task11_save_parquet(employee_table)
    task12_read_parquet()
    task13_save_arrow_ipc(employee_table)
    task14_read_arrow_ipc()

    # Optional bonuses
    bonus_tasks(employee_table)

    section("Assignment complete")
    print("Generated files:")
    print(f"  - {PARQUET_PATH}")
    print(f"  - {ARROW_IPC_PATH}")


if __name__ == "__main__":
    main()
