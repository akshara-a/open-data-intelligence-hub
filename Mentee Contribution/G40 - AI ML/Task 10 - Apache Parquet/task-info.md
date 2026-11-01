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

## Starter Code

```python
import pandas as pd

data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

# Task 1: Create the DataFrame
employees_df = pd.DataFrame(data)

# Task 2: Save the DataFrame as a Parquet file


# Task 3: Read the Parquet file


# Task 4: Perform the requested analysis


# Task 5: Save the filtered data
```

## Expected Output

Your program should display:

* All employee records
* Employees earning more than `50000`
* The average employee salary
* Employee counts by department

## Submission

Submit the following files:

```text
parquet_assignment.py
employees.parquet
high_salary_employees.parquet
```

## Bonus Task

Read only the `name` and `salary` columns from the Parquet file using the `columns` parameter.
