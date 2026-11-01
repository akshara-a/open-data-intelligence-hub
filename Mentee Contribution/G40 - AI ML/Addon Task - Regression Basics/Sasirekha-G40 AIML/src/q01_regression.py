"""
=========================================================
Interview Question 1

What is Regression in Machine Learning, and when is it used?

Interview Answer:

Regression is a supervised machine learning algorithm
used to predict continuous numerical values.

It learns the relationship between independent variables
(features) and the dependent variable (target).

Examples:
- House Price Prediction
- Salary Prediction
- Sales Forecasting
- Temperature Prediction

=========================================================
"""


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv(r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\salary_data.csv")
print(df)

X = df[["Experience"]]
y = df["Salary"]

model = LinearRegression()

model.fit(X, y)

prediction = model.predict([[11]])
print("Predicted Salary =", prediction[0])

plt.scatter(df["Experience"], df["Salary"], color="blue")
plt.plot(df["Experience"], model.predict(X), color="red")
plt.title("Salary Prediction")
plt.xlabel("Experience")
plt.ylabel("Salary")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Read dataset
df = pd.read_csv("../data/salary_data.csv")

# Independent variable
X = df[["Experience"]]

# Dependent variable
y = df["Salary"]

# Create model
model = LinearRegression()

# Train model
model.fit(X, y)

# Predict salary for 11 years experience
prediction = model.predict([[11]])
print("Predicted Salary:", prediction[0])

# Plot
plt.scatter(df["Experience"], df["Salary"])
plt.plot(df["Experience"], model.predict(X))
plt.title("Salary Prediction")
plt.xlabel("Experience")
plt.ylabel("Salary")
plt.show()

#You will see:🔵 Blue dots \(\rightarrow \) Actual salaries🔴 Red line \(\rightarrow \) Best-fit regression line
