from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras

from src.data_loader import load_datasets, optimize_dataset


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"

# Model files
MODEL_PATHS = {
    "baseline_cnn": MODELS_DIR / "baseline_cnn.keras",
    "deep_cnn": MODELS_DIR / "deep_cnn.keras",
    "regularized_cnn": MODELS_DIR / "regularized_cnn.keras",
}

# Classification threshold
THRESHOLD = 0.5


def load_models():
    """Load all trained CNN models."""
    models = {}

    for name, path in MODEL_PATHS.items():
        if not path.exists():
            raise FileNotFoundError(
                f"Model not found: {path}"
            )

        print(f"Loading {name}...")
        models[name] = keras.models.load_model(path)

    return models


def get_predictions(models, test_ds):
    """
    Generate predictions from every model.

    Returns:
        Dictionary containing prediction probabilities.
    """
    predictions = {}

    for name, model in models.items():
        print(f"\nPredicting with {name}...")

        predictions[name] = model.predict(
            test_ds,
            verbose=1
        ).flatten()

    return predictions


def ensemble_predictions(predictions):
    """
    Combine model probabilities using soft voting.

    Soft voting:
        ensemble_probability =
            (baseline + deep + regularized) / 3
    """

    probability_matrix = np.column_stack(
        [
            predictions["baseline_cnn"],
            predictions["deep_cnn"],
            predictions["regularized_cnn"],
        ]
    )

    ensemble_probability = np.mean(
        probability_matrix,
        axis=1
    )

    ensemble_labels = (
        ensemble_probability >= THRESHOLD
    ).astype(int)

    return ensemble_probability, ensemble_labels


def get_true_labels(test_ds):
    """Extract true labels from the test dataset."""
    labels = []

    for _, batch_labels in test_ds:
        labels.extend(batch_labels.numpy())

    return np.array(labels)


def evaluate_ensemble(y_true, y_pred):
    """Calculate ensemble classification metrics."""

    accuracy = np.mean(y_true == y_pred)

    true_positive = np.sum(
        (y_true == 1) & (y_pred == 1)
    )

    false_positive = np.sum(
        (y_true == 0) & (y_pred == 1)
    )

    false_negative = np.sum(
        (y_true == 1) & (y_pred == 0)
    )

    precision = (
        true_positive /
        (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else 0.0
    )

    recall = (
        true_positive /
        (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else 0.0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
    }


def save_predictions(
    y_true,
    ensemble_probability,
    ensemble_labels,
):
    """Save ensemble predictions to CSV."""

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = RESULTS_DIR / "ensemble_predictions.csv"

    data = np.column_stack(
        [
            y_true,
            ensemble_probability,
            ensemble_labels,
        ]
    )

    np.savetxt(
        output_path,
        data,
        delimiter=",",
        header="true_label,ensemble_probability,predicted_label",
        comments="",
        fmt=["%d", "%.6f", "%d"],
    )

    print(
        f"\nPredictions saved to: {output_path}"
    )


def main():
    """Run the complete ensemble pipeline."""

    print("=" * 70)
    print("TASK 15 - ENSEMBLE CNN CLASSIFIER")
    print("=" * 70)

    # Load datasets
    print("\nLoading datasets...")

    train_ds, validation_ds, test_ds = load_datasets()

    test_ds = optimize_dataset(test_ds)

    print(
        f"\nTest classes: {test_ds.class_names}"
        if hasattr(test_ds, "class_names")
        else "\nTest dataset loaded."
    )

    # Load models
    print("\n" + "=" * 70)
    print("LOADING TRAINED MODELS")
    print("=" * 70)

    models = load_models()

    print(
        f"\nSuccessfully loaded {len(models)} models."
    )

    # Generate predictions
    print("\n" + "=" * 70)
    print("GENERATING MODEL PREDICTIONS")
    print("=" * 70)

    predictions = get_predictions(
        models,
        test_ds
    )

    # True labels
    y_true = get_true_labels(test_ds)

    # Ensemble
    print("\n" + "=" * 70)
    print("CREATING ENSEMBLE")
    print("=" * 70)

    ensemble_probability, ensemble_labels = (
        ensemble_predictions(predictions)
    )

    # Evaluate
    metrics = evaluate_ensemble(
        y_true,
        ensemble_labels
    )

    print("\nENSEMBLE RESULTS")
    print("-" * 40)
    print(
        f"Accuracy : {metrics['accuracy']:.4f}"
    )
    print(
        f"Precision: {metrics['precision']:.4f}"
    )
    print(
        f"Recall   : {metrics['recall']:.4f}"
    )

    print(
        f"\nTest samples: {len(y_true)}"
    )

    # Save
    save_predictions(
        y_true,
        ensemble_probability,
        ensemble_labels,
    )

    print("\n" + "=" * 70)
    print("ENSEMBLE PIPELINE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()