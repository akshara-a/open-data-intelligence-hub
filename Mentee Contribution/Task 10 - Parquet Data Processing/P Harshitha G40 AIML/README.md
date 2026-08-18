# Python Parquet Assignment

## Objective

Learn how to create, save, read, and analyze a Parquet file using Python and Pandas.

## Requirements

Install the required libraries:

```bash
pip install pandas pyarrow
```

## Assignment Tasks

### Task 1: Create a DataFrame

Create a Pandas DataFrame with the following columns:

* `employee_id`
* `name`
* `department`
* `salary`

Add at least five employee records.

### Task 2: Save as Parquet

Save the DataFrame as a Parquet file named:

```text
employees.parquet
```

Do not save the DataFrame index.

### Task 3: Read the Parquet File

Read `employees.parquet` into a new DataFrame and display its contents.

### Task 4: Perform Basic Analysis

Using the loaded DataFrame:

1. Display employees with a salary greater than `50000`.
2. Calculate the average salary.
3. Display the number of employees in each department.

### Task 5: Save Filtered Data

Save employees with a salary greater than `50000` into another Parquet file named:

```text
high_salary_employees.parquet
```

## Solution Code

```python
import pandas as pd

# Task 1: Create the DataFrame
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employees_df = pd.DataFrame(data)

# Task 2: Save the DataFrame as a Parquet file
employees_df.to_parquet("employees.parquet", index=False)

# Task 3: Read the Parquet file
loaded_df = pd.read_parquet("employees.parquet")
print("=== All Employees ===")
print(loaded_df)

# Task 4: Perform the requested analysis
print("\n=== Employees with Salary > 50,000 ===")
high_salary_df = loaded_df[loaded_df["salary"] > 50000]
print(high_salary_df)

print("\n=== Average Salary ===")
print(loaded_df["salary"].mean())

print("\n=== Employee Count by Department ===")
print(loaded_df["department"].value_counts())

# Task 5: Save the filtered data
high_salary_df.to_parquet("high_salary_employees.parquet", index=False)

# Bonus Task: Read specific columns
bonus_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print("\n=== Bonus Task: Name and Salary Columns Only ===")
print(bonus_df)
```

## Submission Files

- `parquet_assignment.py`
- `employees.parquet`
- `high_salary_employees.parquet`
