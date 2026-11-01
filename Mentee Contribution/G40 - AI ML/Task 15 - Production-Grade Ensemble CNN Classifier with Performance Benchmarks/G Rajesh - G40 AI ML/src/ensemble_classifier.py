import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


# Allow importing data_loader.py from the same src directory.
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import (
    prepare_datasets,
    create_tf_datasets,
)


MODEL_1_PATH = "models/cnn_model_1.keras"
MODEL_2_PATH = "models/cnn_model_2.keras"

REPORTS_DIR = "reports"

CLASS_NAMES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def load_models():
    """Load the two trained CNN models."""

    print("\nLoading CNN Model 1...")
    model_1 = tf.keras.models.load_model(MODEL_1_PATH)

    print("Loading CNN Model 2...")
    model_2 = tf.keras.models.load_model(MODEL_2_PATH)

    print("Both models loaded successfully.")

    return model_1, model_2


def get_test_predictions(model_1, model_2, x_test, y_test):
    """Generate predictions from both models and ensemble them."""

    print("\nGenerating predictions from CNN Model 1...")
    predictions_1 = model_1.predict(
        x_test,
        batch_size=64,
        verbose=1,
    )

    print("\nGenerating predictions from CNN Model 2...")
    predictions_2 = model_2.predict(
        x_test,
        batch_size=64,
        verbose=1,
    )

    # Average the class probabilities.
    ensemble_probabilities = (
        predictions_1 + predictions_2
    ) / 2.0

    ensemble_predictions = np.argmax(
        ensemble_probabilities,
        axis=1,
    )

    true_labels = y_test.flatten()

    return (
        predictions_1,
        predictions_2,
        ensemble_probabilities,
        ensemble_predictions,
        true_labels,
    )


def calculate_metrics(
    predictions_1,
    predictions_2,
    ensemble_predictions,
    true_labels,
):
    """Calculate individual and ensemble accuracy."""

    model_1_predictions = np.argmax(
        predictions_1,
        axis=1,
    )

    model_2_predictions = np.argmax(
        predictions_2,
        axis=1,
    )

    model_1_accuracy = accuracy_score(
        true_labels,
        model_1_predictions,
    )

    model_2_accuracy = accuracy_score(
        true_labels,
        model_2_predictions,
    )

    ensemble_accuracy = accuracy_score(
        true_labels,
        ensemble_predictions,
    )

    print("\n" + "=" * 60)
    print("TASK 15 - ENSEMBLE RESULTS")
    print("=" * 60)

    print(
        f"CNN Model 1 Accuracy: {model_1_accuracy:.4f}"
    )

    print(
        f"CNN Model 1 Accuracy: {model_1_accuracy * 100:.2f}%"
    )

    print(
        f"\nCNN Model 2 Accuracy: {model_2_accuracy:.4f}"
    )

    print(
        f"CNN Model 2 Accuracy: {model_2_accuracy * 100:.2f}%"
    )

    print(
        f"\nEnsemble Accuracy:    {ensemble_accuracy:.4f}"
    )

    print(
        f"Ensemble Accuracy:    {ensemble_accuracy * 100:.2f}%"
    )

    return (
        model_1_predictions,
        model_2_predictions,
        ensemble_accuracy,
    )


def save_confusion_matrix(
    true_labels,
    ensemble_predictions,
):
    """Save ensemble confusion matrix."""

    os.makedirs(REPORTS_DIR, exist_ok=True)

    cm = confusion_matrix(
        true_labels,
        ensemble_predictions,
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=CLASS_NAMES,
    )

    fig, ax = plt.subplots(
        figsize=(12, 10)
    )

    display.plot(
        ax=ax,
        xticks_rotation=45,
        colorbar=False,
    )

    ax.set_title(
        "Task 15 - Ensemble CNN Confusion Matrix"
    )

    plt.tight_layout()

    output_path = os.path.join(
        REPORTS_DIR,
        "ensemble_confusion_matrix.png",
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"\nConfusion matrix saved to: {output_path}"
    )


def save_classification_report(
    true_labels,
    ensemble_predictions,
):
    """Save ensemble classification report."""

    report = classification_report(
        true_labels,
        ensemble_predictions,
        target_names=CLASS_NAMES,
        digits=4,
    )

    print("\n" + "=" * 60)
    print("ENSEMBLE CLASSIFICATION REPORT")
    print("=" * 60)
    print(report)

    output_path = os.path.join(
        REPORTS_DIR,
        "ensemble_classification_report.txt",
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(
            "TASK 15 - ENSEMBLE CNN CLASSIFICATION REPORT\n"
        )
        file.write("=" * 60 + "\n\n")
        file.write(report)

    print(
        f"Classification report saved to: {output_path}"
    )


def save_comparison_graph(
    model_1_accuracy,
    model_2_accuracy,
    ensemble_accuracy,
):
    """Save accuracy comparison graph."""

    os.makedirs(REPORTS_DIR, exist_ok=True)

    names = [
        "CNN Model 1",
        "CNN Model 2",
        "Ensemble",
    ]

    values = [
        model_1_accuracy,
        model_2_accuracy,
        ensemble_accuracy,
    ]

    plt.figure(figsize=(10, 6))

    plt.bar(
        names,
        values,
    )

    plt.title(
        "Task 15 - CNN Model Accuracy Comparison"
    )

    plt.ylabel("Accuracy")

    plt.ylim(
        0,
        1,
    )

    for index, value in enumerate(values):
        plt.text(
            index,
            value + 0.02,
            f"{value * 100:.2f}%",
            ha="center",
        )

    plt.tight_layout()

    output_path = os.path.join(
        REPORTS_DIR,
        "ensemble_accuracy_comparison.png",
    )

    plt.savefig(
        output_path,
        dpi=150,
    )

    plt.close()

    print(
        f"Accuracy comparison saved to: {output_path}"
    )


def main():

    print("=" * 60)
    print("TASK 15 - ENSEMBLE CNN CLASSIFIER")
    print("=" * 60)

    # Check that both models exist.
    if not os.path.exists(MODEL_1_PATH):
        raise FileNotFoundError(
            f"Model 1 not found: {MODEL_1_PATH}"
        )

    if not os.path.exists(MODEL_2_PATH):
        raise FileNotFoundError(
            f"Model 2 not found: {MODEL_2_PATH}"
        )

    print("\nPreparing CIFAR-10 test data...")

    (
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test,
    ) = prepare_datasets()

    # Create TensorFlow datasets to verify the complete pipeline.
    _, _, test_ds = create_tf_datasets(
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test,
    )

    print(
        f"\nTest dataset contains {len(x_test)} images."
    )

    # Load trained models.
    model_1, model_2 = load_models()

    # Generate predictions.
    (
        predictions_1,
        predictions_2,
        ensemble_probabilities,
        ensemble_predictions,
        true_labels,
    ) = get_test_predictions(
        model_1,
        model_2,
        x_test,
        y_test,
    )

    # Calculate metrics.
    (
        model_1_predictions,
        model_2_predictions,
        ensemble_accuracy,
    ) = calculate_metrics(
        predictions_1,
        predictions_2,
        ensemble_predictions,
        true_labels,
    )

    model_1_accuracy = accuracy_score(
        true_labels,
        model_1_predictions,
    )

    model_2_accuracy = accuracy_score(
        true_labels,
        model_2_predictions,
    )

    # Save reports and graphs.
    save_confusion_matrix(
        true_labels,
        ensemble_predictions,
    )

    save_classification_report(
        true_labels,
        ensemble_predictions,
    )

    save_comparison_graph(
        model_1_accuracy,
        model_2_accuracy,
        ensemble_accuracy,
    )

    # Save ensemble predictions.
    os.makedirs(
        "outputs",
        exist_ok=True,
    )

    predictions_path = (
        "outputs/ensemble_predictions.npy"
    )

    np.save(
        predictions_path,
        ensemble_predictions,
    )

    print(
        f"\nEnsemble predictions saved to: {predictions_path}"
    )

    # Save probabilities.
    probabilities_path = (
        "outputs/ensemble_probabilities.npy"
    )

    np.save(
        probabilities_path,
        ensemble_probabilities,
    )

    print(
        f"Ensemble probabilities saved to: {probabilities_path}"
    )

    print("\n" + "=" * 60)
    print("FINAL TASK 15 RESULTS")
    print("=" * 60)

    print(
        f"CNN Model 1: {model_1_accuracy * 100:.2f}%"
    )

    print(
        f"CNN Model 2: {model_2_accuracy * 100:.2f}%"
    )

    print(
        f"Ensemble:    {ensemble_accuracy * 100:.2f}%"
    )

    print("\nGenerated files:")

    print(
        "reports/ensemble_confusion_matrix.png"
    )

    print(
        "reports/ensemble_classification_report.txt"
    )

    print(
        "reports/ensemble_accuracy_comparison.png"
    )

    print(
        "outputs/ensemble_predictions.npy"
    )

    print(
        "outputs/ensemble_probabilities.npy"
    )

    print(
        "\nTASK 15 ENSEMBLE CNN CLASSIFIER COMPLETED SUCCESSFULLY."
    )


if __name__ == "__main__":
    main()