
"""
============================================================

Interview Question 13

What is Multicollinearity, and how does it affect
Regression?

Interview Answer

Multicollinearity occurs when two or more independent
variables are highly correlated with each other.

Example:

Area --------\
              \
               -----> House Price
              /
Square Feet --/

Both Area and Square Feet represent almost the same
information.

Effects of Multicollinearity

1. Unstable regression coefficients
2. Difficult to identify important features
3. Reduces model interpretability
4. Small changes in data can produce large coefficient
   changes

Solutions

1. Remove highly correlated features
2. Use Variance Inflation Factor (VIF)
3. Apply Ridge Regression
4. Perform Feature Selection

============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Create Dataset
# ----------------------------------------------------

data = {

    "Area": [
        1000,1200,1500,1800,2000,
        2200,2500,2700,3000,3200
    ],

    "Square_Feet": [
        990,1195,1495,1790,2010,
        2195,2490,2710,3010,3195
    ],

    "Bedrooms": [
        2,2,3,3,4,
        4,4,5,5,5
    ],

    "Age": [
        20,18,15,12,10,
        8,6,5,4,2
    ],

    "Price": [
        3000000,
        3400000,
        4200000,
        5000000,
        5600000,
        6100000,
        6900000,
        7500000,
        8200000,
        8800000
    ]

}

df = pd.DataFrame(data)

print("Dataset\n")
print(df)

# ----------------------------------------------------
# Correlation Matrix
# ----------------------------------------------------

correlation = df.corr()

print("\nCorrelation Matrix\n")
print(correlation)

# ----------------------------------------------------
# Find Highly Correlated Features
# ----------------------------------------------------

print("\nHighly Correlated Features")

columns = correlation.columns

for i in range(len(columns)):

    for j in range(i + 1, len(columns)):

        value = correlation.iloc[i, j]

        if abs(value) > 0.80:

            print(
                f"{columns[i]} <--> {columns[j]} : {value:.3f}"
            )

# ----------------------------------------------------
# Heatmap using Matplotlib
# ----------------------------------------------------

plt.figure(figsize=(8,6))

plt.imshow(
    correlation,
    cmap="coolwarm",
    interpolation="nearest"
)

plt.colorbar()

plt.xticks(
    range(len(columns)),
    columns,
    rotation=45
)

plt.yticks(
    range(len(columns)),
    columns
)

plt.title("Correlation Heatmap")

for i in range(len(columns)):

    for j in range(len(columns)):

        plt.text(
            j,
            i,
            f"{correlation.iloc[i,j]:.2f}",
            ha="center",
            va="center",
            fontsize=8
        )

plt.tight_layout()

plt.show()

# ----------------------------------------------------
# Interview Summary
# ----------------------------------------------------

print("\n------------------------------------")
print("Interview Summary")
print("------------------------------------")

print("""
Multicollinearity occurs when independent
variables are highly correlated.

Example:

Area and Square_Feet

These variables provide almost the same
information to the model.

This can make regression coefficients
unstable and difficult to interpret.
""")

# ----------------------------------------------------
# Suggestions
# ----------------------------------------------------

print("Possible Solutions")

print("------------------------")

print("1. Remove one correlated feature")

print("2. Calculate VIF")

print("3. Apply Ridge Regression")

print("4. Perform Feature Selection")