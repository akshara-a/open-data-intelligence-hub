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


# Task 2: Save as Parquet

employees_df.to_parquet(
    "employees.parquet",
    index=False
)

print("\nemployees.parquet created successfully!")


# Task 3: Read the Parquet file

loaded_df = pd.read_parquet("employees.parquet")

print("\n=== Data from employees.parquet ===")
print(loaded_df)


# Task 4.1: Employees with salary greater than 50000

high_salary_df = loaded_df[loaded_df["salary"] > 50000]

print("\n=== Employees earning more than 50000 ===")
print(high_salary_df)


# Task 4.2: Average salary

average_salary = loaded_df["salary"].mean()

print("\n=== Average Salary ===")
print(average_salary)


# Task 4.3: Employee count by department

department_counts = loaded_df["department"].value_counts()

print("\n=== Employees in Each Department ===")
print(department_counts)


# Task 5: Save filtered employees

high_salary_df.to_parquet(
    "high_salary_employees.parquet",
    index=False
)

print("\nhigh_salary_employees.parquet created successfully!")


# Bonus Task

bonus_df = pd.read_parquet(
    "employees.parquet",
    columns=["name", "salary"]
)

print("\n=== Bonus: Name and Salary Only ===")
print(bonus_df)