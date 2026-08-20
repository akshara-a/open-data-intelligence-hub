import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc
import pandas as pd

# Task 1: Create Arrow Table
data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}
employee_table = pa.table(data)
print("Task 1 - Arrow Table created:")
print(employee_table)

# Task 2: Display Schema
print("\nTask 2 - Schema:")
print(employee_table.schema)

# Task 3: Inspect Table
print("\nTask 3 - Inspecting:")
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)

# Task 4: Select Specific Columns
print("\nTask 4 - Selected Columns:")
print(employee_table.select(["name", "department", "salary"]))

# Task 5: Filter Salary > 50000
print("\nTask 5 - High Salary:")
print(employee_table.filter(pc.greater(employee_table["salary"], 50000)))

# Task 6: Filter IT Department
print("\nTask 6 - IT Department:")
it_employees = employee_table.filter(pc.equal(employee_table["department"], "IT"))
print(it_employees)

# Task 7: Calculations
sal = employee_table["salary"]
print(f"\nTask 7 - Calculations: Avg={pc.mean(sal).as_py()}, Max={pc.max(sal).as_py()}, Min={pc.min(sal).as_py()}, Sum={pc.sum(sal).as_py()}")

# Task 8: Add Bonus Column
bonus_col = pc.multiply(employee_table["salary"], 0.10)
employee_table = employee_table.append_column("bonus", bonus_col)

# Task 9 & 10: Convert Arrow <-> Pandas
df = employee_table.to_pandas()
new_table = pa.Table.from_pandas(df, preserve_index=False)

# Task 11 & 12: Parquet Read/Write
pq.write_table(employee_table, "employees.parquet")
print("\nTask 12 - Loaded Parquet:")
print(pq.read_table("employees.parquet"))

# Task 13 & 14: Arrow IPC Read/Write
with ipc.new_file("employees.arrow", employee_table.schema) as writer:
    writer.write_table(employee_table)

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()
print("\nTask 14 - Loaded IPC:")
print(ipc_table)

# Bonus Tasks
pq.write_table(it_employees, "it_employees.parquet")
