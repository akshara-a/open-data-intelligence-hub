"""
============================================================

Interview Question 18

What is Polynomial Regression?

Interview Answer

Polynomial Regression is an extension of Linear Regression
used when the relationship between the independent and
dependent variables is nonlinear.

Instead of fitting a straight line, Polynomial Regression
fits a curved line by adding polynomial terms such as:

x², x³, x⁴ ...

General Equation

y = β₀ + β₁x + β₂x² + β₃x³ + ...

Advantages

1. Captures nonlinear relationships
2. Better prediction for curved data
3. More flexible than Linear Regression

Disadvantages

1. High degree can cause overfitting
2. More computationally expensive
3. Harder to interpret

============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------------------------------
# Create Sample Dataset
# -------------------------------------------------------

experience = np.array([
    1,2,3,4,5,6,7,8,9,10
])

salary = np.array([
    25000,
    29000,
    36000,
    47000,
    61000,
    78000,
    98000,
    121000,
    147000,
    176000
])

df = pd.DataFrame({

    "Experience": experience,

    "Salary": salary

})

print("Dataset\n")

print(df)

# -------------------------------------------------------
# Features
# -------------------------------------------------------

X = df[["Experience"]]

y = df["Salary"]

# -------------------------------------------------------
# Linear Regression
# -------------------------------------------------------

linear = LinearRegression()

linear.fit(X, y)

linear_prediction = linear.predict(X)

# -------------------------------------------------------
# Polynomial Features
# -------------------------------------------------------

poly = PolynomialFeatures(degree=2)

X_poly = poly.fit_transform(X)

# -------------------------------------------------------
# Polynomial Regression
# -------------------------------------------------------

poly_model = LinearRegression()

poly_model.fit(X_poly, y)

poly_prediction = poly_model.predict(X_poly)

# -------------------------------------------------------
# Evaluation
# -------------------------------------------------------

linear_r2 = r2_score(y, linear_prediction)

poly_r2 = r2_score(y, poly_prediction)

linear_mse = mean_squared_error(
    y,
    linear_prediction
)

poly_mse = mean_squared_error(
    y,
    poly_prediction
)

# -------------------------------------------------------
# Performance Table
# -------------------------------------------------------

performance = pd.DataFrame({

    "Model":[

        "Linear Regression",

        "Polynomial Regression"

    ],

    "R²":[

        linear_r2,

        poly_r2

    ],

    "MSE":[

        linear_mse,

        poly_mse

    ]

})

print("\nPerformance Comparison\n")

print(performance)

# -------------------------------------------------------
# Prediction Table
# -------------------------------------------------------

prediction_table = pd.DataFrame({

    "Experience": experience,

    "Actual Salary": salary,

    "Linear Prediction": linear_prediction,

    "Polynomial Prediction": poly_prediction

})

print("\nPrediction Comparison\n")

print(prediction_table)

# -------------------------------------------------------
# Plot
# -------------------------------------------------------

plt.figure(figsize=(8,6))

plt.scatter(

    X,

    y,

    color="blue",

    label="Actual Data"

)

plt.plot(

    X,

    linear_prediction,

    color="red",

    linewidth=2,

    label="Linear Regression"

)

plt.plot(

    X,

    poly_prediction,

    color="green",

    linewidth=2,

    label="Polynomial Regression"

)

plt.title("Linear vs Polynomial Regression")

plt.xlabel("Experience")

plt.ylabel("Salary")

plt.legend()

plt.show()

# -------------------------------------------------------
# Interview Summary
# -------------------------------------------------------

print("\n-----------------------------------")

print("Interview Summary")

print("-----------------------------------")

print("""

Linear Regression

• Straight Line

• Best for linear data

Polynomial Regression

• Curved Line

• Best for nonlinear data

Higher Degree

↓

Higher Flexibility

↓

Risk of Overfitting

""")