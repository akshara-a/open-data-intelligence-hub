import os

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler


RESULTS_DIRECTORY = "outputs/results"
PLOTS_DIRECTORY = "outputs/plots"


def train_classification_model(df):
    """
    Train a Logistic Regression model
    to predict customer purchase likelihood.
    """

    print("\n" + "=" * 60)
    print("CLASSIFICATION - PURCHASE LIKELIHOOD")
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


    target = "purchased"


    X = df[classification_features]

    y = df[target]


    print("\nClassification Features:")

    for feature in classification_features:
        print(f"- {feature}")


    print(
        f"\nTarget Variable: {target}"
    )


    # Display target distribution
    print("\nPurchase Target Distribution:")

    print(
        y.value_counts()
    )


    # Split data using stratification
    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )


    print(
        f"\nTraining Records: "
        f"{X_train.shape[0]}"
    )

    print(
        f"Testing Records : "
        f"{X_test.shape[0]}"
    )


    # Logistic Regression Pipeline
    logistic_model = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42
                )
            )
        ]
    )


    # Train model
    logistic_model.fit(
        X_train,
        y_train
    )


    # Predict classes
    predictions = logistic_model.predict(
        X_test
    )


    # Predict purchase probabilities
    purchase_probabilities = (
        logistic_model.predict_proba(
            X_test
        )[:, 1]
    )


    # Evaluation Metrics
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
        purchase_probabilities
    )


    classification_results = pd.DataFrame(
        [
            {
                "Model": "Logistic Regression",
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1_Score": f1,
                "ROC_AUC": roc_auc
            }
        ]
    )


    print("\nCLASSIFICATION MODEL PERFORMANCE")
    print("-" * 60)

    print(
        classification_results.to_string(
            index=False
        )
    )


    # Save results
    os.makedirs(
        RESULTS_DIRECTORY,
        exist_ok=True
    )


    results_file = os.path.join(
        RESULTS_DIRECTORY,
        "classification_model_results.csv"
    )


    classification_results.to_csv(
        results_file,
        index=False
    )


    print(
        f"\nClassification results saved to: "
        f"{results_file}"
    )


    # Confusion Matrix
    confusion_matrix_values = confusion_matrix(
        y_test,
        predictions
    )


    print("\nCONFUSION MATRIX")
    print("-" * 60)

    print(confusion_matrix_values)


    os.makedirs(
        PLOTS_DIRECTORY,
        exist_ok=True
    )


    ConfusionMatrixDisplay(
        confusion_matrix=confusion_matrix_values,
        display_labels=[
            "Not Purchased",
            "Purchased"
        ]
    ).plot()


    plt.title(
        "Logistic Regression Confusion Matrix"
    )


    confusion_matrix_file = os.path.join(
        PLOTS_DIRECTORY,
        "10_confusion_matrix.png"
    )


    plt.tight_layout()

    plt.savefig(
        confusion_matrix_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"Saved plot: "
        f"{confusion_matrix_file}"
    )


    # ROC Curve
    RocCurveDisplay.from_predictions(
        y_test,
        purchase_probabilities
    )


    plt.title(
        "Logistic Regression ROC Curve"
    )


    roc_curve_file = os.path.join(
        PLOTS_DIRECTORY,
        "11_roc_curve.png"
    )


    plt.tight_layout()

    plt.savefig(
        roc_curve_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"Saved plot: {roc_curve_file}"
    )


    # Example Purchase Prediction
    example_customer = X_test.iloc[[0]]

    actual_purchase = y_test.iloc[0]

    predicted_purchase = (
        logistic_model.predict(
            example_customer
        )[0]
    )

    predicted_probability = (
        logistic_model.predict_proba(
            example_customer
        )[0][1]
    )


    print("\nEXAMPLE PURCHASE PREDICTION")
    print("-" * 60)


    print(
        "Actual Purchase Status:",
        "Purchased"
        if actual_purchase == 1
        else "Not Purchased"
    )


    print(
        "Predicted Purchase Status:",
        "Purchased"
        if predicted_purchase == 1
        else "Not Purchased"
    )


    print(
        f"Purchase Probability: "
        f"{predicted_probability * 100:.2f}%"
    )


    print(
        "\nClassification model training completed."
    )


    return (
        logistic_model,
        classification_results
    )