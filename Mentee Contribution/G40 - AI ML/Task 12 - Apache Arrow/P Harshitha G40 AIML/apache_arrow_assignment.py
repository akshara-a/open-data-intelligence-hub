# pyrefly: ignore [missing-import]
import pyarrow as pa
# pyrefly: ignore [missing-import]
import pyarrow.parquet as pq
# pyrefly: ignore [missing-import]
import pyarrow.ipc as ipc
import pandas as pd

# Employee data
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "Marketing"],
    "salary": [60000, 45000, 70000, 80000, 55000],
    "city": ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]
}

# Create Arrow Table
table = pa.table(data)

print("=== Arrow Table ===")
print(table)

# Display Schema
print("\n=== Schema ===")
print(table.schema)

# Filter IT Employees
it_mask = pa.compute.equal(table["department"], "IT")
it_employees = table.filter(it_mask)

print("\n=== IT Department Employees ===")
print(it_employees)

# Convert to Pandas DataFrame
df = table.to_pandas()

print("\n=== Pandas DataFrame ===")
print(df)

# Save as Parquet
pq.write_table(table, "employees.parquet")
print("\nemployees.parquet saved successfully.")

# Save as Arrow IPC File
with pa.OSFile("employees.arrow", "wb") as sink:
    with ipc.new_file(sink, table.schema) as writer:
        writer.write_table(table)

print("employees.arrow saved successfully.")

# Read Parquet File
parquet_table = pq.read_table("employees.parquet")

print("\n=== Data Read From Parquet ===")
print(parquet_table.to_pandas())

# Read Arrow IPC File
with pa.memory_map("employees.arrow", "r") as source:
    reader = ipc.RecordBatchFileReader(source)
    arrow_table = reader.read_all()

print("\n=== Data Read From Arrow File ===")
print(arrow_table.to_pandas())