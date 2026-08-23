"""Regression models for predicting customer value."""

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV


def regression_metrics(y_true, y_pred):
    """Return standard regression metrics."""
    mse = mean_squared_error(y_true, y_pred)
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "MSE": mse,
        "RMSE": mse ** 0.5,
        "R2": r2_score(y_true, y_pred),
    }


def train_baseline_models(X_train, X_test, y_train, y_test):
    """Train Linear Regression and Ridge Regression baselines."""
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        results[name] = {
            "model": model,
            "predictions": pred,
            "metrics": regression_metrics(y_test, pred),
        }

    return results


def tune_ridge(X_train, y_train):
    """Tune Ridge alpha using GridSearchCV."""
    search = GridSearchCV(
        Ridge(),
        {"alpha": [0.01, 0.1, 1, 10, 100]},
        cv=5,
        scoring="neg_root_mean_squared_error",
    )
    search.fit(X_train, y_train)
    return search
