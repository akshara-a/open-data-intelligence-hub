"""Classification models for purchase likelihood."""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import GridSearchCV


def classification_metrics(y_true, y_pred, probabilities):
    """Return classification metrics."""
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1": f1_score(y_true, y_pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_true, probabilities),
        "ConfusionMatrix": confusion_matrix(y_true, y_pred),
    }


def train_logistic_regression(X_train, X_test, y_train, y_test):
    """Train baseline Logistic Regression."""
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return model, classification_metrics(
        y_test, predictions, probabilities
    )


def tune_logistic_regression(X_train, y_train):
    """Tune Logistic Regression with GridSearchCV."""
    search = GridSearchCV(
        LogisticRegression(max_iter=2000, random_state=42),
        {
            "C": [0.01, 0.1, 1, 10, 100],
            "solver": ["liblinear", "lbfgs"],
        },
        cv=5,
        scoring="f1",
    )
    search.fit(X_train, y_train)
    return search
