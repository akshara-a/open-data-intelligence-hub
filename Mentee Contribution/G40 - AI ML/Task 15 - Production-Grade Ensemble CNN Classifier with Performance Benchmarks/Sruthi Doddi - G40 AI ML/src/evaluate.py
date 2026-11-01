"""
Part 6 — Evaluate every CNN separately (Sections 31-36).
Computes accuracy, precision, recall, F1 and confusion matrix.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix,
)
from tensorflow.keras.models import load_model

from data_loader import load_cifar10, CLASS_NAMES
from preprocessing import prepare_dataset

RESULTS_DIR = "results"
MODELS_DIR = "models"


def evaluate_model(model, x_test, y_test_onehot, name):
    y_true = np.argmax(y_test_onehot, axis=1)
    probs = model.predict(x_test, verbose=0)
    y_pred = np.argmax(probs, axis=1)

    metrics = {
        "model": name,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="macro"),
        "recall": recall_score(y_true, y_pred, average="macro"),
        "f1": f1_score(y_true, y_pred, average="macro"),
    }

    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, name)

    return metrics, probs, y_true


def plot_confusion_matrix(cm, name):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title(f"Confusion Matrix — {name}")
    plt.xlabel("Predicted"); plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, f"confusion_matrix_{name}.png"))
    plt.close()


def main():
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()
    (_, _), (_, _), (x_test, y_test) = prepare_dataset(
        x_train, y_train, x_val, y_val, x_test, y_test
    )

    model_files = {
        "cnn_baseline": "cnn_baseline.keras",
        "cnn_regularized": "cnn_regularized.keras",
        "cnn_deep": "cnn_deep.keras",
    }

    all_metrics = []
    for name, fname in model_files.items():
        path = os.path.join(MODELS_DIR, fname)
        if not os.path.exists(path):
            print(f"Skipping {name}: {path} not found (train it first).")
            continue
        model = load_model(path)
        metrics, _, _ = evaluate_model(model, x_test, y_test, name)
        all_metrics.append(metrics)
        print(metrics)

    import pandas as pd
    pd.DataFrame(all_metrics).to_csv(
        os.path.join(RESULTS_DIR, "individual_cnn_results.csv"), index=False
    )


if __name__ == "__main__":
    main()
