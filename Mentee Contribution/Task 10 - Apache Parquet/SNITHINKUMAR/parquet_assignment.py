import pandas as pd
from pathlib import Path

# Store output files in the same folder as this Python script
BASE_DIR = Path(__file__).resolve().parent
EMPLOYEES_FILE = BASE_DIR / "employees.parquet"
HIGH_SALARY_FILE = BASE_DIR / "high_salary_employees.parquet"

# Task 1: Create a DataFrame
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employees_df = pd.DataFrame(data)

print("Original Employee Data:")
print(employees_df)

# Task 2: Save the DataFrame as a Parquet file
employees_df.to_parquet(EMPLOYEES_FILE, index=False)

print("\nemployees.parquet created successfully.")

# Task 3: Read the Parquet file
loaded_df = pd.read_parquet(EMPLOYEES_FILE)

print("\nEmployee Data Read From Parquet:")
print(loaded_df)

# Task 4.1: Employees with salary greater than 50000
high_salary_df = loaded_df[loaded_df["salary"] > 50000]

print("\nEmployees with Salary Greater Than 50000:")
print(high_salary_df)

# Task 4.2: Calculate average salary
average_salary = loaded_df["salary"].mean()

print("\nAverage Employee Salary:")
print(average_salary)

# Task 4.3: Number of employees in each department
department_counts = loaded_df["department"].value_counts()

print("\nNumber of Employees in Each Department:")
print(department_counts)

# Task 5: Save filtered data
high_salary_df.to_parquet(HIGH_SALARY_FILE, index=False)

print("\nhigh_salary_employees.parquet created successfully.")

# Bonus Task: Read only name and salary columns
bonus_df = pd.read_parquet(
    EMPLOYEES_FILE,
    columns=["name", "salary"]
)

print("\nBonus - Name and Salary Columns:")
print(bonus_df)