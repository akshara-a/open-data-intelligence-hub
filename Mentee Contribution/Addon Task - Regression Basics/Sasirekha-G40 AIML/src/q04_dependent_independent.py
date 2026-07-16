"""
========================================================

Interview Question 4

What is the difference between a dependent variable and
an independent variable?

Interview Answer

Independent Variable:
Input features used for prediction.

Dependent Variable:
Output or target variable that is predicted.

========================================================
"""

import pandas as pd

# Read dataset
df = pd.read_csv(r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\house_price.csv")

print("Complete Dataset\n")
print(df)

print("\nColumn Names")
print(df.columns)

# Independent Variables
X = df[["Area", "Bedrooms", "Age"]]

# Dependent Variable
y = df["Price"]

print("\nIndependent Variables (X)\n")
print(X)

print("\nDependent Variable (y)\n")
print(y)

print("\nShape of X:", X.shape)
print("Shape of y:", y.shape)