import pandas as pd
import matplotlib.pyplot as plt
import os

# create folders
os.makedirs("output/charts", exist_ok=True)

# load data
df = pd.read_csv("data/student_data.csv")

print("\nFIRST 5 ROWS")
print(df.head())

print("\nDATA INFO")
print(df.info())

print("\nSUMMARY")
print(df.describe())

# check null values
print("\nNULL VALUES")
print(df.isnull().sum())

# remove duplicates
df = df.drop_duplicates()

# save cleaned data
df.to_csv("output/cleaned_data.csv", index=False)

# summary statistics
summary = df.describe()
summary.to_csv("output/summary_statistics.csv")

# average marks department wise
print("\nAVERAGE MARKS BY DEPARTMENT")
print(df.groupby("Department")["Marks"].mean())

# gender count
print("\nGENDER COUNT")
print(df["Gender"].value_counts())

# highest scorer
highest = df.loc[df["Marks"].idxmax()]
print("\nTOPPER")
print(highest)

# attendance average
print("\nAVERAGE ATTENDANCE")
print(df["Attendance"].mean())

# graph 1
plt.figure(figsize=(6,4))
df["Gender"].value_counts().plot(kind='bar')
plt.title("Gender Distribution")
plt.savefig("output/charts/gender_chart.png")
plt.close()

# graph 2
plt.figure(figsize=(6,4))
df["Department"].value_counts().plot(kind='bar')
plt.title("Department Distribution")
plt.savefig("output/charts/department_chart.png")
plt.close()

print("\nTask completed successfully.")