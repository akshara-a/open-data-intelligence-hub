import pandas as pd

# Task 1: Create DataFrame
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employees_df = pd.DataFrame(data)

print("All Employee Records:")
print(employees_df)

# Task 2: Save as Parquet
employees_df.to_parquet("employees.parquet", index=False)
print("\nSaved employees.parquet")

# Task 3: Read Parquet
loaded_df = pd.read_parquet("employees.parquet")

print("\nLoaded Data:")
print(loaded_df)

# Task 4: Analysis
high_salary = loaded_df[loaded_df["salary"] > 50000]

print("\nEmployees with salary greater than 50000:")
print(high_salary)

average_salary = loaded_df["salary"].mean()

print("\nAverage Salary:")
print(average_salary)

department_count = loaded_df["department"].value_counts()

print("\nEmployees in each Department:")
print(department_count)

# Task 5: Save filtered data
high_salary.to_parquet("high_salary_employees.parquet", index=False)

print("\nSaved high_salary_employees.parquet")

# Bonus Task
selected_columns = pd.read_parquet(
    "employees.parquet",
    columns=["name", "salary"]
)

print("\nBonus Task (Name and Salary):")
print(selected_columns)