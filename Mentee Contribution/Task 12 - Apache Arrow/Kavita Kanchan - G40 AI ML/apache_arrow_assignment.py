import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.ipc as ipc
import pyarrow.parquet as pq

# ==========================================
# Task 1: Create an Arrow Table
# ==========================================
print("--- Task 1: Create an Arrow Table ---")
data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"],
}

employee_table = pa.table(data)
print(employee_table)
print()

# ==========================================
# Task 2: Display the Schema & Answer Questions
# ==========================================
print("--- Task 2: Display the Schema ---")
print(employee_table.schema)
print("\nSchema Answers:")
print("1. Data type of employee_id:", employee_table.schema.field("employee_id").type)
print("2. Data type of name:", employee_table.schema.field("name").type)
print("3. Data type of salary:", employee_table.schema.field("salary").type)
print()

# ==========================================
# Task 3: Inspect the Table
# ==========================================
print("--- Task 3: Inspect the Table ---")
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)
print("\nName Column:")
print(employee_table.column("name"))
print("\nFirst Three Rows:")
print(employee_table.slice(0, 3))
print()

# ==========================================
# Task 4: Select Specific Columns
# ==========================================
print("--- Task 4: Select Specific Columns ---")
selected_table = employee_table.select(["name", "department", "salary"])
print(selected_table)
print()

# ==========================================
# Task 5: Filter Records (Salary > 50000)
# ==========================================
print("--- Task 5: Filter Records (Salary > 50000) ---")
salary_filter = pc.greater(employee_table["salary"], 50000)
high_salary_table = employee_table.filter(salary_filter)
print(high_salary_table)
print()

# ==========================================
# Task 6: Filter by Department (IT)
# ==========================================
print("--- Task 6: Filter by Department (IT) ---")
department_filter = pc.equal(employee_table["department"], "IT")
it_employees = employee_table.filter(department_filter)
print(it_employees)
print()

# ==========================================
# Task 7: Perform Calculations
# ==========================================
print("--- Task 7: Perform Calculations ---")
salary_column = employee_table["salary"]
print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())
print()

# ==========================================
# Task 8: Add a New Column (bonus)
# ==========================================
print("--- Task 8: Add 'bonus' Column ---")
bonus_column = pc.multiply(employee_table["salary"], 0.10)
employee_table = employee_table.append_column("bonus", bonus_column)
print(employee_table)
print()

# ==========================================
# Task 9: Convert Arrow to Pandas
# ==========================================
print("--- Task 9: Convert Arrow to Pandas ---")
employee_df = employee_table.to_pandas()
print(employee_df)
print()

# ==========================================
# Task 10: Convert Pandas to Arrow
# ==========================================
print("--- Task 10: Convert Pandas to Arrow ---")
new_arrow_table = pa.Table.from_pandas(employee_df, preserve_index=False)
print(new_arrow_table)
print()

# ==========================================
# Task 11: Save as a Parquet File
# ==========================================
print("--- Task 11: Save as Parquet ---")
pq.write_table(employee_table, "employees.parquet")
print("Parquet file created successfully.")
print()

# ==========================================
# Task 12: Read the Parquet File
# ==========================================
print("--- Task 12: Read Parquet File ---")
loaded_table = pq.read_table("employees.parquet")
print(loaded_table)
print()

# ==========================================
# Task 13: Save as an Arrow IPC File
# ==========================================
print("--- Task 13: Save as Arrow IPC File ---")
with ipc.new_file("employees.arrow", employee_table.schema) as writer:
    writer.write_table(employee_table)
print("Arrow IPC file created successfully.")
print()

# ==========================================
# Task 14: Read the Arrow IPC File
# ==========================================
print("--- Task 14: Read Arrow IPC File ---")
with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()
print(ipc_table)
print()

# ==========================================
# Bonus Tasks Solutions
# ==========================================
print("==========================================")
print("              BONUS TASKS                 ")
print("==========================================")

# Bonus 1: Display employees who work in Delhi
print("\n--- Bonus 1: Employees in Delhi ---")
delhi_filter = pc.equal(employee_table["city"], "Delhi")
delhi_employees = employee_table.filter(delhi_filter)
print(delhi_employees)

# Bonus 2: Display employees with salaries between 50000 and 65000 (inclusive)
print("\n--- Bonus 2: Salaries between 50000 and 65000 ---")
salary_between_filter = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000),
)
salary_range_table = employee_table.filter(salary_between_filter)
print(salary_range_table)

# Bonus 3: Add 'annual_salary' column (salary * 12)
print("\n--- Bonus 3: Add 'annual_salary' Column ---")
annual_salary_column = pc.multiply(employee_table["salary"], 12)
employee_table = employee_table.append_column("annual_salary", annual_salary_column)
print(employee_table)

# Bonus 4: Save only IT employees to 'it_employees.parquet'
print("\n--- Bonus 4: Save IT Employees to Parquet ---")
pq.write_table(it_employees, "it_employees.parquet")
print("Saved IT employees to 'it_employees.parquet'.")

# Bonus 5: Read only 'name' and 'salary' columns from Parquet
print("\n--- Bonus 5: Read specific columns from Parquet ---")
selected_columns = pq.read_table("employees.parquet", columns=["name", "salary"])
print(selected_columns)

# Bonus 6: Sort employees by salary from highest to lowest
print("\n--- Bonus 6: Sort employees by salary (descending) ---")
sorted_indices = pc.sort_indices(
    employee_table,
    sort_keys=[("salary", "descending")]
)

sorted_table = employee_table.take(sorted_indices)

print(sorted_table)