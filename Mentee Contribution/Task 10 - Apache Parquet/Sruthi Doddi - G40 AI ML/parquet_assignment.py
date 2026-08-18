import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

# Task 1: Create the DataFrame
employees_df = pd.DataFrame(data)
print("Employee Records:")
print(employees_df)
print("\n" + "="*50 + "\n")

# Task 2: Save as Parquet
employees_df.to_parquet('employees.parquet', index=False)
print("Saved as employees.parquet")
print("\n" + "="*50 + "\n")

# Task 3: Read Parquet File
loaded_data = pd.read_parquet('employees.parquet')
print("Data loaded from employees.parquet:")
print(loaded_data)
print("\n" + "="*50 + "\n")

# Task 4.1: Filter Salary > 50000
high_salary = loaded_data[loaded_data['salary'] > 50000]
print("Employees with salary > 50000:")
print(high_salary)
print("\n")

# Task 4.2: Calculate Average Salary
avg_salary = loaded_data['salary'].mean()
print("Average Salary:", avg_salary)
print("\n")

# Task 4.3: Count by Department
dept_count = loaded_data['department'].value_counts()
print("Employees by Department:")
print(dept_count)
print("\n" + "="*50 + "\n")

# Task 5: Save Filtered Data
high_salary.to_parquet('high_salary_employees.parquet', index=False)
print("Saved filtered data as high_salary_employees.parquet")
print("\n" + "="*50 + "\n")

# Bonus Task: Read Only Name and Salary
name_salary = pd.read_parquet('employees.parquet', columns=['name', 'salary'])
print("Only Name and Salary columns:")
print(name_salary)
print("\n" + "="*50 + "\n")

# Verify Files Created
import os
print("Files created:")
print("- employees.parquet:", os.path.exists('employees.parquet'))
print("- high_salary_employees.parquet:", os.path.exists('high_salary_employees.parquet'))