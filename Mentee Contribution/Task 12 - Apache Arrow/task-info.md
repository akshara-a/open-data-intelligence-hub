# Apache Arrow Assignment Using Python

## Objective

Learn how to create, inspect, filter, convert, and save tabular data using Apache Arrow and Python.

## Requirements

Install the required libraries:

```bash
pip install pyarrow pandas
```

## Dataset

Use the following employee data:

| employee_id | name   | department | salary | city      |
| ----------- | ------ | ---------- | ------ | --------- |
| 1           | Asha   | IT         | 60000  | Delhi     |
| 2           | Rahul  | HR         | 45000  | Mumbai    |
| 3           | Neha   | IT         | 70000  | Bengaluru |
| 4           | Vikram | Finance    | 55000  | Delhi     |
| 5           | Priya  | HR         | 48000  | Mumbai    |
| 6           | Arjun  | Finance    | 65000  | Chennai   |

## Task 1: Create an Arrow Table

Create a PyArrow table using the employee data.

```python
import pyarrow as pa

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)

print(employee_table)
```

## Task 2: Display the Schema

Display the schema of the Arrow table.

```python
print(employee_table.schema)
```

Answer the following questions:

1. What is the data type of `employee_id`?
2. What is the data type of `name`?
3. What is the data type of `salary`?

## Task 3: Inspect the Table

Display:

1. Number of rows
2. Number of columns
3. Column names
4. The `name` column
5. The first three rows

```python
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print(employee_table.column("name"))
print(employee_table.slice(0, 3))
```

## Task 4: Select Specific Columns

Create a new Arrow table containing only:

* `name`
* `department`
* `salary`

```python
selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print(selected_table)
```

## Task 5: Filter Records

Display employees whose salary is greater than `50000`.

```python
import pyarrow.compute as pc

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(salary_filter)

print(high_salary_table)
```

## Task 6: Filter by Department

Display employees from the `IT` department.

```python
department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print(it_employees)
```

## Task 7: Perform Calculations

Calculate:

1. Average salary
2. Maximum salary
3. Minimum salary
4. Total salary

```python
salary_column = employee_table["salary"]

print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())
```

## Task 8: Add a New Column

Add a new column named `bonus`.

The bonus should be 10% of the employee salary.

```python
bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print(employee_table)
```

## Task 9: Convert Arrow to Pandas

Convert the Arrow table into a Pandas DataFrame.

```python
employee_df = employee_table.to_pandas()

print(employee_df)
```

## Task 10: Convert Pandas to Arrow

Convert the Pandas DataFrame back into an Arrow table.

```python
new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print(new_arrow_table)
```

## Task 11: Save as a Parquet File

Save the Arrow table as:

```text
employees.parquet
```

```python
import pyarrow.parquet as pq

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("Parquet file created successfully.")
```

## Task 12: Read the Parquet File

Read `employees.parquet` using PyArrow.

```python
loaded_table = pq.read_table(
    "employees.parquet"
)

print(loaded_table)
```

## Task 13: Save as an Arrow IPC File

Save the table in Apache Arrow IPC file format.

Use the filename:

```text
employees.arrow
```

```python
import pyarrow.ipc as ipc

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("Arrow IPC file created successfully.")
```

## Task 14: Read the Arrow IPC File

Read and display the contents of `employees.arrow`.

```python
with ipc.open_file("employees.arrow") as reader:
    ipc_table = reader.read_all()

print(ipc_table)
```

## Bonus Tasks

1. Display employees who work in Delhi.
2. Display employees with salaries between `50000` and `65000`.
3. Add a column named `annual_salary` by multiplying salary by `12`.
4. Save only IT employees to `it_employees.parquet`.
5. Read only the `name` and `salary` columns from the Parquet file.
6. Sort employees by salary from highest to lowest.

Example for reading selected columns:

```python
selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print(selected_columns)
```

## Submission Files

Submit the following files:

```text
apache_arrow_assignment.py
employees.parquet
employees.arrow
```

## Expected Learning Outcomes

After completing this assignment, you should be able to:

* Create Apache Arrow tables
* Inspect table schemas
* Select and filter Arrow data
* Perform calculations using Arrow Compute
* Add new columns
* Convert between Arrow and Pandas
* Read and write Parquet files
* Read and write Arrow IPC files
