import pandas as pd

#Task 1
data = {
    "employee_id": [1, 2, 3, 4, 5],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya"],
    "department": ["IT", "HR", "IT", "Finance", "HR"],
    "salary": [60000, 45000, 70000, 55000, 48000]
}

employee_df=pd.DataFrame(data)

print("Original Dataframe")
print(employee_df,"\n")

#Task2
employee_df.to_parquet("employees.parquet") 


#Task3

loaded_df=pd.read_parquet("employees.parquet")
print("Loaded dataframe from the parquet")
print(loaded_df,"\n")

#Task4
#Employees with high salary>50000
high_salary_df=loaded_df[loaded_df['salary']>50000]
print(" Employees with salary > 50000:")
print(high_salary_df)
print("\n")

#Avg salary
avg_salary=loaded_df["salary"].mean()
print(" Average Salary: ",avg_salary)
print("\n")

#3 Employee count by department
dept_counts=loaded_df['department'].value_counts()
print("Employee count by department:")
print(dept_counts)
print("\n")

#Task5

high_salary_df.to_parquet("high_salary_employees.parquet",index=False)


#Bonus Task

print(" Bonus: Read only name and salary columns:")
selected_columns_df = pd.read_parquet("employees.parquet", columns=["name", "salary"])
print(selected_columns_df)