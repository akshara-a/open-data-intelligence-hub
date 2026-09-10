import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc

# ============================================================
# Task 1: Create an Arrow Table
# ============================================================
data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Ashish", "Rahul", "Saniya", "Vishakha", "Pritam", "iqra"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)
print("=== Task 1: Employee Arrow Table ===")
print(employee_table)
print()

# Task 2: Display the Schema
# ============================================================
print("=== Task 2: Schema ===")
print(employee_table.schema)
print()
print("employee_id type:", employee_table.schema.field('employee_id').type)
print("name type:", employee_table.schema.field('name').type)
print("salary type:", employee_table.schema.field('salary').type)
print()

# ============================================================
# Task 3: Inspect the Table
# ============================================================
print("=== Task 3: Table Inspection ===")
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)
print()
print("Name column:")
print(employee_table.column("name"))
print()
print("First three rows:")
print(employee_table.slice(0, 3))
print()

# ============================================================
# Task 4: Select Specific Columns
# ============================================================
selected_table = employee_table.select(["name", "department", "salary"])
print("=== Task 4: Selected Columns (name, department, salary) ===")
print(selected_table)
print()

# ============================================================
# Task 5: Filter Records - Salary > 50000
# ============================================================
salary_filter = pc.greater(employee_table["salary"], 50000)
high_salary_table = employee_table.filter(salary_filter)
print("=== Task 5: Employees with Salary > 50000 ===")
print(high_salary_table)
print()

# ============================================================
# Task 6: Filter by Department - IT
# ============================================================
department_filter = pc.equal(employee_table["department"], "IT")
it_employees = employee_table.filter(department_filter)
print("=== Task 6: IT Department Employees ===")
print(it_employees)
print()

# ============================================================
# Task 7: Perform Calculations
# ============================================================
salary_column = employee_table["salary"]
print("=== Task 7: Salary Calculations ===")
print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())
print()

# ============================================================
# Task 8: Add a New Column - Bonus (10% of salary)
# ============================================================
bonus_column = pc.multiply(employee_table["salary"], 0.10)
employee_table = employee_table.append_column("bonus", bonus_column)
print("=== Task 8: Table with Bonus Column ===")
print(employee_table)
print()

# ============================================================
# Task 9: Convert Arrow to Pandas
# ============================================================
employee_df = employee_table.to_pandas()
print("=== Task 9: Converted to Pandas DataFrame ===")
print(employee_df)
print()

# ============================================================
# Task 10: Convert Pandas back to Arrow
# ============================================================
new_arrow_table = pa.Table.from_pandas(employee_df, preserve_index=False)
print("=== Task 10: Converted back to Arrow Table ===")
print(new_arrow_table)
print()

# ============================================================
# Task 11: Save as a Parquet File
# ============================================================
pq.write_table(employee_table, "employees.parquet")
print("Task 11: Parquet file created successfully (employees.parquet).\n")

# ============================================================
# Task 12: Read the Parquet File
# ============================================================
loaded_table = pq.read_table("employees.parquet")
print("=== Task 12: Loaded from employees.parquet ===")
print(loaded_table)
print()

# ============================================================
# Task 13: Save as an Arrow IPC File
# ============================================================
with ipc.new_file("employees.arrow", employee_table.schema) as writer:
    writer.write_table(employee_table)
print("Task 13: Arrow IPC file created successfully (employees.arrow).\n")

# ============================================================
# Task 14: Read the Arrow IPC File
# ============================================================
with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()
print("=== Task 14: Loaded from employees.arrow ===")
print(ipc_table)
print()

# ============================================================
# Bonus Tasks
# ============================================================

# Bonus 1: Employees who work in Delhi
print("=== Bonus 1: Employees in Delhi ===")
delhi_filter = pc.equal(employee_table["city"], "Delhi")
print(employee_table.filter(delhi_filter))
print()

# Bonus 2: Salaries between 50000 and 65000
print("=== Bonus 2: Salaries Between 50000 and 65000 ===")
range_filter = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000)
)
print(employee_table.filter(range_filter))
print()

# Bonus 3: Add annual_salary column (salary * 12)
print("=== Bonus 3: Table with Annual Salary Column ===")
annual_salary_column = pc.multiply(employee_table["salary"], 12)
employee_table = employee_table.append_column("annual_salary", annual_salary_column)
print(employee_table)
print()

# Bonus 4: Save only IT employees to it_employees.parquet
print("Bonus 4: Saving IT employees to it_employees.parquet...")
it_filter = pc.equal(employee_table["department"], "IT")
it_only_table = employee_table.filter(it_filter)
pq.write_table(it_only_table, "it_employees.parquet")
print("it_employees.parquet created successfully.\n")

# Bonus 5: Read only name and salary columns from Parquet
print("=== Bonus 5: Name and Salary Columns Only ===")
selected_columns = pq.read_table("employees.parquet", columns=["name", "salary"])
print(selected_columns)
print()

# Bonus 6: Sort employees by salary descending
print("=== Bonus 6: Sorted by Salary (Descending) ===")
sort_indices = pc.sort_indices(employee_table, sort_keys=[("salary", "descending")])
sorted_table = employee_table.take(sort_indices)
print(sorted_table)