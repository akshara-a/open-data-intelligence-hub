import pandas as pd

df = pd.read_csv("data/urbanization_data.csv")

# Population Density
df["Density"] = df["Population"] / df["Area_km2"]

print(df)

# Average Population
avg_pop = df.groupby("City")["Population"].mean()

print("\nAverage Population")
print(avg_pop)