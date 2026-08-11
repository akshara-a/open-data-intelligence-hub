import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

# Task 1: Create the DataFrame
employees_df = pd.DataFrame(data)
print("=== Task 1: Employee DataFrame ===")
print(employees_df)
print()

# Task 2: Save the DataFrame as a Parquet file
employees_df.to_parquet("employees.parquet", index=False)
print("=== Task 2: Saved DataFrame to employees.parquet ===")
print()

# Task 3: Read the Parquet file
loaded_df = pd.read_parquet("employees.parquet")
print("=== Task 3: Data loaded from employees.parquet ===")
print(loaded_df)
print()

# Task 4: Perform the requested analysis
print("=== Task 4: Analysis ===")

# 1. Employees with salary greater than 50000
high_salary_df = loaded_df[loaded_df["salary"] > 50000]
print("\nEmployees with salary > 50000:")
print(high_salary_df)

# 2. Average salary
average_salary = loaded_df["salary"].mean()
print(f"\nAverage salary: {average_salary}")

# 3. Number of employees in each department
department_counts = loaded_df["department"].value_counts()
print("\nNumber of employees per department:")
print(department_counts)
print()

# Task 5: Save the filtered data
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)
print("=== Task 5: Saved filtered data to high_salary_employees.parquet ===")
print()

# Bonus Task: Read only 'name' and 'salary' columns
print("=== Bonus Task: name and salary columns only ===")
name_salary_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print(name_salary_df)
