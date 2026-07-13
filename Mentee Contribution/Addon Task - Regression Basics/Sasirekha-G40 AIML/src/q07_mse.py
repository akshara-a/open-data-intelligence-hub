"""
========================================================

Interview Question 7

What is Mean Squared Error (MSE), and why is it commonly
used for regression?

Interview Answer

Mean Squared Error (MSE) measures the average squared
difference between actual and predicted values.

A smaller MSE indicates better model performance.

========================================================
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Read dataset
df = pd.read_csv("r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\salary_data.csv")

print("Dataset\n")
print(df)

# Features
X = df[["Experience"]]

# Target
y = df["Salary"]

# Create model
model = LinearRegression()

# Train model
model.fit(X, y)

# Predictions
predictions = model.predict(X)

# MSE using sklearn
mse = mean_squared_error(y, predictions)

print("\nMSE using sklearn")
print(mse)

# Manual calculation
errors = y - predictions
squared_errors = errors ** 2
manual_mse = squared_errors.mean()

print("\nManual MSE")
print(manual_mse)

# Comparison Table
comparison = pd.DataFrame({
    "Actual": y,
    "Predicted": predictions,
    "Error": errors,
    "Squared Error": squared_errors
})

print("\nComparison Table\n")
print(comparison)
