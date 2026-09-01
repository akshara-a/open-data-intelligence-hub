import pandas as pd

# ---------------------------------------------------------
# Task 1: Create a DataFrame
# ---------------------------------------------------------
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employees_df = pd.DataFrame(data)
print("Task 1 Completed: DataFrame created.\n")

# ---------------------------------------------------------
# Task 2: Save as Parquet (do not save index)
# ---------------------------------------------------------
employees_df.to_parquet("employees.parquet", index=False)
print("Task 2 Completed: Saved 'employees.parquet'.\n")

# ---------------------------------------------------------
# Task 3: Read the Parquet File
# ---------------------------------------------------------
loaded_df = pd.read_parquet("employees.parquet")

print("--- Task 3: Loaded DataFrame Contents ---")
print(loaded_df)
print("\n")

# ---------------------------------------------------------
# Task 4: Perform Basic Analysis
# ---------------------------------------------------------
# 1. Employees with salary > 50000
high_salary_df = loaded_df[loaded_df["salary"] > 50000]
print("--- Task 4.1: Employees earning > 50,000 ---")
print(high_salary_df)
print("\n")

# 2. Average salary
avg_salary = loaded_df["salary"].mean()
print("--- Task 4.2: Average Salary ---")
print(f"Average Salary: ${avg_salary:,.2f}\n")

# 3. Number of employees in each department
dept_counts = loaded_df["department"].value_counts()
print("--- Task 4.3: Department-wise Employee Count ---")
print(dept_counts)
print("\n")

# ---------------------------------------------------------
# Task 5: Save Filtered Data (Salary > 50000)
# ---------------------------------------------------------
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)
print("Task 5 Completed: Saved 'high_salary_employees.parquet'.\n")

# ---------------------------------------------------------
# Bonus Task: Read only 'name' and 'salary' columns
# ---------------------------------------------------------
bonus_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print("--- Bonus Task: Selected Columns ('name', 'salary') ---")
print(bonus_df)