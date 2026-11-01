import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from .config import MODELS_DIR, RESULTS_DIR, CLASS_NAMES
from .data_loader import create_or_load_splits
from .dataset import build_dataset
from .ensemble import majority_vote, soft_vote, weighted_soft_vote, disagreement_rate

MODEL_NAMES = ["cnn_baseline", "cnn_regularized", "cnn_deep"]

def metrics_for(name, y_true, y_pred):
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="weighted", zero_division=0
    )
    return {
        "model": name,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
    }

def save_confusion(name, y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(CLASS_NAMES))))
    plt.figure(figsize=(8, 7))
    plt.imshow(cm)
    plt.xticks(range(len(CLASS_NAMES)), CLASS_NAMES, rotation=40, ha="right")
    plt.yticks(range(len(CLASS_NAMES)), CLASS_NAMES)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix - {name}")
    plt.colorbar()
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, str(cm[i, j]), ha="center", va="center")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"confusion_matrix_{name}.png", dpi=160)
    plt.close()

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    _, _, test_df = create_or_load_splits()
    test_ds = build_dataset(test_df)
    y_true = test_df["label"].to_numpy()

    probabilities = []
    rows = []
    for name in MODEL_NAMES:
        model = tf.keras.models.load_model(MODELS_DIR / f"{name}.keras")
        probs = model.predict(test_ds, verbose=0)
        probabilities.append(probs)
        pred = probs.argmax(axis=1)
        rows.append(metrics_for(name, y_true, pred))
        save_confusion(name, y_true, pred)

    majority_pred = majority_vote(probabilities)
    soft_pred, _ = soft_vote(probabilities)

    validation_accuracy = []
    train_df, val_df, _ = create_or_load_splits()
    val_ds = build_dataset(val_df)
    y_val = val_df["label"].to_numpy()
    for name in MODEL_NAMES:
        model = tf.keras.models.load_model(MODELS_DIR / f"{name}.keras")
        validation_accuracy.append(accuracy_score(y_val, model.predict(val_ds, verbose=0).argmax(axis=1)))

    weighted_pred, _ = weighted_soft_vote(probabilities, validation_accuracy)

    for name, pred in [
        ("ensemble_majority", majority_pred),
        ("ensemble_soft", soft_pred),
        ("ensemble_weighted", weighted_pred),
    ]:
        rows.append(metrics_for(name, y_true, pred))
        save_confusion(name, y_true, pred)

    pd.DataFrame(rows).to_csv(RESULTS_DIR / "evaluation_results.csv", index=False)
    with open(RESULTS_DIR / "evaluation_details.json", "w") as f:
        json.dump({
            "classes": CLASS_NAMES,
            "weighted_voting_weights_from_validation": validation_accuracy,
            "model_disagreement_rate": disagreement_rate(probabilities),
        }, f, indent=2)

    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
