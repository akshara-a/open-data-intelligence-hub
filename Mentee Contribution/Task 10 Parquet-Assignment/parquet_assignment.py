import pandas as pd

# Task 1: Create a DataFrame
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employees_df = pd.DataFrame(data)
print("=== Task 1 & 3: Loaded DataFrame ===")
print(employees_df)

# Task 2: Save as Parquet file named employees.parquet (without index)
employees_df.to_parquet("employees.parquet", index=False)
print("\n[Task 2] Saved DataFrame to 'employees.parquet'")

# Task 3: Read the Parquet File
loaded_df = pd.read_parquet("employees.parquet")
print("\n=== Task 3: Read contents from 'employees.parquet' ===")
print(loaded_df)

# Task 4: Perform Basic Analysis
print("\n=== Task 4: Basic Analysis ===")

# 1. Employees with salary > 50000
high_salary_df = loaded_df[loaded_df["salary"] > 50000]
print("\nEmployees with salary > 50,000:")
print(high_salary_df)

# 2. Calculate average salary
avg_salary = loaded_df["salary"].mean()
print(f"\nAverage Salary: {avg_salary}")

# 3. Display number of employees in each department
dept_counts = loaded_df["department"].value_counts()
print("\nEmployee count by department:")
print(dept_counts)

# Task 5: Save Filtered Data
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)
print("\n[Task 5] Saved high salary employees to 'high_salary_employees.parquet'")

# Bonus Task: Read only 'name' and 'salary' columns using columns parameter
bonus_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print("\n=== Bonus Task: Reading only 'name' and 'salary' columns ===")
print(bonus_df)
