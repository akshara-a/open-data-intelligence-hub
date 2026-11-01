import pandas as pd
import pyarrow

# ------------------------------------------------------------------
# 1. Create Employee Dataset
# ------------------------------------------------------------------
print("=" * 60)
print("1. ORIGINAL EMPLOYEE DATA")
print("=" * 60)

employee_data = {
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona"],
    "department": ["HR", "Engineering", "Engineering", "HR", "Marketing", "Engineering"],
    "salary": [48000, 72000, 68000, 91000, 51000, 95000]
}

df = pd.DataFrame(employee_data)
print(df)

# ------------------------------------------------------------------
# 2. Save Data as Parquet
# ------------------------------------------------------------------
df.to_parquet("employees.parquet", index=False)
print("\n[CONFIRMED] employees.parquet created successfully.")

# ------------------------------------------------------------------
# 3. Read the Parquet File
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("2. READ BACK FROM employees.parquet")
print("=" * 60)

df_read = pd.read_parquet("employees.parquet")
print(df_read)

# ------------------------------------------------------------------
# 4. Data Analysis
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("3. DATA ANALYSIS")
print("=" * 60)

filtered = df_read[df_read["salary"] > 50000]
print("\n--- Employees earning more than 50,000 ---")
print(filtered)

avg_salary = df_read["salary"].mean()
print(f"\nAverage salary: ${avg_salary:,.2f}")

dept_counts = df_read["department"].value_counts()
print("\n--- Employee count by department ---")
print(dept_counts)

# ------------------------------------------------------------------
# 5. Save Filtered Data
# ------------------------------------------------------------------
filtered.to_parquet("high_salary_employees.parquet", index=False)
print("\n[CONFIRMED] high_salary_employees.parquet created successfully.")

# ------------------------------------------------------------------
# 6. Bonus Task: Selected Columns
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. BONUS: SELECTED COLUMNS (name, salary)")
print("=" * 60)

bonus_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print(bonus_df)
