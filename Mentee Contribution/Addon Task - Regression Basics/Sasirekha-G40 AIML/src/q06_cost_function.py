"""
========================================================

Interview Question 6

What is the purpose of the cost function in regression?

Interview Answer

A cost function measures the prediction error of a
regression model.

Linear Regression tries to minimize this error.

The most commonly used cost function is Mean Squared
Error (MSE).

========================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import meansquared_error

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

# Calculate cost
cost = mean_squared_error(y, predictions)

print("\nCost Function (MSE):")
print(cost)

# Compare actual and predicted values
comparison = pd.DataFrame({
    "Experience": df["Experience"],
    "Actual Salary": y,
    "Predicted Salary": predictions
})

print("\nActual vs Predicted\n")
print(comparison)

# Plot graph
plt.scatter(
    df["Experience"],
    y,
    label="Actual Data"
)

plt.plot(
    df["Experience"],
    predictions,
    label="Regression Line"
)

plt.title("Linear Regression")

plt.xlabel("Experience")

plt.ylabel("Salary")

plt.legend()

plt.show()
