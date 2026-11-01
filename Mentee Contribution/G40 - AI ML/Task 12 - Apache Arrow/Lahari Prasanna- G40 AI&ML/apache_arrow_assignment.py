# Apache Arrow Assignment Using Python
# Employee Data Analysis with PyArrow and Pandas


# ============================================================
# Task 1: Create an Arrow Table
# ============================================================

import pyarrow as pa

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"],
}

employee_table = pa.table(data)

print("\n========== TASK 1: CREATE ARROW TABLE ==========")
print(employee_table)


# ============================================================
# Task 2: Display the Schema
# ============================================================

print("\n========== TASK 2: SCHEMA ==========")
print(employee_table.schema)


# ============================================================
# Task 3: Inspect the Table
# ============================================================

print("\n========== TASK 3: INSPECT TABLE ==========")

print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print("\nName column:")
print(employee_table.column("name"))

print("\nFirst three rows:")
print(employee_table.slice(0, 3))


# ============================================================
# Task 4: Select Specific Columns
# ============================================================

print("\n========== TASK 4: SELECT COLUMNS ==========")

selected_table = employee_table.select(["name", "department", "salary"])

print(selected_table)


# ============================================================
# Task 5: Filter Records
# Employees whose salary is greater than 50000
# ============================================================

import pyarrow.compute as pc

print("\n========== TASK 5: SALARY > 50000 ==========")

salary_filter = pc.greater(employee_table["salary"], 50000)

high_salary_table = employee_table.filter(salary_filter)

print(high_salary_table)


# ============================================================
# Task 6: Filter by Department
# Employees from IT department
# ============================================================

print("\n========== TASK 6: IT EMPLOYEES ==========")

department_filter = pc.equal(employee_table["department"], "IT")

it_employees = employee_table.filter(department_filter)

print(it_employees)


# ============================================================
# Task 7: Perform Calculations
# ============================================================

print("\n========== TASK 7: SALARY CALCULATIONS ==========")

salary_column = employee_table["salary"]

print("Average salary:", pc.mean(salary_column).as_py())

print("Maximum salary:", pc.max(salary_column).as_py())

print("Minimum salary:", pc.min(salary_column).as_py())

print("Total salary:", pc.sum(salary_column).as_py())


# ============================================================
# Task 8: Add a New Column
# Bonus = 10% of salary
# ============================================================

print("\n========== TASK 8: ADD BONUS COLUMN ==========")

bonus_column = pc.multiply(employee_table["salary"], 0.10)

employee_table = employee_table.append_column("bonus", bonus_column)

print(employee_table)


# ============================================================
# Task 9: Convert Arrow to Pandas
# ============================================================

print("\n========== TASK 9: ARROW TO PANDAS ==========")

employee_df = employee_table.to_pandas()

print(employee_df)


# ============================================================
# Task 10: Convert Pandas to Arrow
# ============================================================

print("\n========== TASK 10: PANDAS TO ARROW ==========")

new_arrow_table = pa.Table.from_pandas(employee_df, preserve_index=False)

print(new_arrow_table)


# ============================================================
# Task 11: Save as a Parquet File
# ============================================================

import pyarrow.parquet as pq

print("\n========== TASK 11: WRITE PARQUET ==========")

pq.write_table(employee_table, "employees.parquet")

print("Parquet file created successfully.")


# ============================================================
# Task 12: Read the Parquet File
# ============================================================

print("\n========== TASK 12: READ PARQUET ==========")

loaded_table = pq.read_table("employees.parquet")

print(loaded_table)


# ============================================================
# Task 13: Save as an Arrow IPC File
# ============================================================

import pyarrow.ipc as ipc

print("\n========== TASK 13: WRITE ARROW IPC ==========")

with ipc.new_file("employees.arrow", employee_table.schema) as writer:
    writer.write_table(employee_table)

print("Arrow IPC file created successfully.")


# ============================================================
# Task 14: Read the Arrow IPC File
# ============================================================

print("\n========== TASK 14: READ ARROW IPC ==========")

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print(ipc_table)


# ============================================================
# BONUS TASKS
# ============================================================

print("\n\n============================================================")
print("BONUS TASKS")
print("============================================================")


# ------------------------------------------------------------
# Bonus Task 1: Display employees who work in Delhi
# ------------------------------------------------------------

print("\n========== BONUS 1: DELHI EMPLOYEES ==========")

delhi_filter = pc.equal(employee_table["city"], "Delhi")

delhi_employees = employee_table.filter(delhi_filter)

print(delhi_employees)


# ------------------------------------------------------------
# Bonus Task 2: Salary between 50000 and 65000
# ------------------------------------------------------------

print("\n========== BONUS 2: SALARY BETWEEN 50000 AND 65000 ==========")

min_salary_filter = pc.greater_equal(employee_table["salary"], 50000)

max_salary_filter = pc.less_equal(employee_table["salary"], 65000)

salary_range_filter = pc.and_(min_salary_filter, max_salary_filter)

salary_range_employees = employee_table.filter(salary_range_filter)

print(salary_range_employees)


# ------------------------------------------------------------
# Bonus Task 3: Add annual_salary column
# ------------------------------------------------------------

print("\n========== BONUS 3: ANNUAL SALARY ==========")

annual_salary_column = pc.multiply(employee_table["salary"], 12)

employee_table = employee_table.append_column("annual_salary", annual_salary_column)

print(employee_table)


# ------------------------------------------------------------
# Bonus Task 4: Save only IT employees
# ------------------------------------------------------------

print("\n========== BONUS 4: SAVE IT EMPLOYEES ==========")

pq.write_table(it_employees, "it_employees.parquet")

print("IT employees Parquet file created successfully.")


# ------------------------------------------------------------
# Bonus Task 5: Read only name and salary columns
# ------------------------------------------------------------

print("\n========== BONUS 5: READ SELECTED COLUMNS ==========")

selected_columns = pq.read_table("employees.parquet", columns=["name", "salary"])

print(selected_columns)


# ------------------------------------------------------------
# Bonus Task 6: Sort employees by salary
# Highest to lowest
# ------------------------------------------------------------

print("\n========== BONUS 6: SORT BY SALARY ==========")

sort_indices = pc.sort_indices(employee_table, sort_keys=[("salary", "descending")])

sorted_employees = employee_table.take(sort_indices)

print(sorted_employees)


# ============================================================
# Assignment Complete
# ============================================================

print("\n============================================================")
print("ASSIGNMENT COMPLETED SUCCESSFULLY")
print("============================================================")

print("\nRequired files created:")
print("1. apache_arrow_assignment.py")
print("2. employees.parquet")
print("3. employees.arrow")

print("\nBonus file created:")
print("4. it_employees.parquet")
