import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc

# =========================================================
# Task 1: Create an Arrow Table
# =========================================================
data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)

print("=== Task 1: Arrow Table ===")
print(employee_table)
print()

# =========================================================
# Task 2: Display the Schema
# =========================================================
print("=== Task 2: Schema ===")
print(employee_table.schema)
print()
print("1. employee_id data type:", employee_table.schema.field("employee_id").type)
print("2. name data type:", employee_table.schema.field("name").type)
print("3. salary data type:", employee_table.schema.field("salary").type)
print()

# =========================================================
# Task 3: Inspect the Table
# =========================================================
print("=== Task 3: Inspecting the Table ===")
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)
print("\nname column:")
print(employee_table.column("name"))
print("\nFirst three rows:")
print(employee_table.slice(0, 3))
print()

# =========================================================
# Task 4: Select Specific Columns
# =========================================================
selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print("=== Task 4: Selected Columns (name, department, salary) ===")
print(selected_table)
print()

# =========================================================
# Task 5: Filter Records (salary > 50000)
# =========================================================
salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(salary_filter)

print("=== Task 5: Employees with salary > 50000 ===")
print(high_salary_table)
print()

# =========================================================
# Task 6: Filter by Department (IT)
# =========================================================
department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print("=== Task 6: IT department employees ===")
print(it_employees)
print()

# =========================================================
# Task 7: Perform Calculations
# =========================================================
salary_column = employee_table["salary"]

print("=== Task 7: Salary Calculations ===")
print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())
print()

# =========================================================
# Task 8: Add a New Column (bonus = 10% of salary)
# =========================================================
bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print("=== Task 8: Table with bonus column ===")
print(employee_table)
print()

# =========================================================
# Task 9: Convert Arrow to Pandas
# =========================================================
employee_df = employee_table.to_pandas()

print("=== Task 9: Converted to Pandas DataFrame ===")
print(employee_df)
print()

# =========================================================
# Task 10: Convert Pandas to Arrow
# =========================================================
new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print("=== Task 10: Converted back to Arrow Table ===")
print(new_arrow_table)
print()

# =========================================================
# Task 11: Save as a Parquet File
# =========================================================
pq.write_table(
    employee_table,
    "employees.parquet"
)

print("=== Task 11: Parquet file created successfully ===")
print()

# =========================================================
# Task 12: Read the Parquet File
# =========================================================
loaded_table = pq.read_table(
    "employees.parquet"
)

print("=== Task 12: Data loaded from employees.parquet ===")
print(loaded_table)
print()

# =========================================================
# Task 13: Save as an Arrow IPC File
# =========================================================
with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("=== Task 13: Arrow IPC file created successfully ===")
print()

# =========================================================
# Task 14: Read the Arrow IPC File
# =========================================================
with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print("=== Task 14: Data loaded from employees.arrow ===")
print(ipc_table)
print()

# =========================================================
# Bonus Tasks
# =========================================================
print("=== Bonus Tasks ===")

# 1. Employees who work in Delhi
delhi_filter = pc.equal(employee_table["city"], "Delhi")
delhi_employees = employee_table.filter(delhi_filter)
print("\n1. Employees who work in Delhi:")
print(delhi_employees)

# 2. Employees with salaries between 50000 and 65000
salary_range_filter = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000)
)
salary_range_employees = employee_table.filter(salary_range_filter)
print("\n2. Employees with salary between 50000 and 65000:")
print(salary_range_employees)

# 3. Add annual_salary column (salary * 12)
annual_salary_column = pc.multiply(employee_table["salary"], 12)
employee_table = employee_table.append_column("annual_salary", annual_salary_column)
print("\n3. Table with annual_salary column added:")
print(employee_table)

# 4. Save only IT employees to it_employees.parquet
it_department_filter = pc.equal(employee_table["department"], "IT")
it_only_table = employee_table.filter(it_department_filter)
pq.write_table(it_only_table, "it_employees.parquet")
print("\n4. IT employees saved to it_employees.parquet")

# 5. Read only name and salary columns from the Parquet file
selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)
print("\n5. name and salary columns from employees.parquet:")
print(selected_columns)

# 6. Sort employees by salary from highest to lowest
sort_indices = pc.sort_indices(
    employee_table,
    sort_keys=[("salary", "descending")]
)
sorted_table = employee_table.take(sort_indices)
print("\n6. Employees sorted by salary (highest to lowest):")
print(sorted_table)
