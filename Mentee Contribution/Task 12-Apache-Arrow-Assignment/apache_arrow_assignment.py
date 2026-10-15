import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc


# ============================================================
# Apache Arrow Assignment Using Python
# ============================================================

print("=" * 60)
print("APACHE ARROW ASSIGNMENT")
print("=" * 60)


# ------------------------------------------------------------
# Task 1: Create an Arrow Table
# ------------------------------------------------------------

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)

print("\n=== Task 1: Arrow Table ===")
print(employee_table)


# ------------------------------------------------------------
# Task 2: Display the Schema
# ------------------------------------------------------------

print("\n=== Task 2: Schema ===")
print(employee_table.schema)

print("\nData Types:")
print("employee_id:", employee_table.schema.field("employee_id").type)
print("name:", employee_table.schema.field("name").type)
print("salary:", employee_table.schema.field("salary").type)


# ------------------------------------------------------------
# Task 3: Inspect the Table
# ------------------------------------------------------------

print("\n=== Task 3: Inspect Table ===")

print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print("\nName column:")
print(employee_table.column("name"))

print("\nFirst three rows:")
print(employee_table.slice(0, 3))


# ------------------------------------------------------------
# Task 4: Select Specific Columns
# ------------------------------------------------------------

print("\n=== Task 4: Selected Columns ===")

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print(selected_table)


# ------------------------------------------------------------
# Task 5: Filter Salary > 50000
# ------------------------------------------------------------

print("\n=== Task 5: Salary Greater Than 50000 ===")

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(salary_filter)

print(high_salary_table)


# ------------------------------------------------------------
# Task 6: Filter IT Department
# ------------------------------------------------------------

print("\n=== Task 6: IT Employees ===")

department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print(it_employees)


# ------------------------------------------------------------
# Task 7: Perform Calculations
# ------------------------------------------------------------

print("\n=== Task 7: Salary Calculations ===")

salary_column = employee_table["salary"]

average_salary = pc.mean(salary_column).as_py()
maximum_salary = pc.max(salary_column).as_py()
minimum_salary = pc.min(salary_column).as_py()
total_salary = pc.sum(salary_column).as_py()

print("Average salary:", average_salary)
print("Maximum salary:", maximum_salary)
print("Minimum salary:", minimum_salary)
print("Total salary:", total_salary)


# ------------------------------------------------------------
# Task 8: Add Bonus Column
# ------------------------------------------------------------

print("\n=== Task 8: Add Bonus Column ===")

bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print(employee_table)


# ------------------------------------------------------------
# Task 9: Convert Arrow to Pandas
# ------------------------------------------------------------

print("\n=== Task 9: Arrow to Pandas ===")

employee_df = employee_table.to_pandas()

print(employee_df)


# ------------------------------------------------------------
# Task 10: Convert Pandas to Arrow
# ------------------------------------------------------------

print("\n=== Task 10: Pandas to Arrow ===")

new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print(new_arrow_table)


# ------------------------------------------------------------
# Task 11: Save as Parquet
# ------------------------------------------------------------

print("\n=== Task 11: Save Parquet File ===")

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("Parquet file created successfully.")


# ------------------------------------------------------------
# Task 12: Read Parquet File
# ------------------------------------------------------------

print("\n=== Task 12: Read Parquet File ===")

loaded_table = pq.read_table(
    "employees.parquet"
)

print(loaded_table)


# ------------------------------------------------------------
# Task 13: Save as Arrow IPC File
# ------------------------------------------------------------

print("\n=== Task 13: Save Arrow IPC File ===")

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("Arrow IPC file created successfully.")


# ------------------------------------------------------------
# Task 14: Read Arrow IPC File
# ------------------------------------------------------------

print("\n=== Task 14: Read Arrow IPC File ===")

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print(ipc_table)


# ============================================================
# BONUS TASKS
# ============================================================

# ------------------------------------------------------------
# Bonus 1: Employees in Delhi
# ------------------------------------------------------------

print("\n=== Bonus 1: Employees in Delhi ===")

delhi_filter = pc.equal(
    employee_table["city"],
    "Delhi"
)

delhi_employees = employee_table.filter(delhi_filter)

print(delhi_employees)


# ------------------------------------------------------------
# Bonus 2: Salary Between 50000 and 65000
# ------------------------------------------------------------

print("\n=== Bonus 2: Salary Between 50000 and 65000 ===")

minimum_filter = pc.greater_equal(
    employee_table["salary"],
    50000
)

maximum_filter = pc.less_equal(
    employee_table["salary"],
    65000
)

salary_range_filter = pc.and_(
    minimum_filter,
    maximum_filter
)

salary_range_employees = employee_table.filter(
    salary_range_filter
)

print(salary_range_employees)


# ------------------------------------------------------------
# Bonus 3: Add Annual Salary
# ------------------------------------------------------------

print("\n=== Bonus 3: Annual Salary ===")

annual_salary_column = pc.multiply(
    employee_table["salary"],
    12
)

employee_table = employee_table.append_column(
    "annual_salary",
    annual_salary_column
)

print(employee_table)


# ------------------------------------------------------------
# Bonus 4: Save IT Employees
# ------------------------------------------------------------

print("\n=== Bonus 4: Save IT Employees ===")

it_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(it_filter)

pq.write_table(
    it_employees,
    "it_employees.parquet"
)

print("IT employees saved to it_employees.parquet")


# ------------------------------------------------------------
# Bonus 5: Read Only Name and Salary
# ------------------------------------------------------------

print("\n=== Bonus 5: Read Name and Salary ===")

selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print(selected_columns)


# ------------------------------------------------------------
# Bonus 6: Sort Employees by Salary
# ------------------------------------------------------------

print("\n=== Bonus 6: Sort by Salary Descending ===")

sort_indices = pc.sort_indices(
    employee_table,
    sort_keys=[("salary", "descending")]
)

sorted_employees = pc.take(
    employee_table,
    sort_indices
)

print(sorted_employees)


# ============================================================
# Final Output Files
# ============================================================

print("\n" + "=" * 60)
print("ASSIGNMENT COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nGenerated files:")
print("1. employees.parquet")
print("2. employees.arrow")
print("3. it_employees.parquet")