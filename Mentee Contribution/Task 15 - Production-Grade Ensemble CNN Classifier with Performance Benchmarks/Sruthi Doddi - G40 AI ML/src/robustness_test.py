"""
Part 9 — Robustness Testing (Sections 57-60).
Creates modified versions of test images (rotated, blurred, noisy,
dark, bright, cropped) and compares individual CNNs vs. the ensemble.
"""

import os
import numpy as np
import pandas as pd
from scipy.ndimage import rotate, gaussian_filter
from tensorflow.keras.models import load_model

from data_loader import load_cifar10
from preprocessing import prepare_dataset
from ensemble import soft_voting, get_all_probs

MODELS_DIR = "models"
RESULTS_DIR = "results"
N_SAMPLES = 200  # subset of test set for speed


def make_rotated(x): return np.array([rotate(img, 25, reshape=False, mode="nearest") for img in x])
def make_blurred(x): return np.array([gaussian_filter(img, sigma=(1.2, 1.2, 0)) for img in x])
def make_noisy(x):
    noise = np.random.normal(0, 0.08, x.shape)
    return np.clip(x + noise, 0, 1)
def make_dark(x): return np.clip(x * 0.4, 0, 1)
def make_bright(x): return np.clip(x * 1.6, 0, 1)
def make_cropped(x):
    # zero out a border region to simulate partial cropping
    out = x.copy()
    out[:, :6, :, :] = 0
    out[:, -6:, :, :] = 0
    return out


TRANSFORMS = {
    "original": lambda x: x,
    "rotated": make_rotated,
    "blurred": make_blurred,
    "noisy": make_noisy,
    "dark": make_dark,
    "bright": make_bright,
    "cropped": make_cropped,
}


def accuracy_under_transform(models, model_names, x, y_true):
    row = {}
    probs_list = get_all_probs(models, x)
    for name, probs in zip(model_names, probs_list):
        preds = np.argmax(probs, axis=1)
        row[name] = float(np.mean(preds == y_true))

    ens_pred, _ = soft_voting(probs_list)
    row["ensemble_soft"] = float(np.mean(ens_pred == y_true))
    return row


def main():
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()
    (_, _), (_, _), (x_test, y_test) = prepare_dataset(
        x_train, y_train, x_val, y_val, x_test, y_test
    )

    x_sub = x_test[:N_SAMPLES]
    y_true = np.argmax(y_test[:N_SAMPLES], axis=1)

    model_names = ["cnn_baseline", "cnn_regularized", "cnn_deep"]
    paths = [os.path.join(MODELS_DIR, f"{n}.keras") for n in model_names]
    if not all(os.path.exists(p) for p in paths):
        print("Train all three models first (src/train.py).")
        return
    models = [load_model(p) for p in paths]

    results = []
    for transform_name, fn in TRANSFORMS.items():
        x_mod = fn(x_sub)
        row = accuracy_under_transform(models, model_names, x_mod, y_true)
        row["condition"] = transform_name
        results.append(row)
        print(transform_name, row)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame(results).to_csv(
        os.path.join(RESULTS_DIR, "robustness_results.csv"), index=False
    )


if __name__ == "__main__":
    main()
