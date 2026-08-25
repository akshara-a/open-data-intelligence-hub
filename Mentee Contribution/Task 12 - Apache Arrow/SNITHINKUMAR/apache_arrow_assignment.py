import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc
import pandas as pd


# Employee Dataset
data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}


# Task 1: Create an Arrow Table
employee_table = pa.table(data)

print("\n--- Task 1: Arrow Table ---")
print(employee_table)


# Task 2: Display Schema
print("\n--- Task 2: Schema ---")
print(employee_table.schema)

print("employee_id datatype:", employee_table.schema.field("employee_id").type)
print("name datatype:", employee_table.schema.field("name").type)
print("salary datatype:", employee_table.schema.field("salary").type)


# Task 3: Inspect the Table
print("\n--- Task 3: Inspect Table ---")

print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print("\nName Column:")
print(employee_table.column("name"))

print("\nFirst Three Rows:")
print(employee_table.slice(0, 3))


# Task 4: Select Specific Columns
print("\n--- Task 4: Selected Columns ---")

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print(selected_table)


# Task 5: Filter Salary > 50000
print("\n--- Task 5: Salary Greater Than 50000 ---")

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(salary_filter)

print(high_salary_table)


# Task 6: Filter IT Department
print("\n--- Task 6: IT Employees ---")

department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print(it_employees)


# Task 7: Salary Calculations
print("\n--- Task 7: Salary Calculations ---")

salary_column = employee_table["salary"]

print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())


# Task 8: Add Bonus Column
print("\n--- Task 8: Bonus Column ---")

bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print(employee_table)


# Task 9: Arrow to Pandas
print("\n--- Task 9: Arrow to Pandas ---")

employee_df = employee_table.to_pandas()

print(employee_df)


# Task 10: Pandas to Arrow
print("\n--- Task 10: Pandas to Arrow ---")

new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print(new_arrow_table)


# Task 11: Save as Parquet
print("\n--- Task 11: Save Parquet ---")

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("Parquet file created successfully.")


# Task 12: Read Parquet
print("\n--- Task 12: Read Parquet ---")

loaded_table = pq.read_table(
    "employees.parquet"
)

print(loaded_table)


# Task 13: Save Arrow IPC File
print("\n--- Task 13: Save Arrow IPC ---")

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("Arrow IPC file created successfully.")


# Task 14: Read Arrow IPC File
print("\n--- Task 14: Read Arrow IPC ---")

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print(ipc_table)


# ---------------- BONUS TASKS ----------------

print("\n========== BONUS TASKS ==========")


# Bonus 1: Employees in Delhi
print("\nEmployees in Delhi:")

delhi_filter = pc.equal(
    employee_table["city"],
    "Delhi"
)

delhi_employees = employee_table.filter(delhi_filter)

print(delhi_employees)


# Bonus 2: Salary Between 50000 and 65000
print("\nEmployees with salary between 50000 and 65000:")

salary_range = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000)
)

salary_range_table = employee_table.filter(salary_range)

print(salary_range_table)


# Bonus 3: Annual Salary Column
print("\nAnnual Salary Column:")

annual_salary = pc.multiply(
    employee_table["salary"],
    12
)

employee_table = employee_table.append_column(
    "annual_salary",
    annual_salary
)

print(employee_table)


# Bonus 4: Save IT Employees
pq.write_table(
    it_employees,
    "it_employees.parquet"
)

print("\nit_employees.parquet created successfully.")


# Bonus 5: Read Only Name and Salary
print("\nName and Salary Columns:")

selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print(selected_columns)


# Bonus 6: Sort Salary Highest to Lowest
print("\nEmployees Sorted by Salary (Highest to Lowest):")

sorted_employees = employee_table.sort_by(
    [("salary", "descending")]
)

print(sorted_employees)

print("\nApache Arrow Assignment Completed Successfully!")