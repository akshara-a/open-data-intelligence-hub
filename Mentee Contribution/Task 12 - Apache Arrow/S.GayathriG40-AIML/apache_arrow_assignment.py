import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc
import pandas as pd

# ==========================================
# Employee Data
# ==========================================

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

# ==========================================
# Task 1
# Create Arrow Table
# ==========================================

employee_table = pa.table(data)

print("=" * 60)
print("TASK 1 : ARROW TABLE")
print("=" * 60)
print(employee_table)

# ==========================================
# Task 2
# Display Schema
# ==========================================

print("\n" + "=" * 60)
print("TASK 2 : SCHEMA")
print("=" * 60)
print(employee_table.schema)

print("\nAnswers:")
print("employee_id datatype :", employee_table.schema.field("employee_id").type)
print("name datatype        :", employee_table.schema.field("name").type)
print("salary datatype      :", employee_table.schema.field("salary").type)

# ==========================================
# Task 3
# Inspect Table
# ==========================================

print("\n" + "=" * 60)
print("TASK 3 : INSPECT TABLE")
print("=" * 60)

print("Rows :", employee_table.num_rows)
print("Columns :", employee_table.num_columns)
print("Column Names :", employee_table.column_names)

print("\nName Column")
print(employee_table.column("name"))

print("\nFirst Three Rows")
print(employee_table.slice(0, 3))

# ==========================================
# Task 4
# Select Columns
# ==========================================

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print("\n" + "=" * 60)
print("TASK 4 : SELECTED COLUMNS")
print("=" * 60)
print(selected_table)

# ==========================================
# Task 5
# Salary > 50000
# ==========================================

salary_filter = pc.greater(employee_table["salary"], 50000)

high_salary_table = employee_table.filter(salary_filter)

print("\n" + "=" * 60)
print("TASK 5 : SALARY > 50000")
print("=" * 60)
print(high_salary_table)

# ==========================================
# Task 6
# IT Department
# ==========================================

department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print("\n" + "=" * 60)
print("TASK 6 : IT EMPLOYEES")
print("=" * 60)
print(it_employees)

# ==========================================
# Task 7
# Salary Calculations
# ==========================================

salary_column = employee_table["salary"]

print("\n" + "=" * 60)
print("TASK 7 : CALCULATIONS")
print("=" * 60)

print("Average Salary :", pc.mean(salary_column).as_py())
print("Maximum Salary :", pc.max(salary_column).as_py())
print("Minimum Salary :", pc.min(salary_column).as_py())
print("Total Salary   :", pc.sum(salary_column).as_py())

# ==========================================
# Task 8
# Add Bonus Column
# ==========================================

bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print("\n" + "=" * 60)
print("TASK 8 : BONUS COLUMN")
print("=" * 60)
print(employee_table)

# ==========================================
# Task 9
# Arrow -> Pandas
# ==========================================

employee_df = employee_table.to_pandas()

print("\n" + "=" * 60)
print("TASK 9 : PANDAS DATAFRAME")
print("=" * 60)
print(employee_df)

# ==========================================
# Task 10
# Pandas -> Arrow
# ==========================================

new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print("\n" + "=" * 60)
print("TASK 10 : PANDAS TO ARROW")
print("=" * 60)
print(new_arrow_table)

# ==========================================
# Task 11
# Save Parquet
# ==========================================

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("\n" + "=" * 60)
print("TASK 11")
print("employees.parquet created successfully.")

# ==========================================
# Task 12
# Read Parquet
# ==========================================

loaded_table = pq.read_table(
    "employees.parquet"
)

print("\n" + "=" * 60)
print("TASK 12 : READ PARQUET")
print("=" * 60)
print(loaded_table)

# ==========================================
# Task 13
# Save Arrow IPC
# ==========================================

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("\n" + "=" * 60)
print("TASK 13")
print("employees.arrow created successfully.")

# ==========================================
# Task 14
# Read Arrow IPC
# ==========================================

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print("\n" + "=" * 60)
print("TASK 14 : READ ARROW FILE")
print("=" * 60)
print(ipc_table)

# ==========================================
# BONUS TASK 1
# Delhi Employees
# ==========================================

print("\n" + "=" * 60)
print("BONUS 1 : DELHI EMPLOYEES")
print("=" * 60)

delhi_filter = pc.equal(
    employee_table["city"],
    "Delhi"
)

print(employee_table.filter(delhi_filter))

# ==========================================
# BONUS TASK 2
# Salary Between 50000 and 65000
# ==========================================

print("\n" + "=" * 60)
print("BONUS 2 : SALARY BETWEEN 50000 AND 65000")
print("=" * 60)

greater = pc.greater_equal(employee_table["salary"], 50000)
less = pc.less_equal(employee_table["salary"], 65000)

between = pc.and_(greater, less)

print(employee_table.filter(between))

# ==========================================
# BONUS TASK 3
# Annual Salary
# ==========================================

annual_salary = pc.multiply(
    employee_table["salary"],
    12
)

employee_table = employee_table.append_column(
    "annual_salary",
    annual_salary
)

print("\n" + "=" * 60)
print("BONUS 3 : ANNUAL SALARY")
print("=" * 60)
print(employee_table)

# ==========================================
# BONUS TASK 4
# Save IT Employees
# ==========================================

pq.write_table(
    it_employees,
    "it_employees.parquet"
)

print("\nBonus 4 : it_employees.parquet created.")

# ==========================================
# BONUS TASK 5
# Read Selected Columns
# ==========================================

selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print("\n" + "=" * 60)
print("BONUS 5 : NAME & SALARY")
print("=" * 60)
print(selected_columns)

# ==========================================
# BONUS TASK 6
# Sort Salary Descending
# ==========================================

sorted_df = employee_table.to_pandas().sort_values(
    by="salary",
    ascending=False
)

print("\n" + "=" * 60)
print("BONUS 6 : SORTED BY SALARY")
print("=" * 60)
print(sorted_df)

print("\n" + "=" * 60)
print("ALL TASKS COMPLETED SUCCESSFULLY")
print("=" * 60)