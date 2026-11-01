import polars as pl

# Read CSV file
df = pl.read_csv("data.csv")

print("Dataset:")
print(df)

print("\nTotal Rows:")
print(df.height)

print("\nAverage Salary:")
print(df["Salary"].mean())

print("\nMaximum Salary:")
print(df["Salary"].max())

print("\nMinimum Salary:")
print(df["Salary"].min())