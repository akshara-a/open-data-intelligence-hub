import pyarrow as pa

# ==========================================
# Task 1: Create an Arrow Table
# ==========================================

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)

print("TASK 1: EMPLOYEE TABLE")
print(employee_table)


# ==========================================
# Task 2: Display the Schema
# ==========================================

print("\nTASK 2: SCHEMA")
print(employee_table.schema)


# ==========================================
# Task 3: Inspect the Table
# ==========================================

print("\nTASK 3: INSPECT TABLE")

print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print("\nName column:")
print(employee_table.column("name"))

print("\nFirst three rows:")
print(employee_table.slice(0, 3))


# ==========================================
# Task 4: Select Specific Columns
# ==========================================

print("\nTASK 4: SELECTED COLUMNS")

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print(selected_table)


# ==========================================
# Task 5: Filter Records
# ==========================================

import pyarrow.compute as pc

print("\nTASK 5: EMPLOYEES WITH SALARY > 50000")

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(salary_filter)

print(high_salary_table)

# ==========================================
# Task 6: Filter by Department
# ==========================================

print("\nTASK 6: IT DEPARTMENT EMPLOYEES")

department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print(it_employees)


# ==========================================
# Task 7: Perform Calculations
# ==========================================

print("\nTASK 7: SALARY CALCULATIONS")

salary_column = employee_table["salary"]

print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())


# ==========================================
# Task 8: Add Bonus Column
# ==========================================

print("\nTASK 8: ADD BONUS COLUMN")

bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print(employee_table)


# ==========================================
# Task 9: Convert Arrow to Pandas
# ==========================================

print("\nTASK 9: ARROW TO PANDAS")

employee_df = employee_table.to_pandas()

print(employee_df)


# ==========================================
# Task 10: Convert Pandas to Arrow
# ==========================================

print("\nTASK 10: PANDAS TO ARROW")

new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print(new_arrow_table)

import pyarrow.parquet as pq


# ==========================================
# Task 11: Save as Parquet File
# ==========================================

print("\nTASK 11: SAVE PARQUET FILE")

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("Parquet file created successfully.")


# ==========================================
# Task 12: Read Parquet File
# ==========================================

print("\nTASK 12: READ PARQUET FILE")

loaded_table = pq.read_table(
    "employees.parquet"
)

print(loaded_table)

import pyarrow.ipc as ipc
# ==========================================
# Task 13: Save as Arrow IPC File
# ==========================================

print("\nTASK 13: SAVE ARROW IPC FILE")

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("Arrow IPC file created successfully.")

# ==========================================
# Task 14: Read Arrow IPC File
# ==========================================

print("\nTASK 14: READ ARROW IPC FILE")

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print(ipc_table)

# ==========================================
# Bonus Task 1: Employees in Delhi
# ==========================================

print("\nBONUS TASK 1: EMPLOYEES IN DELHI")

delhi_filter = pc.equal(
    employee_table["city"],
    "Delhi"
)

delhi_employees = employee_table.filter(delhi_filter)

print(delhi_employees)


# ==========================================
# Bonus Task 2: Salary Between 50000 and 65000
# ==========================================

print("\nBONUS TASK 2: SALARY BETWEEN 50000 AND 65000")

salary_range_filter = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000)
)

salary_range_employees = employee_table.filter(
    salary_range_filter
)

print(salary_range_employees)


# ==========================================
# Bonus Task 3: Add Annual Salary Column
# ==========================================

print("\nBONUS TASK 3: ADD ANNUAL SALARY COLUMN")

annual_salary_column = pc.multiply(
    employee_table["salary"],
    12
)

employee_table = employee_table.append_column(
    "annual_salary",
    annual_salary_column
)

print(employee_table)


# ==========================================
# Bonus Task 4: Save IT Employees to Parquet
# ==========================================

print("\nBONUS TASK 4: SAVE IT EMPLOYEES")

pq.write_table(
    it_employees,
    "it_employees.parquet"
)

print("IT employees Parquet file created successfully.")


# ==========================================
# Bonus Task 5: Read Name and Salary Only
# ==========================================

print("\nBONUS TASK 5: READ NAME AND SALARY")

selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print(selected_columns)


# ==========================================
# Bonus Task 6: Sort Salary Highest to Lowest
# ==========================================

print("\nBONUS TASK 6: SORT BY SALARY DESCENDING")

sorted_table = employee_table.sort_by(
    [("salary", "descending")]
)

print(sorted_table)