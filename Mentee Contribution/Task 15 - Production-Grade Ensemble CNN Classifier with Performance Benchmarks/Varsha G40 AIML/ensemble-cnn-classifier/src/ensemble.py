import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import load_small_cifar10


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)

MODEL_PATHS = {
    "CNN1_Baseline": os.path.join(MODEL_DIR, "cnn_baseline.keras"),
    "CNN2_Regularized": os.path.join(MODEL_DIR, "cnn_regularized.keras"),
    "CNN3_Deep": os.path.join(MODEL_DIR, "cnn_deep.keras"),
}


# ---------------------------------------------------------
# Load models
# ---------------------------------------------------------

def load_models():

    models = {}

    print("\nLoading trained CNN models...")
    print("=" * 60)

    for name, path in MODEL_PATHS.items():

        if not os.path.exists(path):
            print(f"ERROR: Model not found: {path}")
            continue

        models[name] = tf.keras.models.load_model(path)

        print(f"Loaded: {name}")

    print("=" * 60)

    return models


# ---------------------------------------------------------
# Majority Voting
# ---------------------------------------------------------

def majority_voting(predictions):

    """
    predictions shape:

    (number_of_models, number_of_images)
    """

    predictions = np.array(predictions)

    final_predictions = []

    for i in range(predictions.shape[1]):

        votes = predictions[:, i]

        counts = np.bincount(votes, minlength=10)

        final_class = np.argmax(counts)

        final_predictions.append(final_class)

    return np.array(final_predictions)


# ---------------------------------------------------------
# Soft Voting
# ---------------------------------------------------------

def soft_voting(probabilities):

    """
    Average probability predictions from all CNNs.
    """

    probabilities = np.array(probabilities)

    average_probability = np.mean(probabilities, axis=0)

    final_predictions = np.argmax(
        average_probability,
        axis=1
    )

    return final_predictions, average_probability


# ---------------------------------------------------------
# Calculate Metrics
# ---------------------------------------------------------

def calculate_metrics(y_true, y_pred):

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# ---------------------------------------------------------
# Main Ensemble Process
# ---------------------------------------------------------

def main():

    print("\n")
    print("=" * 60)
    print("ENSEMBLE CNN CLASSIFIER")
    print("=" * 60)

    # Load dataset
    print("\nLoading CIFAR-10 subset...")

    (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test
    ) = load_small_cifar10()

    # Convert labels to 1D
    y_test = np.array(y_test).flatten()

    print(f"Test images: {X_test.shape}")
    print(f"Test labels: {y_test.shape}")

    # Load models
    models = load_models()

    if len(models) < 3:

        print("\nERROR: All 3 trained models are required.")

        return

    # -----------------------------------------------------
    # Generate predictions
    # -----------------------------------------------------

    class_predictions = []
    probability_predictions = []

    individual_results = []

    print("\nGenerating predictions...")
    print("=" * 60)

    for name, model in models.items():

        print(f"\nPredicting with {name}...")

        probabilities = model.predict(
            X_test,
            verbose=0
        )

        predictions = np.argmax(
            probabilities,
            axis=1
        )

        class_predictions.append(predictions)

        probability_predictions.append(probabilities)

        metrics = calculate_metrics(
            y_test,
            predictions
        )

        individual_results.append({
            "Model": name,
            "Accuracy": metrics["accuracy"],
            "Precision": metrics["precision"],
            "Recall": metrics["recall"],
            "F1": metrics["f1"]
        })

    # -----------------------------------------------------
    # Majority Voting
    # -----------------------------------------------------

    print("\n")
    print("=" * 60)
    print("MAJORITY VOTING")
    print("=" * 60)

    majority_predictions = majority_voting(
        class_predictions
    )

    majority_metrics = calculate_metrics(
        y_test,
        majority_predictions
    )

    print(
        f"Accuracy : {majority_metrics['accuracy']:.4f}"
    )

    print(
        f"Precision: {majority_metrics['precision']:.4f}"
    )

    print(
        f"Recall   : {majority_metrics['recall']:.4f}"
    )

    print(
        f"F1 Score : {majority_metrics['f1']:.4f}"
    )

    # -----------------------------------------------------
    # Soft Voting
    # -----------------------------------------------------

    print("\n")
    print("=" * 60)
    print("SOFT VOTING")
    print("=" * 60)

    soft_predictions, average_probability = soft_voting(
        probability_predictions
    )

    soft_metrics = calculate_metrics(
        y_test,
        soft_predictions
    )

    print(
        f"Accuracy : {soft_metrics['accuracy']:.4f}"
    )

    print(
        f"Precision: {soft_metrics['precision']:.4f}"
    )

    print(
        f"Recall   : {soft_metrics['recall']:.4f}"
    )

    print(
        f"F1 Score : {soft_metrics['f1']:.4f}"
    )

    # -----------------------------------------------------
    # Final Comparison
    # -----------------------------------------------------

    final_results = individual_results.copy()

    final_results.append({
        "Model": "Majority Voting",
        "Accuracy": majority_metrics["accuracy"],
        "Precision": majority_metrics["precision"],
        "Recall": majority_metrics["recall"],
        "F1": majority_metrics["f1"]
    })

    final_results.append({
        "Model": "Soft Voting",
        "Accuracy": soft_metrics["accuracy"],
        "Precision": soft_metrics["precision"],
        "Recall": soft_metrics["recall"],
        "F1": soft_metrics["f1"]
    })

    results_df = pd.DataFrame(final_results)

    # -----------------------------------------------------
    # Save results
    # -----------------------------------------------------

    csv_path = os.path.join(
        RESULTS_DIR,
        "ensemble_results.csv"
    )

    results_df.to_csv(
        csv_path,
        index=False
    )

    print("\n")
    print("=" * 60)
    print("FINAL ENSEMBLE RESULTS")
    print("=" * 60)

    print(
        results_df.to_string(index=False)
    )

    print("\nResults saved to:")
    print(csv_path)

    # -----------------------------------------------------
    # Save predictions
    # -----------------------------------------------------

    prediction_df = pd.DataFrame({
        "Actual": y_test,
        "Majority_Voting": majority_predictions,
        "Soft_Voting": soft_predictions
    })

    prediction_path = os.path.join(
        RESULTS_DIR,
        "ensemble_predictions.csv"
    )

    prediction_df.to_csv(
        prediction_path,
        index=False
    )

    print("\nPredictions saved to:")
    print(prediction_path)

    print("\n")
    print("=" * 60)
    print("ENSEMBLE EVALUATION COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()