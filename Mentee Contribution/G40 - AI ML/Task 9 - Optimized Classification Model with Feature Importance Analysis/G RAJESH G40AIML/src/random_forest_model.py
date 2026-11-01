from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from src.evaluation import evaluate_model
from src.feature_importance import plot_feature_importance


def run_random_forest(X_train, X_test, y_train, y_test):

    print("\n========== Random Forest ==========")

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    evaluate_model(y_test, predictions)

    print("\nClassification Report")
    print(classification_report(y_test, predictions))

    # Generate Feature Importance graph
    plot_feature_importance(model, X_train.columns)

    return model