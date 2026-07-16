import os

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.linear_model import (
    LinearRegression,
    Ridge
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RESULTS_DIRECTORY = "outputs/results"
PLOTS_DIRECTORY = "outputs/plots"


def calculate_regression_metrics(
    model_name,
    y_true,
    y_pred
):
    """
    Calculate regression evaluation metrics.
    """

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    mse = mean_squared_error(
        y_true,
        y_pred
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_true,
        y_pred
    )

    return {
        "Model": model_name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2_Score": r2
    }


def train_regression_models(df):
    """
    Train and compare Linear Regression
    and Ridge Regression models for
    customer rating prediction.
    """

    print("\n" + "=" * 60)
    print("REGRESSION - RATING PREDICTION")
    print("=" * 60)


    # Features used for rating prediction
    regression_features = [
        "unit_price",
        "quantity",
        "discount_percent",
        "pages_viewed",
        "time_on_site_sec",
        "added_to_cart",
        "product_category",
        "device_type",
        "user_type",
        "engagement_score"
    ]


    target = "rating"


    X = df[regression_features]

    y = df[target]


    print("\nRegression Features:")

    for feature in regression_features:
        print(f"- {feature}")


    print(
        f"\nTarget Variable: {target}"
    )


    # Split the dataset
    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )
    )


    print(
        f"\nTraining Records: {X_train.shape[0]}"
    )

    print(
        f"Testing Records : {X_test.shape[0]}"
    )


    # -------------------------------------------------
    # Linear Regression
    # -------------------------------------------------

    linear_model = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                LinearRegression()
            )
        ]
    )


    linear_model.fit(
        X_train,
        y_train
    )


    linear_predictions = (
        linear_model.predict(X_test)
    )


    linear_metrics = (
        calculate_regression_metrics(
            "Linear Regression",
            y_test,
            linear_predictions
        )
    )


    # -------------------------------------------------
    # Ridge Regression
    # -------------------------------------------------

    ridge_model = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                Ridge(
                    alpha=1.0
                )
            )
        ]
    )


    ridge_model.fit(
        X_train,
        y_train
    )


    ridge_predictions = (
        ridge_model.predict(X_test)
    )


    ridge_metrics = (
        calculate_regression_metrics(
            "Ridge Regression",
            y_test,
            ridge_predictions
        )
    )


    # -------------------------------------------------
    # Model Comparison
    # -------------------------------------------------

    regression_results = pd.DataFrame(
        [
            linear_metrics,
            ridge_metrics
        ]
    )


    print("\nREGRESSION MODEL COMPARISON")
    print("-" * 60)

    print(
        regression_results.to_string(
            index=False
        )
    )


    # Create results directory
    os.makedirs(
        RESULTS_DIRECTORY,
        exist_ok=True
    )


    results_file = os.path.join(
        RESULTS_DIRECTORY,
        "regression_model_comparison.csv"
    )


    regression_results.to_csv(
        results_file,
        index=False
    )


    print(
        f"\nRegression results saved to: "
        f"{results_file}"
    )


    # -------------------------------------------------
    # Select Better Model
    # -------------------------------------------------

    best_model_index = (
        regression_results["RMSE"]
        .idxmin()
    )


    best_model_name = (
        regression_results.loc[
            best_model_index,
            "Model"
        ]
    )


    print(
        f"\nBest Regression Model: "
        f"{best_model_name}"
    )


    # -------------------------------------------------
    # Actual vs Predicted Rating Plot
    # -------------------------------------------------

    if best_model_name == "Linear Regression":

        best_predictions = (
            linear_predictions
        )

        best_model = linear_model

    else:

        best_predictions = (
            ridge_predictions
        )

        best_model = ridge_model


    os.makedirs(
        PLOTS_DIRECTORY,
        exist_ok=True
    )


    plt.figure(
        figsize=(8, 6)
    )


    plt.scatter(
        y_test,
        best_predictions,
        alpha=0.4
    )


    minimum_rating = min(
        y_test.min(),
        best_predictions.min()
    )

    maximum_rating = max(
        y_test.max(),
        best_predictions.max()
    )


    plt.plot(
        [
            minimum_rating,
            maximum_rating
        ],
        [
            minimum_rating,
            maximum_rating
        ],
        linestyle="--"
    )


    plt.title(
        "Actual vs Predicted Customer Ratings"
    )

    plt.xlabel(
        "Actual Rating"
    )

    plt.ylabel(
        "Predicted Rating"
    )


    regression_plot = os.path.join(
        PLOTS_DIRECTORY,
        "09_actual_vs_predicted_rating.png"
    )


    plt.tight_layout()

    plt.savefig(
        regression_plot,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"Saved plot: {regression_plot}"
    )


    # -------------------------------------------------
    # Example Prediction
    # -------------------------------------------------

    example_customer = X_test.iloc[[0]]

    actual_rating = y_test.iloc[0]

    predicted_rating = best_model.predict(
        example_customer
    )[0]


    print("\nEXAMPLE RATING PREDICTION")
    print("-" * 60)

    print(
        f"Actual Rating    : "
        f"{actual_rating:.2f}"
    )

    print(
        f"Predicted Rating : "
        f"{predicted_rating:.2f} out of 5"
    )


    print(
        "\nRegression model training completed."
    )


    return (
        best_model,
        regression_results
    )