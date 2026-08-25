
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc
import pandas as pd
import os

print("="*60)
print("APACHE ARROW ASSIGNMENT")
print("="*60)


# TASK 1: Create an Arrow Table

print("\n" + "="*60)
print("TASK 1: Create Arrow Table")
print("="*60)

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)
print("Arrow Table Created Successfully!")
print(employee_table)


# TASK 2: Display the Schema

print("\n" + "="*60)
print("TASK 2: Display Schema")
print("="*60)

print("Table Schema:")
print(employee_table.schema)
print("\nAnswers:")
print("1. employee_id data type:", employee_table.schema.field('employee_id').type)
print("2. name data type:", employee_table.schema.field('name').type)
print("3. salary data type:", employee_table.schema.field('salary').type)


# TASK 3: Inspect the Table

print("\n" + "="*60)
print("TASK 3: Inspect the Table")
print("="*60)

print("Number of rows:", employee_table.num_rows)
print("Number of columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)
print("\nName column:")
print(employee_table.column("name"))
print("\nFirst three rows:")
print(employee_table.slice(0, 3))


# TASK 4: Select Specific Columns

print("\n" + "="*60)
print("TASK 4: Select Specific Columns (name, department, salary)")
print("="*60)

selected_table = employee_table.select(["name", "department", "salary"])
print(selected_table)


# TASK 5: Filter Records (Salary > 50000)

print("\n" + "="*60)
print("TASK 5: Filter Employees with Salary > 50000")
print("="*60)

salary_filter = pc.greater(employee_table["salary"], 50000)
high_salary_table = employee_table.filter(salary_filter)
print(high_salary_table)


# TASK 6: Filter by Department (IT)

print("\n" + "="*60)
print("TASK 6: Filter IT Department Employees")
print("="*60)

department_filter = pc.equal(employee_table["department"], "IT")
it_employees = employee_table.filter(department_filter)
print(it_employees)


# TASK 7: Perform Calculations

print("\n" + "="*60)
print("TASK 7: Salary Calculations")
print("="*60)

salary_column = employee_table["salary"]
print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())


# TASK 8: Add a New Column (Bonus)

print("\n" + "="*60)
print("TASK 8: Add Bonus Column (10% of Salary)")
print("="*60)

bonus_column = pc.multiply(employee_table["salary"], 0.10)
employee_table = employee_table.append_column("bonus", bonus_column)
print("Table with Bonus Column:")
print(employee_table)


# TASK 9: Convert Arrow to Pandas

print("\n" + "="*60)
print("TASK 9: Convert Arrow to Pandas DataFrame")
print("="*60)

employee_df = employee_table.to_pandas()
print(employee_df)


# TASK 10: Convert Pandas to Arrow

print("\n" + "="*60)
print("TASK 10: Convert Pandas to Arrow Table")
print("="*60)

new_arrow_table = pa.Table.from_pandas(employee_df, preserve_index=False)
print(new_arrow_table)


# TASK 11: Save as Parquet File

print("\n" + "="*60)
print("TASK 11: Save as Parquet File")
print("="*60)

pq.write_table(employee_table, "employees.parquet")
print(" employees.parquet created successfully!")


# TASK 12: Read the Parquet File

print("\n" + "="*60)
print("TASK 12: Read Parquet File")
print("="*60)

loaded_table = pq.read_table("employees.parquet")
print("Data loaded from employees.parquet:")
print(loaded_table)


# TASK 13: Save as Arrow IPC File

print("\n" + "="*60)
print("TASK 13: Save as Arrow IPC File")
print("="*60)

with ipc.new_file("employees.arrow", employee_table.schema) as writer:
    writer.write_table(employee_table)
print(" employees.arrow created successfully!")


# TASK 14: Read the Arrow IPC File

print("\n" + "="*60)
print("TASK 14: Read Arrow IPC File")
print("="*60)

with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()
print("Data loaded from employees.arrow:")
print(ipc_table)


# BONUS TASKS

print("\n" + "="*60)
print("BONUS TASKS")
print("="*60)

# Bonus 1: Display employees who work in Delhi
print("\nBonus 1: Employees in Delhi")
delhi_filter = pc.equal(employee_table["city"], "Delhi")
delhi_employees = employee_table.filter(delhi_filter)
print(delhi_employees)

# Bonus 2: Display employees with salaries between 50000 and 65000
print("\nBonus 2: Employees with salary between 50000 and 65000")
salary_range_filter = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000)
)
range_employees = employee_table.filter(salary_range_filter)
print(range_employees)

# Bonus 3: Add annual_salary column (salary * 12)
print("\nBonus 3: Add Annual Salary Column")
annual_salary = pc.multiply(employee_table["salary"], 12)
employee_table = employee_table.append_column("annual_salary", annual_salary)
print(employee_table)

# Bonus 4: Save only IT employees to parquet
print("\nBonus 4: Save IT Employees to it_employees.parquet")
it_filter = pc.equal(employee_table["department"], "IT")
it_table = employee_table.filter(it_filter)
pq.write_table(it_table, "it_employees.parquet")
print(" it_employees.parquet created successfully!")
print(it_table)

# Bonus 5: Read only name and salary columns from Parquet
print("\nBonus 5: Read only name and salary columns from Parquet")
selected_columns = pq.read_table("employees.parquet", columns=["name", "salary"])
print(selected_columns)

# Bonus 6: Sort employees by salary highest to lowest
print("\nBonus 6: Employees sorted by salary (highest to lowest)")
sorted_indices = pc.sort_indices(employee_table, sort_keys=[("salary", "descending")])
sorted_table = employee_table.take(sorted_indices)
print(sorted_table)


# VERIFY ALL FILES CREATED

print("\n" + "="*60)
print("FILES CREATED")
print("="*60)

files = ['employees.parquet', 'employees.arrow', 'it_employees.parquet']
for file in files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f" {file} - {size:,} bytes")
    else:
        print(f" {file} - NOT FOUND")

