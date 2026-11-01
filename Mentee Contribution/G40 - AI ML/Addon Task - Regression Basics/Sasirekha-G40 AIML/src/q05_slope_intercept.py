"""
========================================================

Interview Question 5

What do the slope and intercept represent in a Linear
Regression model?

Interview Answer

Slope:
Shows how much the dependent variable changes when the
independent variable increases by one unit.

Intercept:
Predicted value of the dependent variable when the
independent variable is zero.

========================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Read dataset
df = pd.read_csv(C\salary_data.csv")

print("Dataset")
print(df)

# Independent Variable
X = df[["Experience"]]

# Dependent Variable
y = df["Salary"]

# Create Model
model = LinearRegression()

# Train Model
model.fit(X, y)

# Print slope
print("\nSlope (Coefficient)")
print(model.coef_)

# Print intercept
print("\nIntercept")
print(model.intercept_)

# Predict all values
predictions = model.predict(X)

# Predict salary for 11 years of experience
salary = model.predict([[11]])

print("\nPredicted Salary for 11 Years Experience")
print(salary[0])

# Plot graph
plt.scatter(df["Experience"], df["Salary"], label="Actual Data")
plt.plot(df["Experience"], predictions, label="Regression Line")
plt.title("Linear Regression")
plt.xlabel("Experience")
plt.ylabel("Salary")
plt.legend()
plt.show()
