"""
Part 7 — Ensemble (Sections 37-43).
Implements Majority (Hard) Voting, Soft Voting, and Weighted Soft Voting.
Weights for weighted voting must come from VALIDATION accuracy only
(Section 43) — never from the test set.
"""

import os
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix,
)

from data_loader import load_cifar10, CLASS_NAMES
from preprocessing import prepare_dataset
from evaluate import plot_confusion_matrix

MODELS_DIR = "models"
RESULTS_DIR = "results"


def get_all_probs(models, x):
    """Returns a list of probability arrays, one per model."""
    return [m.predict(x, verbose=0) for m in models]


def majority_voting(probs_list):
    """Hard voting: each model votes its own top class (Section 38)."""
    preds = np.array([np.argmax(p, axis=1) for p in probs_list])  # (n_models, n_samples)
    final = np.array([
        np.bincount(preds[:, i], minlength=probs_list[0].shape[1]).argmax()
        for i in range(preds.shape[1])
    ])
    return final


def soft_voting(probs_list):
    """Averages probabilities across models (Section 40)."""
    avg = np.mean(probs_list, axis=0)
    return np.argmax(avg, axis=1), avg


def weighted_soft_voting(probs_list, weights):
    """Weighted average of probabilities (Section 42)."""
    weights = np.array(weights) / np.sum(weights)
    avg = np.zeros_like(probs_list[0])
    for w, p in zip(weights, probs_list):
        avg += w * p
    return np.argmax(avg, axis=1), avg


def compute_validation_weights(models, x_val, y_val_onehot):
    """Uses validation accuracy to derive weights (Section 43)."""
    y_true = np.argmax(y_val_onehot, axis=1)
    accs = []
    for m in models:
        preds = np.argmax(m.predict(x_val, verbose=0), axis=1)
        accs.append(accuracy_score(y_true, preds))
    return accs  # used directly as weights (proportional to val accuracy)


def score(y_true, y_pred, name):
    return {
        "model": name,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="macro"),
        "recall": recall_score(y_true, y_pred, average="macro"),
        "f1": f1_score(y_true, y_pred, average="macro"),
    }


def main():
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()
    (_, _), (x_val, y_val), (x_test, y_test) = prepare_dataset(
        x_train, y_train, x_val, y_val, x_test, y_test
    )

    model_names = ["cnn_baseline", "cnn_regularized", "cnn_deep"]
    paths = [os.path.join(MODELS_DIR, f"{n}.keras") for n in model_names]
    if not all(os.path.exists(p) for p in paths):
        print("Train all three models first (src/train.py).")
        return

    models = [load_model(p) for p in paths]

    # weights from validation set only
    weights = compute_validation_weights(models, x_val, y_val)
    print("Validation-based weights:", dict(zip(model_names, weights)))

    # now evaluate ensemble on the untouched test set
    probs_list = get_all_probs(models, x_test)
    y_true = np.argmax(y_test, axis=1)

    results = []

    maj_pred = majority_voting(probs_list)
    results.append(score(y_true, maj_pred, "majority_voting"))
    plot_confusion_matrix(confusion_matrix(y_true, maj_pred), "ensemble_majority")

    soft_pred, _ = soft_voting(probs_list)
    results.append(score(y_true, soft_pred, "soft_voting"))
    plot_confusion_matrix(confusion_matrix(y_true, soft_pred), "ensemble_soft")

    wsoft_pred, _ = weighted_soft_voting(probs_list, weights)
    results.append(score(y_true, wsoft_pred, "weighted_soft_voting"))
    plot_confusion_matrix(confusion_matrix(y_true, wsoft_pred), "ensemble_weighted")

    import pandas as pd
    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame(results).to_csv(
        os.path.join(RESULTS_DIR, "ensemble_results.csv"), index=False
    )
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
