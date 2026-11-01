"""
Production Prediction Pipeline (Sections 61-64).
Loads all 3 CNNs, runs soft voting, returns class + confidence,
optionally flags low-confidence predictions for manual review.
"""

import os
import time
import numpy as np
from tensorflow.keras.models import load_model

from data_loader import CLASS_NAMES
from ensemble import soft_voting, get_all_probs

MODELS_DIR = "models"
CONFIDENCE_THRESHOLD = 0.80


def load_ensemble():
    names = ["cnn_baseline", "cnn_regularized", "cnn_deep"]
    paths = [os.path.join(MODELS_DIR, f"{n}.keras") for n in names]
    return [load_model(p) for p in paths], names


def predict(image_batch, models, model_names, debug=False):
    """
    image_batch: normalized numpy array, shape (n, 32, 32, 3)
    Returns a list of prediction dicts (Section 64 format).
    """
    start = time.perf_counter()
    probs_list = get_all_probs(models, image_batch)
    preds, avg_probs = soft_voting(probs_list)
    elapsed_ms = (time.perf_counter() - start) * 1000

    results = []
    for i, pred_class in enumerate(preds):
        confidence = float(avg_probs[i][pred_class])
        entry = {
            "predictedClass": CLASS_NAMES[pred_class],
            "confidence": round(confidence, 4),
            "inferenceTimeMs": round(elapsed_ms / len(image_batch), 2),
            "decision": "Accept" if confidence >= CONFIDENCE_THRESHOLD else "Manual Review",
        }
        if debug:
            entry["modelPredictions"] = {
                name: CLASS_NAMES[int(np.argmax(probs_list[j][i]))]
                for j, name in enumerate(model_names)
            }
        results.append(entry)
    return results


if __name__ == "__main__":
    from data_loader import load_cifar10
    from preprocessing import prepare_dataset

    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()
    (_, _), (_, _), (x_test, y_test) = prepare_dataset(
        x_train, y_train, x_val, y_val, x_test, y_test
    )

    models, names = load_ensemble()
    output = predict(x_test[:5], models, names, debug=True)
    for r in output:
        print(r)
