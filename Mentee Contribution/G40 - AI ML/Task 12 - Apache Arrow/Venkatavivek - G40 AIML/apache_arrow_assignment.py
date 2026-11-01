import pyarrow as pa
import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

#task1

employee_table = pa.table(data)

print(employee_table)

#task2

print(employee_table.schema)

#task3
print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print(employee_table.column("name"))
print(employee_table.slice(0, 3))


#TASK 4

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print(selected_table)

#task5

import pyarrow.compute as pc

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(salary_filter)

print(high_salary_table)

#TASK 6
department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(department_filter)

print(it_employees)

#TAsk 7salary_column = employee_table["salary"]

salary_column = employee_table["salary"]

print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())


#Task 8
bonus_column=pc.multiply(
    employee_table['salary'],0.1    
)
employee_table=employee_table.append_column(
    'bonus',
    bonus_column
)

print(employee_table)

#Task 9
employee_df=employee_table.to_pandas()
print(employee_df)


#Task 10
new_arrow_table =pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)
print(new_arrow_table)


#task11
import pyarrow.parquet as pq
pq.write_table(
    employee_table,
    "employees.parquet"
)
print("Parquet file created successfully")


#TASK 12

loaded_table=pq.read_table('employees.parquet')

print(loaded_table)


#Task 13

import pyarrow.ipc as ipc

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:
    writer.write_table(employee_table)

print("Arrow IPC file created successfully.")

#Task 14

with ipc.open_file('employees.arrow') as reader:
    ipc_table = reader.read_all()



#Bonus tasks

#Task a
delhi_emp=pc.equal(
    ipc_table['name'],
    'Delhi'    
)

delhi_emp_table = ipc_table.filter(delhi_emp)

print(delhi_emp_table)

#task b
salary_condition=pc.and_(
    pc.greater_equal(ipc_table['salary'],50000),
    pc.less_equal(ipc_table['salary'],65000)
)
salary_range_emp=ipc_table.filter(salary_condition)
print(salary_range_emp)


#task c

annual_salary=pc.multiply(
    ipc_table['salary'],
    12
)

ipc_table=ipc_table.append_column("annual_salary",annual_salary)

#task d

it_filter=pc.equal(ipc_table['department'],'IT')
it_emp=ipc_table.filter(it_filter)

pq.write_table(it_employees,"it_employees.parquet")

print("IT employees saved to  it_employees_parquet")


#task e

selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"])
print(selected_columns)

#task f

sorted_table=ipc_table.sort_by([("salary","descending")])
print(sorted_table)







