import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc

# ---------------------------------------------------------------------------
# Task 1: Create an Arrow Table
# ---------------------------------------------------------------------------
data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)
print("=== Task 1: Arrow Table ===")
print(employee_table, "\n")

# ---------------------------------------------------------------------------
# Task 2: Display the Schema
# ---------------------------------------------------------------------------
print("=== Task 2: Schema ===")
print(employee_table.schema, "\n")
# 1. employee_id -> int64
# 2. name -> string
# 3. salary -> int64

# ---------------------------------------------------------------------------
# Task 3: Inspect the Table
# ---------------------------------------------------------------------------
print("=== Task 3: Inspect Table ===")
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)
print(employee_table.column("name"))
print(employee_table.slice(0, 3), "\n")

# ---------------------------------------------------------------------------
# Task 4: Select Specific Columns
# ---------------------------------------------------------------------------
print("=== Task 4: Selected Columns ===")
selected_table = employee_table.select(["name", "department", "salary"])
print(selected_table, "\n")

# ---------------------------------------------------------------------------
# Task 5: Filter Records (salary > 50000)
# ---------------------------------------------------------------------------
print("=== Task 5: Salary > 50000 ===")
salary_filter = pc.greater(employee_table["salary"], 50000)
high_salary_table = employee_table.filter(salary_filter)
print(high_salary_table, "\n")

# ---------------------------------------------------------------------------
# Task 6: Filter by Department (IT)
# ---------------------------------------------------------------------------
print("=== Task 6: IT Department ===")
department_filter = pc.equal(employee_table["department"], "IT")
it_employees = employee_table.filter(department_filter)
print(it_employees, "\n")

# ---------------------------------------------------------------------------
# Task 7: Perform Calculations
# ---------------------------------------------------------------------------
print("=== Task 7: Calculations ===")
salary_column = employee_table["salary"]
print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py(), "\n")

# ---------------------------------------------------------------------------
# Task 8: Add a New Column (bonus = 10% of salary)
# ---------------------------------------------------------------------------
print("=== Task 8: Add bonus column ===")
bonus_column = pc.multiply(employee_table["salary"], 0.10)
employee_table = employee_table.append_column("bonus", bonus_column)
print(employee_table, "\n")

# ---------------------------------------------------------------------------
# Task 9: Convert Arrow to Pandas
# ---------------------------------------------------------------------------
print("=== Task 9: Arrow to Pandas ===")
employee_df = employee_table.to_pandas()
print(employee_df, "\n")

# ---------------------------------------------------------------------------
# Task 10: Convert Pandas to Arrow
# ---------------------------------------------------------------------------
print("=== Task 10: Pandas to Arrow ===")
new_arrow_table = pa.Table.from_pandas(employee_df, preserve_index=False)
print(new_arrow_table, "\n")

# ---------------------------------------------------------------------------
# Task 11: Save as a Parquet File
# ---------------------------------------------------------------------------
pq.write_table(employee_table, "employees.parquet")
print("Parquet file created successfully.\n")

# ---------------------------------------------------------------------------
# Task 12: Read the Parquet File
# ---------------------------------------------------------------------------
print("=== Task 12: Read Parquet ===")
loaded_table = pq.read_table("employees.parquet")
print(loaded_table, "\n")

# ---------------------------------------------------------------------------
# Task 13: Save as an Arrow IPC File
# ---------------------------------------------------------------------------
with ipc.new_file("employees.arrow", employee_table.schema) as writer:
    writer.write_table(employee_table)
print("Arrow IPC file created successfully.\n")

# ---------------------------------------------------------------------------
# Task 14: Read the Arrow IPC File
# ---------------------------------------------------------------------------
print("=== Task 14: Read Arrow IPC ===")
with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()
print(ipc_table, "\n")

# ---------------------------------------------------------------------------
# Bonus Tasks
# ---------------------------------------------------------------------------
print("=== Bonus 1: Employees in Delhi ===")
delhi_filter = pc.equal(employee_table["city"], "Delhi")
delhi_employees = employee_table.filter(delhi_filter)
print(delhi_employees, "\n")

print("=== Bonus 2: Salaries between 50000 and 65000 ===")
range_filter = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000)
)
salary_range_table = employee_table.filter(range_filter)
print(salary_range_table, "\n")

print("=== Bonus 3: Add annual_salary column ===")
annual_salary_column = pc.multiply(employee_table["salary"], 12)
employee_table = employee_table.append_column("annual_salary", annual_salary_column)
print(employee_table, "\n")

print("=== Bonus 4: Save IT employees to it_employees.parquet ===")
it_filter = pc.equal(employee_table["department"], "IT")
it_only_table = employee_table.filter(it_filter)
pq.write_table(it_only_table, "it_employees.parquet")
print("it_employees.parquet created successfully.\n")

print("=== Bonus 5: Read only name and salary columns ===")
selected_columns = pq.read_table("employees.parquet", columns=["name", "salary"])
print(selected_columns, "\n")

print("=== Bonus 6: Sort employees by salary DESC ===")
sort_indices = pc.sort_indices(employee_table, sort_keys=[("salary", "descending")])
sorted_table = employee_table.take(sort_indices)
print(sorted_table)
