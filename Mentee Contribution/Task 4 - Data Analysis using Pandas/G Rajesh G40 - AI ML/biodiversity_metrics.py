import pandas as pd
import math

df = pd.read_csv("data/species_data.csv")

total_count = df["count"].sum()

shannon_index = 0

for count in df["count"]:
    p = count / total_count
    shannon_index -= p * math.log(p)

print("Shannon Diversity Index:", round(shannon_index, 4))