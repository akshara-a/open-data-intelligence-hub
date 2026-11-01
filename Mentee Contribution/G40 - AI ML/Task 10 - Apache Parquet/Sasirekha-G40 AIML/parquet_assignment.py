import pandas as pd

# Employee dataset
employee_data = {
    "employee_id": [101, 102, 103, 104, 105],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

# Create a DataFrame
employees = pd.DataFrame(employee_data)

print("\nEmployee Details")
print("-" * 40)
print(employees)

# Store the data in Parquet format
employees.to_parquet("employees.parquet", index=False)
print("\nParquet file created successfully.")

# Load the Parquet file
employee_records = pd.read_parquet("employees.parquet")

print("\nData Loaded from Parquet")
print("-" * 40)
print(employee_records)

# Find employees whose salary is greater than 50000
high_salary_employees = employee_records[employee_records["salary"] > 50000]

print("\nEmployees with Salary Greater Than 50000")
print("-" * 40)
print(high_salary_employees)

# Calculate the average salary
average_salary = employee_records["salary"].mean()

print(f"\nAverage Salary : {average_salary:.2f}")

# Count employees in each department
department_summary = employee_records["department"].value_counts()

print("\nEmployees by Department")
print("-" * 40)
print(department_summary)

# Save the filtered employees into another Parquet file
high_salary_employees.to_parquet(
    "high_salary_employees.parquet",
    index=False
)

print("\nHigh salary employee data saved successfully.")

# Read only selected columns
selected_columns = pd.read_parquet(
    "employees.parquet",
    columns=["name", "salary"]
)

print("\nEmployee Name and Salary")
print("-" * 40)
print(selected_columns)