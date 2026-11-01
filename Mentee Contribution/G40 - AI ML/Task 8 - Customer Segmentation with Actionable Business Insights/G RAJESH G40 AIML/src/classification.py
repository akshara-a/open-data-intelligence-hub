from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt


def run_classification(df):

    # Create target column
    median_spend = df["Total Spend"].median()
    df["PurchaseLikelihood"] = (df["Total Spend"] > median_spend).astype(int)

    # Features
    X = df[
        [
            "Age",
            "Items Purchased",
            "Average Rating",
            "Days Since Last Purchase",
            "Cluster",
        ]
    ]

    y = df["PurchaseLikelihood"]

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    # Logistic Regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\n========== Logistic Regression ==========")
    print("Accuracy :", round(accuracy_score(y_test, predictions), 3))
    print("Precision:", round(precision_score(y_test, predictions), 3))
    print("Recall   :", round(recall_score(y_test, predictions), 3))
    print("F1 Score :", round(f1_score(y_test, predictions), 3))

    # Confusion Matrix
    cm = confusion_matrix(y_test, predictions)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()

    plt.savefig("outputs/charts/confusion_matrix.png")
    plt.close()

    print("\nConfusion matrix saved successfully!")