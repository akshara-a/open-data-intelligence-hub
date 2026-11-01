import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/species_data.csv")

plt.bar(df["species"], df["count"])

plt.title("Species Distribution")
plt.xlabel("Species")
plt.ylabel("Count")

plt.show()