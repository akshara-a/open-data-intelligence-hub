import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc


# ---------------------------------------------------------
# Task 1: Create an Arrow Table
# ---------------------------------------------------------

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)

print("\nTask 1 - Employee Arrow Table:")
print(employee_table)


# ---------------------------------------------------------
# Task 2: Display the Schema
# ---------------------------------------------------------

print("\nTask 2 - Schema:")
print(employee_table.schema)

print("employee_id type:", employee_table.schema.field("employee_id").type)
print("name type:", employee_table.schema.field("name").type)
print("salary type:", employee_table.schema.field("salary").type)


# ---------------------------------------------------------
# Task 3: Inspect the Table
# ---------------------------------------------------------

print("\nTask 3 - Table Inspection:")
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print("\nName column:")
print(employee_table.column("name"))

print("\nFirst three rows:")
print(employee_table.slice(0, 3))


# ---------------------------------------------------------
# Task 4: Select Specific Columns
# ---------------------------------------------------------

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print("\nTask 4 - Selected Columns:")
print(selected_table)


# ---------------------------------------------------------
# Task 5: Filter Records
# Employees earning more than 50,000
# ---------------------------------------------------------

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(salary_filter)

print("\nTask 5 - Employees earning more than 50,000:")
print(high_salary_table)


# ---------------------------------------------------------
# Task 6: Filter by Department
# IT employees
# ---------------------------------------------------------

department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print("\nTask 6 - IT Employees:")
print(it_employees)


# ---------------------------------------------------------
# Task 7: Perform Calculations
# ---------------------------------------------------------

salary_column = employee_table["salary"]

print("\nTask 7 - Salary Calculations:")
print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())


# ---------------------------------------------------------
# Task 8: Add a New Column
# Bonus = 10% of salary
# ---------------------------------------------------------

bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print("\nTask 8 - Table with Bonus:")
print(employee_table)


# ---------------------------------------------------------
# Task 9: Convert Arrow to Pandas
# ---------------------------------------------------------

employee_df = employee_table.to_pandas()

print("\nTask 9 - Arrow to Pandas:")
print(employee_df)


# ---------------------------------------------------------
# Task 10: Convert Pandas to Arrow
# ---------------------------------------------------------

new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print("\nTask 10 - Pandas to Arrow:")
print(new_arrow_table)


# ---------------------------------------------------------
# Task 11: Save as Parquet
# ---------------------------------------------------------

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("\nTask 11 - Parquet file created successfully.")


# ---------------------------------------------------------
# Task 12: Read the Parquet File
# ---------------------------------------------------------

loaded_table = pq.read_table(
    "employees.parquet"
)

print("\nTask 12 - Loaded Parquet Table:")
print(loaded_table)


# ---------------------------------------------------------
# Task 13: Save as Arrow IPC File
# ---------------------------------------------------------

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("\nTask 13 - Arrow IPC file created successfully.")


# ---------------------------------------------------------
# Task 14: Read the Arrow IPC File
# ---------------------------------------------------------

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print("\nTask 14 - Loaded Arrow IPC Table:")
print(ipc_table)


# =========================================================
# BONUS TASKS
# =========================================================

# Bonus 1: Employees who work in Delhi

delhi_filter = pc.equal(
    employee_table["city"],
    "Delhi"
)

delhi_employees = employee_table.filter(delhi_filter)

print("\nBonus 1 - Employees in Delhi:")
print(delhi_employees)


# Bonus 2: Employees with salary between 50,000 and 65,000

salary_min = pc.greater_equal(
    employee_table["salary"],
    50000
)

salary_max = pc.less_equal(
    employee_table["salary"],
    65000
)

salary_range_filter = pc.and_(
    salary_min,
    salary_max
)

salary_range_employees = employee_table.filter(
    salary_range_filter
)

print("\nBonus 2 - Salary between 50,000 and 65,000:")
print(salary_range_employees)


# Bonus 3: Add annual_salary column

annual_salary_column = pc.multiply(
    employee_table["salary"],
    12
)

employee_table = employee_table.append_column(
    "annual_salary",
    annual_salary_column
)

print("\nBonus 3 - Annual Salary:")
print(employee_table)


# Bonus 4: Save only IT employees to it_employees.parquet

it_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(it_filter)

pq.write_table(
    it_employees,
    "it_employees.parquet"
)

print("\nBonus 4 - IT employees saved to it_employees.parquet")


# Bonus 5: Read only name and salary columns

selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print("\nBonus 5 - Name and Salary columns:")
print(selected_columns)


# Bonus 6: Sort employees by salary highest to lowest

sorted_indices = pc.sort_indices(
    employee_table,
    sort_keys=[("salary", "descending")]
)

sorted_employees = employee_table.take(sorted_indices)

print("\nBonus 6 - Employees sorted by salary:")
print(sorted_employees)


print("\nApache Arrow assignment completed successfully.")