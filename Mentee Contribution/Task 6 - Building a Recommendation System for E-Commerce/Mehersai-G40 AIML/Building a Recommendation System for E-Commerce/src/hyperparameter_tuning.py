import os

import pandas as pd

from sklearn.linear_model import (
    Ridge,
    LogisticRegression
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV
)

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler


RESULTS_DIRECTORY = "outputs/results"


def tune_ridge_regression(df):
    """
    Tune Ridge Regression alpha using GridSearchCV.
    """

    print("\n" + "=" * 60)
    print("RIDGE REGRESSION HYPERPARAMETER TUNING")
    print("=" * 60)


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


    X = df[regression_features]

    y = df["rating"]


    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )
    )


    ridge_pipeline = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                Ridge()
            )
        ]
    )


    ridge_parameters = {
        "model__alpha": [
            0.01,
            0.1,
            1.0,
            10.0,
            100.0
        ]
    }


    ridge_grid_search = GridSearchCV(
        estimator=ridge_pipeline,
        param_grid=ridge_parameters,
        scoring="neg_root_mean_squared_error",
        cv=5,
        n_jobs=-1
    )


    ridge_grid_search.fit(
        X_train,
        y_train
    )


    best_ridge_model = (
        ridge_grid_search.best_estimator_
    )


    predictions = best_ridge_model.predict(
        X_test
    )


    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )


    print("\nBEST RIDGE PARAMETERS")
    print("-" * 60)

    print(
        ridge_grid_search.best_params_
    )


    print("\nTUNED RIDGE PERFORMANCE")
    print("-" * 60)

    print(f"MAE      : {mae:.6f}")
    print(f"MSE      : {mse:.6f}")
    print(f"RMSE     : {rmse:.6f}")
    print(f"R2 Score : {r2:.6f}")


    ridge_results = pd.DataFrame(
        [
            {
                "Model": "Tuned Ridge Regression",
                "Best_Alpha": (
                    ridge_grid_search.best_params_[
                        "model__alpha"
                    ]
                ),
                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse,
                "R2_Score": r2
            }
        ]
    )


    os.makedirs(
        RESULTS_DIRECTORY,
        exist_ok=True
    )


    ridge_file = os.path.join(
        RESULTS_DIRECTORY,
        "tuned_ridge_results.csv"
    )


    ridge_results.to_csv(
        ridge_file,
        index=False
    )


    print(
        f"\nTuned Ridge results saved to: "
        f"{ridge_file}"
    )


    return (
        best_ridge_model,
        ridge_results
    )


def tune_logistic_regression(df):
    """
    Tune Logistic Regression using GridSearchCV.
    """

    print("\n" + "=" * 60)
    print("LOGISTIC REGRESSION HYPERPARAMETER TUNING")
    print("=" * 60)


    classification_features = [
        "device_type",
        "user_type",
        "marketing_channel",
        "product_category",
        "unit_price",
        "quantity",
        "discount_percent",
        "pages_viewed",
        "time_on_site_sec",
        "added_to_cart",
        "visit_day",
        "visit_month",
        "visit_weekday",
        "visit_season",
        "discount_applied",
        "engagement_score"
    ]


    X = df[classification_features]

    y = df["purchased"]


    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )


    logistic_pipeline = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                LogisticRegression(
                    class_weight="balanced",
                    random_state=42,
                    solver="liblinear"
                )
            )
        ]
    )


    logistic_parameters = {
    "model__C": [
        0.01,
        0.1,
        1.0,
        10.0
    ],
    "model__l1_ratio": [
        0.0,
        1.0
    ],
    "model__max_iter": [
        500,
        1000
    ]
}


    logistic_grid_search = GridSearchCV(
        estimator=logistic_pipeline,
        param_grid=logistic_parameters,
        scoring="roc_auc",
        cv=5,
        n_jobs=-1
    )


    logistic_grid_search.fit(
        X_train,
        y_train
    )


    best_logistic_model = (
        logistic_grid_search.best_estimator_
    )


    predictions = (
        best_logistic_model.predict(
            X_test
        )
    )


    probabilities = (
        best_logistic_model.predict_proba(
            X_test
        )[:, 1]
    )


    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions
    )

    recall = recall_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )


    print("\nBEST LOGISTIC REGRESSION PARAMETERS")
    print("-" * 60)

    print(
        logistic_grid_search.best_params_
    )


    print("\nTUNED LOGISTIC REGRESSION PERFORMANCE")
    print("-" * 60)

    print(f"Accuracy  : {accuracy:.6f}")
    print(f"Precision : {precision:.6f}")
    print(f"Recall    : {recall:.6f}")
    print(f"F1 Score  : {f1:.6f}")
    print(f"ROC-AUC   : {roc_auc:.6f}")


    logistic_results = pd.DataFrame(
        [
            {
                "Model": (
                    "Tuned Logistic Regression"
                ),
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1_Score": f1,
                "ROC_AUC": roc_auc
            }
        ]
    )


    logistic_file = os.path.join(
        RESULTS_DIRECTORY,
        "tuned_logistic_results.csv"
    )


    logistic_results.to_csv(
        logistic_file,
        index=False
    )


    print(
        f"\nTuned Logistic results saved to: "
        f"{logistic_file}"
    )


    return (
        best_logistic_model,
        logistic_results
    )


def perform_hyperparameter_tuning(df):
    """
    Perform hyperparameter optimization
    for regression and classification models.
    """

    print("\n" + "=" * 60)
    print("HYPERPARAMETER OPTIMIZATION")
    print("=" * 60)


    tuned_ridge_model, ridge_results = (
        tune_ridge_regression(df)
    )


    (
        tuned_logistic_model,
        logistic_results
    ) = tune_logistic_regression(df)


    print("\n" + "=" * 60)
    print(
        "HYPERPARAMETER OPTIMIZATION COMPLETED"
    )
    print("=" * 60)


    return (
        tuned_ridge_model,
        tuned_logistic_model,
        ridge_results,
        logistic_results
    )