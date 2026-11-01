"""
=========================================================
Interview Question 2

What is the difference between Simple Linear Regression
and Multiple Linear Regression?

Interview Answer:

Simple Linear Regression:
Uses only one independent variable.

Multiple Linear Regression:
Uses two or more independent variables.

Examples:
Simple:
Experience ---> Salary

Multiple:
Area + Bedrooms + Age ---> House Price

=========================================================
"""


import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv(r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\house_price.csv")
print(df)

X_simple = df[["Area"]]
y = df["Price"]

simple_model = LinearRegression()
simple_model.fit(X_simple, y)

simple_prediction = simple_model.predict([[3500]])
print("Simple Regression Prediction:")
print(simple_prediction[0])

X_multiple = df[["Area", "Bedrooms", "Age"]]

multiple_model = LinearRegression()
multiple_model.fit(X_multiple, y)

multiple_prediction = multiple_model.predict([[3500, 5, 2]])
print("Multiple Regression Prediction:")
print(multiple_prediction[0])
