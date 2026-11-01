import pandas as pd

#  Read Parquet File
loaded_df = pd.read_parquet(
    "employee.parquet",
    engine="pyarrow"
)

print("\nData Read from Parquet File:")
print(loaded_df)

# T Perform Basic Analysis

# Employees earning 
high_salary_df = loaded_df[loaded_df["Salary"] > 60000]

print("\nEmployees with Salary Greater Than 60000:")
print(high_salary_df)


# Calculate average salary
average_salary = loaded_df["Salary"].mean()

print("\nAverage Employee Salary:")
print(average_salary)


# Number of employees in each department 
department_counts = loaded_df["Department"].value_counts()

print("\nNumber of Employees in Each Department:")
print(department_counts)



# Save Filtered Data

high_salary_df.to_parquet(
    "high_salary_employees.parquet",
    index=False,
    engine="pyarrow"
)

print("\nhigh_salary_employees.parquet created successfully.")

#  Read Specific Columns
name_salary_df = pd.read_parquet(
    "employee.parquet",
    columns=["Name", "Salary"],
    engine="pyarrow"
)

print("\nBonus Task - Name and Salary Columns:")
print(name_salary_df)
