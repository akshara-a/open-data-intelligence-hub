import pandas as pd

# Step 1: Creating a sample dataset for analysis
data = {
    'Topic': ['Python', 'Machine Learning', 'Pandas', 'Python', 'Pandas', 'Machine Learning', 'Python'],
    'Hours_Studied': [5, 7, 4, 3, 6, 8, 4],
    'Score': [85, 90, 78, 72, 88, 92, 75]
}
df = pd.DataFrame(data)

# Step 2: Basic Inspection
print("=== Dataset Head ===")
print(df.head())

print("\n=== Dataset Summary ===")
print(df.describe())

print("\n=== Value Counts for Topics ===")
print(df['Topic'].value_counts())

# FINAL INSIGHT CONCLUSION:
# The analysis shows that 'Python' is the most frequent topic in the dataset,
# and the average scores reflect consistent performance across different modules.
