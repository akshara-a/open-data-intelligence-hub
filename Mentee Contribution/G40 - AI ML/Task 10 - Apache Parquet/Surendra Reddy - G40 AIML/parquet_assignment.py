import pandas as pd

# Task 1: Create the DataFrame
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employees_df = pd.DataFrame(data)
print("=== All Employee Records ===")
print(employees_df)
print()

# Task 2: Save the DataFrame as a Parquet file (without index)
employees_df.to_parquet("employees.parquet", index=False)
print("Saved employees.parquet successfully!\n")

# Task 3: Read the Parquet file into a new DataFrame
loaded_df = pd.read_parquet("employees.parquet")
print("=== Data Loaded from employees.parquet ===")
print(loaded_df)
print()

# Task 4: Perform basic analysis

# 4.1 Employees with salary > 50000
high_salary_df = loaded_df[loaded_df["salary"] > 50000]
print("=== Employees Earning More Than 50000 ===")
print(high_salary_df)
print()

# 4.2 Average salary
average_salary = loaded_df["salary"].mean()
print(f"=== Average Salary ===\n{average_salary}\n")

# 4.3 Number of employees per department
department_counts = loaded_df["department"].value_counts()
print("=== Employee Count by Department ===")
print(department_counts)
print()

# Task 5: Save filtered data (salary > 50000) as a separate Parquet file
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)
print("Saved high_salary_employees.parquet successfully!\n")

# Bonus Task: Read only 'name' and 'salary' columns from the Parquet file
bonus_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print("=== Bonus: Name and Salary Columns Only ===")
print(bonus_df)