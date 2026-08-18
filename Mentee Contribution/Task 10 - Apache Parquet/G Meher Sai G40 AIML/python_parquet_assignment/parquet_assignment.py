import pandas as pd

# Employee data
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

# --------------------------------------------------
# Task 1: Create the DataFrame
# --------------------------------------------------

employees_df = pd.DataFrame(data)

print("All Employee Records:")
print(employees_df)


# --------------------------------------------------
# Task 2: Save the DataFrame as a Parquet file
# --------------------------------------------------

employees_df.to_parquet(
    "employees.parquet",
    index=False,
    engine="pyarrow"
)

print("\nemployees.parquet created successfully.")


# --------------------------------------------------
# Task 3: Read the Parquet file
# --------------------------------------------------

loaded_df = pd.read_parquet(
    "employees.parquet",
    engine="pyarrow"
)

print("\nData Read from Parquet File:")
print(loaded_df)


# --------------------------------------------------
# Task 4: Perform Basic Analysis
# --------------------------------------------------

# Employees earning more than 50000
high_salary_df = loaded_df[loaded_df["salary"] > 50000]

print("\nEmployees with Salary Greater Than 50000:")
print(high_salary_df)


# Calculate average salary
average_salary = loaded_df["salary"].mean()

print("\nAverage Employee Salary:")
print(average_salary)


# Number of employees in each department
department_counts = loaded_df["department"].value_counts()

print("\nNumber of Employees in Each Department:")
print(department_counts)


# --------------------------------------------------
# Task 5: Save Filtered Data
# --------------------------------------------------

high_salary_df.to_parquet(
    "high_salary_employees.parquet",
    index=False,
    engine="pyarrow"
)

print("\nhigh_salary_employees.parquet created successfully.")


# --------------------------------------------------
# Bonus Task
# Read only name and salary columns
# --------------------------------------------------

name_salary_df = pd.read_parquet(
    "employees.parquet",
    columns=["name", "salary"],
    engine="pyarrow"
)

print("\nBonus Task - Name and Salary Columns:")
print(name_salary_df)