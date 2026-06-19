import pandas as pd

# Load dataset
df = pd.read_csv("dataset.csv")

print("=" * 50)
print("STUDENT PERFORMANCE ANALYSIS")
print("=" * 50)

# Dataset overview
print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())

# Average scores
print("\nAverage Subject Scores:")
print(df[["Math_Score", "Science_Score", "English_Score"]].mean())

# Add overall average column
df["Average_Score"] = df[
    ["Math_Score", "Science_Score", "English_Score"]
].mean(axis=1)

# Top performer
top_student = df.loc[df["Average_Score"].idxmax()]

print("\nTop Performer:")
print(top_student[["Name", "Average_Score"]])

# Gender-wise average
print("\nGender-wise Average Scores:")
print(df.groupby("Gender")["Average_Score"].mean())

# Attendance statistics
print("\nAttendance Statistics:")
print(df["Attendance"].describe())

print("\nAnalysis Completed Successfully!")