"""
=====================================================

Interview Question 3

What assumptions are made by Linear Regression?

Interview Answer

1. Linearity
2. Independence
3. Homoscedasticity
4. Normal Distribution of Residuals
5. No Multicollinearity

=====================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Read dataset
df = pd.read_csv(r"C:\Users\ELCOT\Desktop\Regression_Interview_practice\data\salary_data.csv")

# Independent Variable
X = df[["Experience"]]

# Dependent Variable
y = df["Salary"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Predictions
predictions = model.predict(X)

# Residuals
residuals = y - predictions

# -------------------------
# Linearity
# -------------------------
plt.scatter(df["Experience"], y)
plt.plot(df["Experience"], predictions)
plt.title("Linearity Check")
plt.xlabel("Experience")
plt.ylabel("Salary")
plt.show()

# -------------------------
# Homoscedasticity
# -------------------------
plt.scatter(predictions, residuals)
plt.axhline(y=0)
plt.title("Residual Plot")
plt.xlabel("Predicted Salary")
plt.ylabel("Residual")
plt.show()

# -------------------------
# Normality of Residuals
# -------------------------
plt.hist(residuals)
plt.title("Residual Histogram")
plt.xlabel("Residual")
plt.ylabel("Frequency")
plt.show()
