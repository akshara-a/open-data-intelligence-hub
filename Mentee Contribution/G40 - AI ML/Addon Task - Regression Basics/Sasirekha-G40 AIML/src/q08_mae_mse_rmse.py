"""
========================================================

Interview Question 8

What is the difference between Mean Absolute Error (MAE),
Mean Squared Error (MSE), and Root Mean Squared Error (RMSE)?

Interview Answer

MAE (Mean Absolute Error):
--------------------------
Measures the average absolute difference between actual
and predicted values.

Formula:
MAE = Σ|Actual - Predicted| / n

Advantages:
- Easy to understand.
- Less affected by outliers.

--------------------------------------------------------

MSE (Mean Squared Error):
-------------------------
Measures the average squared difference between actual
and predicted values.

Formula:
MSE = Σ(Actual - Predicted)^2 / n

Advantages:
- Penalizes large errors.
- Common cost function in Linear Regression.

--------------------------------------------------------

RMSE (Root Mean Squared Error):
-------------------------------
Square root of MSE.

Formula:
RMSE = √MSE

Advantages:
- Same unit as the target variable.
- Easier to interpret than MSE.

========================================================
"""

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

# -----------------------------------------------------
# Read Dataset
# -----------------------------------------------------

df = pd.read_csv("r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\salary_data.csv")

print("Dataset\n")
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
# Error Calculation
# -----------------------------------------------------

errors = y - predictions

absolute_errors = abs(errors)

squared_errors = errors ** 2

# -----------------------------------------------------
# Manual Metrics
# -----------------------------------------------------

manual_mae = absolute_errors.mean()

manual_mse = squared_errors.mean()

manual_rmse = np.sqrt(manual_mse)

# -----------------------------------------------------
# sklearn Metrics
# -----------------------------------------------------

sklearn_mae = mean_absolute_error(y, predictions)

sklearn_mse = mean_squared_error(y, predictions)

sklearn_rmse = np.sqrt(sklearn_mse)

# -----------------------------------------------------
# Comparison Table
# -----------------------------------------------------

comparison = pd.DataFrame({

    "Actual": y,

    "Predicted": predictions,

    "Error": errors,

    "Absolute Error": absolute_errors,

    "Squared Error": squared_errors

})

print("\nComparison Table\n")

print(comparison)

# -----------------------------------------------------
# Metrics Table
# -----------------------------------------------------

metrics = pd.DataFrame({

    "Metric": [
        "MAE",
        "MSE",
        "RMSE"
    ],

    "Manual Value": [
        manual_mae,
        manual_mse,
        manual_rmse
    ],

    "scikit-learn Value": [
        sklearn_mae,
        sklearn_mse,
        sklearn_rmse
    ]

})

print("\nEvaluation Metrics\n")

print(metrics)

# -----------------------------------------------------
# Best Metric
# -----------------------------------------------------

print("\nInterview Summary")
print("-----------------------------")
print(f"MAE  : {sklearn_mae:.2f}")
print(f"MSE  : {sklearn_mse:.2f}")
print(f"RMSE : {sklearn_rmse:.2f}")

print("\nInterpretation")

print("• Lower MAE means smaller average prediction error.")

print("• Lower MSE means fewer large prediction errors.")

print("• Lower RMSE means better prediction accuracy and it is in the same unit as Salary.")
