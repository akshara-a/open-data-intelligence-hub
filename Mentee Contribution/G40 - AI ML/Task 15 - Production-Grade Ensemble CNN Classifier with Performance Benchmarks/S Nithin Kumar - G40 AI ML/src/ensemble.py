import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_prepare_data


MODEL_DIR = "models"
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


def load_models():

    print("Loading trained models...")

    baseline = tf.keras.models.load_model(
        os.path.join(MODEL_DIR, "baseline_cnn.keras")
    )

    regularized = tf.keras.models.load_model(
        os.path.join(MODEL_DIR, "regularized_cnn.keras")
    )

    deep = tf.keras.models.load_model(
        os.path.join(MODEL_DIR, "deep_cnn.keras")
    )

    print("All models loaded successfully!\n")

    return baseline, regularized, deep


def main():

    # Load dataset
    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        class_names
    ) = load_and_prepare_data()

    # Load trained models
    baseline, regularized, deep = load_models()

    print("Generating predictions...\n")

    # Prediction probabilities
    baseline_pred = baseline.predict(X_test, verbose=1)
    regularized_pred = regularized.predict(X_test, verbose=1)
    deep_pred = deep.predict(X_test, verbose=1)

    # ==========================================================
    # WEIGHTED ENSEMBLE
    # ==========================================================

    ensemble_prob = (
        0.30 * baseline_pred +
        0.15 * regularized_pred +
        0.55 * deep_pred
    )

    # Final predicted class
    y_pred = np.argmax(ensemble_prob, axis=1)

    # ==========================================================
    # METRICS
    # ==========================================================

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

    print("=" * 70)
    print("ENSEMBLE CNN RESULTS")
    print("=" * 70)

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-Score  : {f1:.4f}")

    # Save results
    results = pd.DataFrame([
        {
            "Model": "weighted_ensemble",
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1_Score": f1,
            "Baseline_Weight": 0.30,
            "Regularized_Weight": 0.15,
            "Deep_Weight": 0.55
        }
    ])

    results.to_csv(
        os.path.join(RESULTS_DIR, "ensemble_results.csv"),
        index=False
    )

    print("\nResults saved to:")
    print("results\\ensemble_results.csv")


if __name__ == "__main__":
    main()