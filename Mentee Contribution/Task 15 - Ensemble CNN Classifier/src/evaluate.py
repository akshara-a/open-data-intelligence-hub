import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_prepare_data


MODEL_DIR = "models"
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


def evaluate_model(model_name, X_test, y_test, class_names):

    print("\n" + "=" * 70)
    print(f"EVALUATING: {model_name.upper()}")
    print("=" * 70)

    model_path = os.path.join(
        MODEL_DIR,
        f"{model_name}.keras"
    )

    model = tf.keras.models.load_model(model_path)

    # Get prediction probabilities
    y_prob = model.predict(X_test, verbose=1)

    # Convert probabilities to predicted classes
    y_pred = np.argmax(y_prob, axis=1)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    print(f"\nAccuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-Score  : {f1:.4f}")

    # Classification report
    report = classification_report(
        y_test,
        y_pred,
        target_names=class_names,
        zero_division=0
    )

    print("\nClassification Report:\n")
    print(report)

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names
    )

    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()

    image_path = os.path.join(
        RESULTS_DIR,
        f"{model_name}_confusion_matrix.png"
    )

    plt.savefig(image_path, dpi=300)
    plt.close()

    print(f"\nConfusion matrix saved to:")
    print(image_path)

    return {
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1_Score": f1
    }


def main():

    # Load data
    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        class_names
    ) = load_and_prepare_data()

    model_names = [
        "baseline_cnn",
        "regularized_cnn",
        "deep_cnn"
    ]

    all_results = []

    for model_name in model_names:

        result = evaluate_model(
            model_name,
            X_test,
            y_test,
            class_names
        )

        all_results.append(result)

    # Save comparison
    results_df = pd.DataFrame(all_results)

    results_path = os.path.join(
        RESULTS_DIR,
        "model_comparison.csv"
    )

    results_df.to_csv(results_path, index=False)

    print("\n" + "=" * 70)
    print("FINAL MODEL COMPARISON")
    print("=" * 70)

    print(results_df.to_string(index=False))

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()