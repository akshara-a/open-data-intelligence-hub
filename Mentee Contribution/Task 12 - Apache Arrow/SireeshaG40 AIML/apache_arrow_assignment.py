import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc
import pandas as pd

# ===================================================
# Task 1: Create Employee Data
# ===================================================

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)

print("=" * 60)
print("Employee Table")
print("=" * 60)
print(employee_table)

# ===================================================
# Task 2: Display Schema
# ===================================================

print("\nSchema")
print(employee_table.schema)

print("\nData Types")
print("employee_id :", employee_table.schema.field("employee_id").type)
print("name        :", employee_table.schema.field("name").type)
print("salary      :", employee_table.schema.field("salary").type)

# ===================================================
# Task 3: Inspect Table
# ===================================================

print("\nRows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column Names:", employee_table.column_names)

print("\nName Column")
print(employee_table.column("name"))

print("\nFirst Three Rows")
print(employee_table.slice(0, 3))

# ===================================================
# Task 4: Select Specific Columns
# ===================================================

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print("\nSelected Columns")
print(selected_table)

# ===================================================
# Task 5: Salary > 50000
# ===================================================

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary = employee_table.filter(salary_filter)

print("\nEmployees Salary > 50000")
print(high_salary)

# ===================================================
# Task 6: IT Department
# ===================================================

department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_table = employee_table.filter(department_filter)

print("\nIT Employees")
print(it_table)

# ===================================================
# Task 7: Calculations
# ===================================================

salary = employee_table["salary"]

print("\nSalary Statistics")
print("Average :", pc.mean(salary).as_py())
print("Maximum :", pc.max(salary).as_py())
print("Minimum :", pc.min(salary).as_py())
print("Total   :", pc.sum(salary).as_py())

# ===================================================
# Task 8: Add Bonus Column
# ===================================================

bonus = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus
)

print("\nTable with Bonus")
print(employee_table)

# ===================================================
# Task 9: Arrow to Pandas
# ===================================================

employee_df = employee_table.to_pandas()

print("\nArrow to Pandas")
print(employee_df)

# ===================================================
# Task 10: Pandas to Arrow
# ===================================================

new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print("\nPandas to Arrow")
print(new_arrow_table)

# ===================================================
# Task 11: Save as Parquet
# ===================================================

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("\nemployees.parquet created successfully.")

# ===================================================
# Task 12: Read Parquet
# ===================================================

loaded_table = pq.read_table(
    "employees.parquet"
)

print("\nRead Parquet")
print(loaded_table)

# ===================================================
# Task 13: Save Arrow IPC File
# ===================================================

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("\nemployees.arrow created successfully.")

# ===================================================
# Task 14: Read Arrow IPC File
# ===================================================

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print("\nRead Arrow IPC File")
print(ipc_table)

# ===================================================
# Bonus 1: Employees from Delhi
# ===================================================

print("\nEmployees from Delhi")

delhi_filter = pc.equal(
    employee_table["city"],
    "Delhi"
)

print(employee_table.filter(delhi_filter))

# ===================================================
# Bonus 2: Salary Between 50000 and 65000
# ===================================================

print("\nSalary Between 50000 and 65000")

greater_equal = pc.greater_equal(
    employee_table["salary"],
    50000
)

less_equal = pc.less_equal(
    employee_table["salary"],
    65000
)

between = pc.and_(greater_equal, less_equal)

print(employee_table.filter(between))

# ===================================================
# Bonus 3: Annual Salary
# ===================================================

annual_salary = pc.multiply(
    employee_table["salary"],
    12
)

table2 = employee_table.append_column(
    "annual_salary",
    annual_salary
)

print("\nAnnual Salary Added")
print(table2)

# ===================================================
# Bonus 4: Save IT Employees
# ===================================================

pq.write_table(
    it_table,
    "it_employees.parquet"
)

print("\nit_employees.parquet created successfully.")

# ===================================================
# Bonus 5: Read Selected Columns
# ===================================================

selected = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print("\nSelected Columns from Parquet")
print(selected)

# ===================================================
# Bonus 6: Sort by Salary
# ===================================================

sorted_df = employee_table.to_pandas().sort_values(
    by="salary",
    ascending=False
)

print("\nEmployees Sorted by Salary")
print(sorted_df)

print("\nAssignment Completed Successfully.")