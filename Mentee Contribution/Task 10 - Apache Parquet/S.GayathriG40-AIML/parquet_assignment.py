import pandas as pd

# ------------------------------------------
# Task 1: Create Employee DataFrame
# ------------------------------------------

employee_data = {
    "employee_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "name": [
        "Arjun",
        "Sneha",
        "Karthik",
        "Meghana",
        "Rohit",
        "Ananya",
        "Vishal",
        "Keerthana",
        "Harsha",
        "Nithya"
    ],
    "department": [
        "Software Development",
        "Data Science",
        "Cyber Security",
        "Cloud Computing",
        "UI/UX Design",
        "Machine Learning",
        "DevOps",
        "Data Science",
        "Data Engineering",
        "DevOps"
    ],
    "salary": [
        72000,
        68000,
        58000,
        83000,
        47000,
        91000,
        62000,
        51000,
        76000,
        54000
    ]
}

employees_df = pd.DataFrame(employee_data)

print("=" * 60)
print("Employee Data")
print("=" * 60)
print(employees_df)

# ------------------------------------------
# Task 2: Save DataFrame as Parquet
# ------------------------------------------

employees_df.to_parquet(
    "employees.parquet",
    index=False
)

print("\nemployees.parquet has been created successfully.")

# ------------------------------------------
# Task 3: Read Parquet File
# ------------------------------------------

loaded_df = pd.read_parquet("employees.parquet")

print("\n" + "=" * 60)
print("Loaded Data From Parquet")
print("=" * 60)
print(loaded_df)

# ------------------------------------------
# Task 4: Basic Analysis
# ------------------------------------------

print("\n" + "=" * 60)
print("Employees with Salary Greater Than 50000")
print("=" * 60)

high_salary = loaded_df[loaded_df["salary"] > 50000]
print(high_salary)

average_salary = loaded_df["salary"].mean()

print("\nAverage Salary")
print(f"₹{average_salary:.2f}")

print("\nEmployee Count by Department")
department_count = loaded_df["department"].value_counts()
print(department_count)

# ------------------------------------------
# Task 5: Save Filtered Employees
# ------------------------------------------

high_salary.to_parquet(
    "high_salary_employees.parquet",
    index=False
)

print("\nhigh_salary_employees.parquet has been created successfully.")

# ------------------------------------------
# Bonus Task
# ------------------------------------------

print("\n" + "=" * 60)
print("Only Name and Salary Columns")
print("=" * 60)

selected_columns = pd.read_parquet(
    "employees.parquet",
    columns=["name", "salary"]
)

print(selected_columns)

print("\nAssignment Completed Successfully!")