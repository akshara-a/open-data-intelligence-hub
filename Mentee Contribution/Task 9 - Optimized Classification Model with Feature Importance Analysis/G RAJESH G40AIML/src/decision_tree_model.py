from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from src.evaluation import evaluate_model


def run_decision_tree(X_train, X_test, y_train, y_test):

    print("\n========== Decision Tree ==========")

    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=6
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    evaluate_model(y_test, predictions)

    print("\nClassification Report")
    print(classification_report(y_test, predictions))

    return model