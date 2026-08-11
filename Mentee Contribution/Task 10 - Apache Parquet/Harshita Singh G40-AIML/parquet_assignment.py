import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

# Task 1: Create the DataFrame
employees_df = pd.DataFrame(data)
print("All employee records:")
print(employees_df, "\n")

# Task 2: Save the DataFrame as a Parquet file
employees_df.to_parquet("employees.parquet", index=False)

# Task 3: Read the Parquet file
loaded_df = pd.read_parquet("employees.parquet")
print("Loaded employee records:")
print(loaded_df, "\n")

# Task 4: Perform the requested analysis
high_salary_df = loaded_df[loaded_df["salary"] > 50000]
print("Employees earning more than 50000:")
print(high_salary_df, "\n")

average_salary = loaded_df["salary"].mean()
print(f"Average salary: {average_salary:.2f}\n")

department_counts = loaded_df["department"].value_counts()
print("Employee count by department:")
print(department_counts, "\n")

# Task 5: Save the filtered data
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)

# Bonus Task: Read only name and salary columns
name_salary_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print("Name and salary columns only:")
print(name_salary_df)
