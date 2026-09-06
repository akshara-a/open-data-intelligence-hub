import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000],
}

# Task 1: Create the DataFrame
employees_df = pd.DataFrame(data)

# Task 2: Save the DataFrame as a Parquet file
employees_df.to_parquet("employees.parquet", index=False)


# Task 3: Read the Parquet file
loaded_df = pd.read_parquet("employees.parquet")

print(loaded_df)


# Task 4: Perform the requested analysis
high_salary_df = loaded_df[loaded_df["salary"] > 50000]

print("\nEmployees with salary greater than 50000:")
print(high_salary_df)

average_salary = loaded_df["salary"].mean()

print("\nAverage salary:")
print(average_salary)

department_counts = loaded_df["department"].value_counts()

print("\nNumber of employees in each department:")
print(department_counts)


# Task 5: Save the filtered data
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)

# Bonus Task: Read only name and salary columns
selected_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])

print("\nName and salary:")
print(selected_df)
