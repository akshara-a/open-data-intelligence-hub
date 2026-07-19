"""Classification experiments: Logistic Regression with GridSearchCV."""
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def run_classification(X, y, preprocessor):
    X_trans = preprocessor.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_trans, y, test_size=0.2, random_state=42)

    lr = LogisticRegression(max_iter=1000)
    param_grid = {"C": [0.01, 0.1, 1.0, 10.0], "penalty": ["l2"]}
    grid = GridSearchCV(lr, param_grid, cv=5, scoring='f1')
    grid.fit(X_train, y_train)
    best = grid.best_estimator_
    preds = best.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "best_params": grid.best_params_,
    }
    return metrics, best
