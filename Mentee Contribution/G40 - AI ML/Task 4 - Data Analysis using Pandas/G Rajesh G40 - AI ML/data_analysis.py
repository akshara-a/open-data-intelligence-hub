import pandas as pd

df = pd.read_csv("data/species_data.csv")

print("Dataset:")
print(df)

print("\nTotal Species:")
print(df["species"].nunique())

print("\nTotal Observations:")
print(df["count"].sum())