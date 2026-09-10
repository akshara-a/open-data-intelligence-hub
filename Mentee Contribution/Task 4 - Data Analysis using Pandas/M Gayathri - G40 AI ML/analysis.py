import pandas as pd

df = pd.read_csv("data/dataset.csv")

print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nThreat Counts:")
print(df["primary_threat"].value_counts())
