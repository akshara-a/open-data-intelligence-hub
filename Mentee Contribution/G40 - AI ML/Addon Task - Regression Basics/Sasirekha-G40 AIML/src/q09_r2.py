"""
========================================================

Interview Question 9

What is the R-squared (R²) Score, and how should it be
interpreted?

Interview Answer

R² (R-squared) is a regression evaluation metric that
measures how well the regression model explains the
variation in the dependent variable.

Formula:

R² = 1 - (SSR / SST)

Where:

SSR = Sum of Squared Residuals
SST = Total Sum of Squares

Interpretation:

R² = 1.0
Perfect prediction.

R² = 0.90
The model explains 90% of the variation in the target.

R² = 0
The model performs no better than predicting the mean.

R² < 0
The model performs worse than simply predicting the
average value.

Higher R² generally indicates a better model.

========================================================
"""

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# -----------------------------------------------------
# Read Dataset
# -----------------------------------------------------

df = pd.read_csv("../data/salary_data.csv")

print("r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\n")
print(df)

# -----------------------------------------------------
# Features and Target
# -----------------------------------------------------

X = df[["Experience"]]
y = df["Salary"]

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
# Manual R² Calculation
# -----------------------------------------------------

# Mean of actual values
mean_y = np.mean(y)

# Total Sum of Squares (SST)
sst = np.sum((y - mean_y) ** 2)

# Sum of Squared Residuals (SSR)
ssr = np.sum((y - predictions) ** 2)

# Manual R²
manual_r2 = 1 - (ssr / sst)

# -----------------------------------------------------
# sklearn R²
# -----------------------------------------------------

sklearn_r2 = r2_score(y, predictions)

# -----------------------------------------------------
# Display Calculations
# -----------------------------------------------------

print("\nMean of Target (y)")
print(mean_y)

print("\nTotal Sum of Squares (SST)")
print(sst)

print("\nSum of Squared Residuals (SSR)")
print(ssr)

print("\nManual R²")
print(manual_r2)

print("\nscikit-learn R²")
print(sklearn_r2)

# -----------------------------------------------------
# Comparison Table
# -----------------------------------------------------

comparison = pd.DataFrame({

    "Experience": df["Experience"],

    "Actual Salary": y,

    "Predicted Salary": predictions

})

print("\nComparison Table\n")

print(comparison)

# -----------------------------------------------------
# Interpretation
# -----------------------------------------------------

print("\nInterview Interpretation")
print("--------------------------------")

print(f"R² Score : {sklearn_r2:.4f}")

if sklearn_r2 >= 0.90:
    print("Excellent model. Most of the variance is explained.")

elif sklearn_r2 >= 0.75:
    print("Good model with strong predictive ability.")

elif sklearn_r2 >= 0.50:
    print("Average model. Improvement is possible.")

elif sklearn_r2 >= 0:
    print("Weak model.")

else:
    print("Poor model. Worse than predicting the average.")

# -----------------------------------------------------
# Formula Explanation
# -----------------------------------------------------

print("\nFormula Used")

print("R² = 1 - (SSR / SST)")

print("\nWhere")

print("SSR = Sum of Squared Residuals")

print("SST = Total Sum of Squares")