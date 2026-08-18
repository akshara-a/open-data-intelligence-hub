import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from src.evaluation import evaluate_model


def run_logistic_model(X_train, X_test, y_train, y_test):

    print("\n========== Logistic Regression ==========")

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    evaluate_model(y_test, predictions)

    print("\nClassification Report")
    print(classification_report(y_test, predictions))

    cm = confusion_matrix(y_test, predictions)

    plt.figure(figsize=(5, 5))
    plt.imshow(cm, cmap="Blues")

    plt.title("Logistic Regression Confusion Matrix")
    plt.colorbar()

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    for i in range(len(cm)):
        for j in range(len(cm)):
            plt.text(j, i, cm[i, j], ha="center", va="center")

    plt.tight_layout()

    # Create output folder if it doesn't exist
    os.makedirs("outputs/charts", exist_ok=True)

    plt.savefig("outputs/charts/logistic_confusion_matrix.png")
    plt.close()

    print("\nConfusion matrix saved successfully!")

    return model