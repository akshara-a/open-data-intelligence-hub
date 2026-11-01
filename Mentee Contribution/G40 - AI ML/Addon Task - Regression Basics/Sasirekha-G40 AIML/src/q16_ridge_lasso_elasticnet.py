"""
============================================================

Interview Question 14

How can Multicollinearity be detected?

Interview Answer

Multicollinearity can be detected using:

1. Correlation Matrix
2. Heatmap
3. Variance Inflation Factor (VIF)

The most common interview answer is VIF.

What is VIF?

VIF (Variance Inflation Factor) measures how much the
variance of a regression coefficient is increased due to
multicollinearity.

VIF Formula

            1
VIF = ----------------
      (1 - R²)

where R² is obtained by regressing one independent
variable against all the remaining independent variables.

Interpretation

VIF = 1
No correlation.

VIF = 1 - 5
Moderate correlation.

VIF > 5
High multicollinearity.

VIF > 10
Very serious multicollinearity.

============================================================
"""

import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ---------------------------------------------------------
# Create Dataset
# ---------------------------------------------------------

data = {

    "Area": [
        1000,1200,1500,1800,2000,
        2200,2500,2700,3000,3200
    ],

    "Square_Feet": [
        995,1198,1497,1798,1995,
        2205,2495,2705,3002,3198
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

# ---------------------------------------------------------
# Select Independent Variables
# ---------------------------------------------------------

X = df[["Area", "Square_Feet", "Bedrooms", "Age"]]

print("\nIndependent Variables\n")
print(X)

# ---------------------------------------------------------
# Calculate VIF
# ---------------------------------------------------------

vif = pd.DataFrame()

vif["Feature"] = X.columns

vif["VIF"] = [

    variance_inflation_factor(
        X.values,
        i
    )

    for i in range(X.shape[1])

]

print("\nVariance Inflation Factor\n")
print(vif)

# ---------------------------------------------------------
# Interpretation
# ---------------------------------------------------------

print("\n------------------------------------")
print("Feature Interpretation")
print("------------------------------------")

for feature, value in zip(vif["Feature"], vif["VIF"]):

    print(f"\nFeature : {feature}")

    print(f"VIF     : {value:.2f}")

    if value == 1:

        print("No multicollinearity")

    elif value < 5:

        print("Moderate correlation")

    elif value < 10:

        print("High multicollinearity")

    else:

        print("Very High Multicollinearity")

# ---------------------------------------------------------
# Sort Features
# ---------------------------------------------------------

print("\n------------------------------------")
print("Features Sorted by VIF")
print("------------------------------------")

print(

    vif.sort_values(
        by="VIF",
        ascending=False
    )

)

# ---------------------------------------------------------
# Interview Summary
# ---------------------------------------------------------

print("\n------------------------------------")
print("Interview Summary")
print("------------------------------------")

print("""

Variance Inflation Factor (VIF) is the most common
technique used to detect multicollinearity.

A high VIF indicates that an independent variable
contains information already explained by the other
independent variables.

High VIF values make regression coefficients unstable.

Possible Solutions

1. Remove highly correlated features

2. Feature Engineering

3. Ridge Regression

4. Principal Component Analysis (PCA)

""")