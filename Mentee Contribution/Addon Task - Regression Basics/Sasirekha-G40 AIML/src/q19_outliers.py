"""
============================================================

Interview Question 19

How do outliers affect a regression model?

Interview Answer

Outliers are observations that are significantly different
from the rest of the data.

Example

Most salaries:
30000, 35000, 40000, 45000

Outlier:
500000

Effects of Outliers

1. Change the regression line.
2. Increase prediction error.
3. Increase Mean Squared Error (MSE).
4. Reduce model accuracy.
5. Produce unreliable predictions.

Ways to Handle Outliers

1. Detect using Box Plot
2. Detect using Z-Score
3. Detect using IQR Method
4. Remove incorrect values
5. Transform data if appropriate

============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

# -----------------------------------------------------
# Dataset WITHOUT Outliers
# -----------------------------------------------------

experience = [

    1,2,3,4,5,
    6,7,8,9,10

]

salary = [

    25000,
    30000,
    36000,
    43000,
    52000,
    61000,
    72000,
    85000,
    98000,
    112000

]

# -----------------------------------------------------
# Dataset WITH Outlier
# -----------------------------------------------------

salary_outlier = [

    25000,
    30000,
    36000,
    43000,
    52000,
    61000,
    72000,
    85000,
    98000,
    350000

]

# -----------------------------------------------------
# DataFrames
# -----------------------------------------------------

df_normal = pd.DataFrame({

    "Experience": experience,

    "Salary": salary

})

df_outlier = pd.DataFrame({

    "Experience": experience,

    "Salary": salary_outlier

})

print("Dataset Without Outlier\n")

print(df_normal)

print("\nDataset With Outlier\n")

print(df_outlier)

# -----------------------------------------------------
# Features
# -----------------------------------------------------

X1 = df_normal[["Experience"]]

y1 = df_normal["Salary"]

X2 = df_outlier[["Experience"]]

y2 = df_outlier["Salary"]

# -----------------------------------------------------
# Train Models
# -----------------------------------------------------

model1 = LinearRegression()

model1.fit(X1, y1)

prediction1 = model1.predict(X1)

model2 = LinearRegression()

model2.fit(X2, y2)

prediction2 = model2.predict(X2)

# -----------------------------------------------------
# Metrics
# -----------------------------------------------------

normal_r2 = r2_score(y1, prediction1)

outlier_r2 = r2_score(y2, prediction2)

normal_mse = mean_squared_error(
    y1,
    prediction1
)

outlier_mse = mean_squared_error(
    y2,
    prediction2
)

# -----------------------------------------------------
# Comparison Table
# -----------------------------------------------------

comparison = pd.DataFrame({

    "Model":[

        "Without Outlier",

        "With Outlier"

    ],

    "R2 Score":[

        normal_r2,

        outlier_r2

    ],

    "MSE":[

        normal_mse,

        outlier_mse

    ]

})

print("\nPerformance Comparison\n")

print(comparison)

# -----------------------------------------------------
# Plot Without Outlier
# -----------------------------------------------------

plt.figure(figsize=(8,6))

plt.scatter(
    X1,
    y1,
    label="Data"
)

plt.plot(
    X1,
    prediction1,
    linewidth=2,
    label="Regression Line"
)

plt.title("Regression Without Outlier")

plt.xlabel("Experience")

plt.ylabel("Salary")

plt.legend()

plt.show()

# -----------------------------------------------------
# Plot With Outlier
# -----------------------------------------------------

plt.figure(figsize=(8,6))

plt.scatter(
    X2,
    y2,
    label="Data"
)

plt.plot(
    X2,
    prediction2,
    linewidth=2,
    label="Regression Line"
)

plt.title("Regression With Outlier")

plt.xlabel("Experience")

plt.ylabel("Salary")

plt.legend()

plt.show()

# -----------------------------------------------------
# Interview Summary
# -----------------------------------------------------

print("\n----------------------------------")

print("Interview Summary")

print("----------------------------------")

print("""

Without Outliers

• Better Regression Line

• Lower Prediction Error

• Lower MSE

• Better Generalization

----------------------------------

With Outliers

• Regression Line Changes

• Higher Prediction Error

• Higher MSE

• Less Reliable Predictions

""")

# -----------------------------------------------------
# Final Conclusion
# -----------------------------------------------------

print("Conclusion")

print("----------------------------------")

print(f"Without Outlier R² : {normal_r2:.4f}")

print(f"With Outlier R²    : {outlier_r2:.4f}")

print()

print(f"Without Outlier MSE : {normal_mse:.2f}")

print(f"With Outlier MSE    : {outlier_mse:.2f}")

print()

print("Outliers can significantly affect")

print("Linear Regression because the model")

print("tries to minimize squared errors.")

print("Large errors from outliers have")

print("a strong influence on the fitted line.")