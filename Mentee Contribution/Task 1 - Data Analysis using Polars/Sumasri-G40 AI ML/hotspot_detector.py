# hotspot_detector.py

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load dataset
df = pd.read_csv("data/antarctic_data.csv")

# Step 2: Process data
print(df.head())

# Step 3: Create graph
plt.figure(figsize=(10,5))
plt.plot([1,2,3,4,5], [10,20,15,25,30])
plt.title("Biodiversity Hotspot Analysis")
plt.savefig("static/graphs/hotspot_graph.png")

print("Graph created successfully")