import pandas as pd

# -------------------------------
# Task 1: Create Employee DataFrame
# -------------------------------

data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employees_df = pd.DataFrame(data)

print("=" * 60)
print("Employee DataFrame")
print("=" * 60)
print(employees_df)

# -------------------------------
# Task 2: Save as Parquet
# -------------------------------

employees_df.to_parquet(
    "employees.parquet",
    index=False
)

print("\nemployees.parquet created successfully.")

# -------------------------------
# Task 3: Read the Parquet File
# -------------------------------

employees = pd.read_parquet("employees.parquet")

print("\n" + "=" * 60)
print("Data Read from Parquet File")
print("=" * 60)
print(employees)

# -------------------------------
# Task 4.1: Employees with Salary > 50000
# -------------------------------

high_salary = employees[
    employees["salary"] > 50000
]

print("\n" + "=" * 60)
print("Employees with Salary Greater than 50000")
print("=" * 60)
print(high_salary)

# -------------------------------
# Task 4.2: Average Salary
# -------------------------------

average_salary = employees["salary"].mean()

print("\nAverage Salary:", average_salary)

# -------------------------------
# Task 4.3: Employees by Department
# -------------------------------

department_count = employees["department"].value_counts()

print("\nEmployees Count by Department")
print(department_count)

# -------------------------------
# Task 5: Save High Salary Employees
# -------------------------------

high_salary.to_parquet(
    "high_salary_employees.parquet",
    index=False
)

print("\nhigh_salary_employees.parquet created successfully.")

# -------------------------------
# Bonus Task
# -------------------------------

selected_columns = pd.read_parquet(
    "employees.parquet",
    columns=["name", "salary"]
)

print("\n" + "=" * 60)
print("Name and Salary Columns")
print("=" * 60)
print(selected_columns)

# -------------------------------
# Program Completed
# -------------------------------

print("\n" + "=" * 60)
print("Python Parquet Assignment Completed Successfully")
print("=" * 60)