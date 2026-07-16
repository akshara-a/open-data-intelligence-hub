
"""
========================================================

Interview Question 10

What is Adjusted R², and why is it useful?

Interview Answer

Adjusted R² is a modified version of the R² score that
takes into account the number of independent variables
(features) used in the regression model.

Unlike R², which always stays the same or increases when
new features are added, Adjusted R² increases only if the
new feature actually improves the model.

Formula:

Adjusted R² = 1 - [(1 - R²)(n - 1)] / (n - p - 1)

Where:

R² = R-squared Score
n  = Number of observations
p  = Number of independent variables

Advantages

1. Penalizes unnecessary features.
2. Helps compare regression models.
3. Prevents selecting overly complex models.
4. More reliable than R² when multiple features exist.

========================================================
"""

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# -----------------------------------------------------
# Read Dataset
# -----------------------------------------------------

df = pd.read_csv("r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\house_price.csv")

print("Dataset\n")
print(df)

# -----------------------------------------------------
# Features and Target
# -----------------------------------------------------

X = df[["Area", "Bedrooms", "Age"]]

y = df["Price"]

# -----------------------------------------------------
# Train Model
# -----------------------------------------------------

model = LinearRegression()

model.fit(X, y)

# -----------------------------------------------------
# Predictions
# -----------------------------------------------------

predictions = model.predict(X)

# -----------------------------------------------------
# Calculate R²
# -----------------------------------------------------

r2 = r2_score(y, predictions)

# -----------------------------------------------------
# Calculate Adjusted R²
# -----------------------------------------------------

n = len(y)

p = X.shape[1]

adjusted_r2 = 1 - ((1 - r2) * (n - 1)) / (n - p - 1)

# -----------------------------------------------------
# Display Results
# -----------------------------------------------------

print("\nNumber of Observations (n)")
print(n)

print("\nNumber of Features (p)")
print(p)

print("\nR² Score")
print(r2)

print("\nAdjusted R²")
print(adjusted_r2)

# -----------------------------------------------------
# Comparison Table
# -----------------------------------------------------

comparison = pd.DataFrame({

    "Area": df["Area"],

    "Bedrooms": df["Bedrooms"],

    "Age": df["Age"],

    "Actual Price": y,

    "Predicted Price": predictions

})

print("\nComparison Table\n")

print(comparison)

# -----------------------------------------------------
# Manual Formula Display
# -----------------------------------------------------

print("\nFormula Used")
print("---------------------------------------")
print("Adjusted R² = 1 - ((1 - R²)(n - 1)) / (n - p - 1)")

# -----------------------------------------------------
# Interview Interpretation
# -----------------------------------------------------

print("\nInterview Interpretation")
print("---------------------------------------")

print(f"R² Score          : {r2:.4f}")

print(f"Adjusted R² Score : {adjusted_r2:.4f}")

if adjusted_r2 >= 0.90:
    print("\nExcellent model with useful features.")

elif adjusted_r2 >= 0.75:
    print("\nGood regression model.")

elif adjusted_r2 >= 0.50:
    print("\nAverage regression model.")

else:
    print("\nModel needs improvement.")

# -----------------------------------------------------
# Difference Between R² and Adjusted R²
# -----------------------------------------------------

print("\nDifference")

print("---------------------------------------")

print("R² always stays the same or increases when")
print("new features are added.")

print()

print("Adjusted R² increases only if the added")
print("feature improves the model.")

print()

print("Otherwise, Adjusted R² decreases.")