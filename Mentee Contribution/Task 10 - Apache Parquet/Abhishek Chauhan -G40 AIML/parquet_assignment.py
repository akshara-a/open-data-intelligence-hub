import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

# Creating the DataFrame
employees_df = pd.DataFrame(data)
print("All employee records:")
print(employees_df)
print()

# Saving the DataFrame as a Parquet file
employees_df.to_parquet("employees.parquet", index=False)

# Read the Parquet file
loaded_df = pd.read_parquet("employees.parquet")
print("Employees loaded from employees.parquet:")
print(loaded_df)
print()

# Performing analysis

# Employees earning more than 50000
high_salary_df = loaded_df[loaded_df["salary"] > 50000]
print("Employees with salary greater than 50000:")
print(high_salary_df)
print()

# Average salary
average_salary = loaded_df["salary"].mean()
print(f"Average salary: {average_salary:.2f}")
print()

# Employee counts by department
department_counts = loaded_df["department"].value_counts()
print("Number of employees per department:")
print(department_counts)
print()

# Saving the filtered data
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)

#Read only the 'name' and 'salary' columns
name_salary_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print("Name and salary columns only (bonus task):")
print(name_salary_df)
