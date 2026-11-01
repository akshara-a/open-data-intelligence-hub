from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def run_regression(df):

    # Features
    X = df[[
        "Age",
        "Items Purchased",
        "Average Rating",
        "Days Since Last Purchase"
    ]]

    # Target
    y = df["Total Spend"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -----------------------------
    # Linear Regression
    # -----------------------------
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    y_pred = linear_model.predict(X_test)

    print("\n========== Linear Regression ==========")
    print("MAE :", round(mean_absolute_error(y_test, y_pred),2))
    print("RMSE:", round(mean_squared_error(y_test, y_pred)**0.5,2))
    print("R2  :", round(r2_score(y_test, y_pred),3))

    # -----------------------------
    # Ridge Regression
    # -----------------------------
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train, y_train)

    ridge_pred = ridge_model.predict(X_test)

    print("\n========== Ridge Regression ==========")
    print("MAE :", round(mean_absolute_error(y_test, ridge_pred),2))
    print("RMSE:", round(mean_squared_error(y_test, ridge_pred)**0.5,2))
    print("R2  :", round(r2_score(y_test, ridge_pred),3))

    # -----------------------------
    # Save Plot
    # -----------------------------
    plt.figure(figsize=(6,6))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual Total Spend")
    plt.ylabel("Predicted Total Spend")
    plt.title("Actual vs Predicted")
    plt.grid(True)

    plt.savefig("outputs/charts/regression_prediction.png")
    plt.close()

    print("\nRegression graph saved successfully!")