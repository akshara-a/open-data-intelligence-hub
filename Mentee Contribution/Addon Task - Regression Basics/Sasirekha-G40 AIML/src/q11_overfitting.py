"""
============================================================

Interview Question 11

What is Overfitting in a Regression Model?

Interview Answer

Overfitting occurs when a machine learning model learns
the training data too well, including noise and outliers.

Characteristics:
1. Very high training accuracy.
2. Poor testing accuracy.
3. Poor generalization to new data.

Solution:
- More training data
- Cross Validation
- Regularization
- Simpler model
- Pruning (Decision Trees)

============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score

# -----------------------------------------------------
# Generate Dataset
# -----------------------------------------------------

X, y = make_regression(
    n_samples=200,
    n_features=1,
    noise=25,
    random_state=42
)

# Convert to DataFrame

df = pd.DataFrame({
    "Experience": X.flatten(),
    "Salary": y
})

print(df.head())

# -----------------------------------------------------
# Split Dataset
# -----------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

# -----------------------------------------------------
# Overfitting Model
# Very Deep Decision Tree
# -----------------------------------------------------

model = DecisionTreeRegressor(
    max_depth=None,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------------------------------
# Predictions
# -----------------------------------------------------

train_prediction = model.predict(X_train)

test_prediction = model.predict(X_test)

# -----------------------------------------------------
# Accuracy
# -----------------------------------------------------

train_r2 = r2_score(y_train, train_prediction)

test_r2 = r2_score(y_test, test_prediction)

print("\nTraining R2 Score")
print(train_r2)

print("\nTesting R2 Score")
print(test_r2)

# -----------------------------------------------------
# Graph
# -----------------------------------------------------

plt.figure(figsize=(8,6))

plt.scatter(
    X_train,
    y_train,
    label="Training Data"
)

plt.scatter(
    X_test,
    y_test,
    label="Testing Data"
)

plt.title("Overfitting Example")

plt.xlabel("Experience")

plt.ylabel("Salary")

plt.legend()

plt.show()

# -----------------------------------------------------
# Interview Summary
# -----------------------------------------------------

print("\n----------------------------")
print("Interview Summary")
print("----------------------------")

print(f"Training R2 : {train_r2:.3f}")

print(f"Testing R2  : {test_r2:.3f}")

if train_r2 > 0.95 and test_r2 < 0.80:
    print("\nModel is Overfitting.")
    print("Excellent on training data.")
    print("Poor on unseen testing data.")
else:
    print("\nModel is not strongly overfitting.")