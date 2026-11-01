import os
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATHS
# ============================================================

SRC_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    SRC_DIR
)

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)

RESULTS_DIR = os.path.join(
    PROJECT_ROOT,
    "results"
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ============================================================
# IMPORT DATA LOADER
# ============================================================

from data_loader import load_cifar10


# ============================================================
# CLASS NAMES
# ============================================================

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
    "truck"
]


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATHS = {

    "cnn1": os.path.join(
        MODEL_DIR,
        "cnn_baseline.keras"
    ),

    "cnn2": os.path.join(
        MODEL_DIR,
        "cnn_regularized.keras"
    ),

    "cnn3": os.path.join(
        MODEL_DIR,
        "cnn_deep.keras"
    )
}


# ============================================================
# CHECK MODELS
# ============================================================

print("\n" + "=" * 60)
print("CHECKING MODEL FILES")
print("=" * 60)

for name, path in MODEL_PATHS.items():

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"\n{name.upper()} model not found:\n{path}"
        )

    print(
        f"{name.upper()} : FOUND"
    )


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "=" * 60)
print("LOADING DATASET")
print("=" * 60)

(
    x_train,
    y_train,
    x_val,
    y_val,
    x_test,
    y_test
) = load_cifar10()


# ============================================================
# LOAD MODELS
# ============================================================

print("\n" + "=" * 60)
print("LOADING MODELS")
print("=" * 60)

models = {}

for name, path in MODEL_PATHS.items():

    print(
        f"\nLoading {name.upper()}..."
    )

    models[name] = tf.keras.models.load_model(
        path
    )

    print(
        f"{name.upper()} loaded successfully."
    )


# ============================================================
# GENERATE VALIDATION PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("GENERATING VALIDATION PREDICTIONS")
print("=" * 60)

validation_probabilities = {}

for name, model in models.items():

    print(
        f"\nPredicting validation set with {name.upper()}..."
    )

    validation_probabilities[name] = model.predict(
        x_val,
        batch_size=32,
        verbose=1
    )


# ============================================================
# GENERATE TEST PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("GENERATING TEST PREDICTIONS")
print("=" * 60)

test_probabilities = {}

for name, model in models.items():

    print(
        f"\nPredicting test set with {name.upper()}..."
    )

    test_probabilities[name] = model.predict(
        x_test,
        batch_size=32,
        verbose=1
    )


# ============================================================
# WEIGHT COMBINATIONS
# ============================================================

weight_combinations = [

    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),

    (0.5, 0.0, 0.5),
    (0.0, 0.5, 0.5),
    (0.5, 0.5, 0.0),

    (0.2, 0.2, 0.6),
    (0.2, 0.1, 0.7),
    (0.1, 0.2, 0.7),

    (0.1, 0.1, 0.8),
    (0.1, 0.3, 0.6),
    (0.3, 0.1, 0.6),

    (0.2, 0.3, 0.5),
    (0.3, 0.2, 0.5),
    (0.4, 0.1, 0.5),

    (0.15, 0.15, 0.70),
    (0.15, 0.25, 0.60),
    (0.25, 0.15, 0.60),

    (0.10, 0.20, 0.70),
    (0.20, 0.10, 0.70),
    (0.20, 0.20, 0.60)
]


# Remove duplicates
weight_combinations = list(
    dict.fromkeys(weight_combinations)
)


# ============================================================
# VALIDATION WEIGHT SEARCH
# ============================================================

print("\n" + "=" * 60)
print("SEARCHING FOR BEST WEIGHTS")
print("=" * 60)

validation_results = []

best_accuracy = -1
best_weights = None


for w1, w2, w3 in weight_combinations:

    combined_probabilities = (
        w1 * validation_probabilities["cnn1"]
        + w2 * validation_probabilities["cnn2"]
        + w3 * validation_probabilities["cnn3"]
    )

    predictions = np.argmax(
        combined_probabilities,
        axis=1
    )

    accuracy = accuracy_score(
        y_val,
        predictions
    )

    validation_results.append(
        {
            "cnn1_weight": w1,
            "cnn2_weight": w2,
            "cnn3_weight": w3,
            "validation_accuracy": accuracy
        }
    )

    print(
        f"CNN1={w1:.2f}, "
        f"CNN2={w2:.2f}, "
        f"CNN3={w3:.2f} "
        f"→ Validation Accuracy: "
        f"{accuracy * 100:.2f}%"
    )

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_weights = (
            w1,
            w2,
            w3
        )


# ============================================================
# BEST WEIGHTS
# ============================================================

w1, w2, w3 = best_weights

print("\n" + "=" * 60)
print("BEST WEIGHT COMBINATION")
print("=" * 60)

print(
    f"CNN 1 Weight : {w1:.2f}"
)

print(
    f"CNN 2 Weight : {w2:.2f}"
)

print(
    f"CNN 3 Weight : {w3:.2f}"
)

print(
    f"Validation Accuracy : "
    f"{best_accuracy * 100:.2f}%"
)


# ============================================================
# FINAL TEST EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("EVALUATING BEST WEIGHTS ON TEST SET")
print("=" * 60)

final_probabilities = (
    w1 * test_probabilities["cnn1"]
    + w2 * test_probabilities["cnn2"]
    + w3 * test_probabilities["cnn3"]
)

final_predictions = np.argmax(
    final_probabilities,
    axis=1
)


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    final_predictions
)

precision = precision_score(
    y_test,
    final_predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    final_predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    final_predictions,
    average="weighted",
    zero_division=0
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("WEIGHTED SOFT VOTING RESULTS")
print("=" * 60)

print(
    f"Accuracy  : {accuracy:.4f} "
    f"({accuracy * 100:.2f}%)"
)

print(
    f"Precision : {precision:.4f} "
    f"({precision * 100:.2f}%)"
)

print(
    f"Recall    : {recall:.4f} "
    f"({recall * 100:.2f}%)"
)

print(
    f"F1-score  : {f1:.4f} "
    f"({f1 * 100:.2f}%)"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

report = classification_report(
    y_test,
    final_predictions,
    target_names=CLASS_NAMES,
    zero_division=0
)

print(report)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    final_predictions
)

plt.figure(
    figsize=(10, 8)
)

plt.imshow(
    cm,
    interpolation="nearest"
)

plt.title(
    "Weighted Soft Voting - Confusion Matrix"
)

plt.colorbar()

tick_marks = np.arange(
    len(CLASS_NAMES)
)

plt.xticks(
    tick_marks,
    CLASS_NAMES,
    rotation=45,
    ha="right"
)

plt.yticks(
    tick_marks,
    CLASS_NAMES
)

for i in range(
    len(CLASS_NAMES)
):

    for j in range(
        len(CLASS_NAMES)
    ):

        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )

plt.xlabel(
    "Predicted Label"
)

plt.ylabel(
    "True Label"
)

plt.tight_layout()


confusion_path = os.path.join(
    RESULTS_DIR,
    "confusion_matrix_weighted_voting.png"
)

plt.savefig(
    confusion_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print(
    f"\nConfusion matrix saved to:\n"
    f"{confusion_path}"
)


# ============================================================
# SAVE WEIGHT SEARCH RESULTS
# ============================================================

weights_path = os.path.join(
    RESULTS_DIR,
    "weight_search_results.txt"
)

with open(
    weights_path,
    "w"
) as file:

    file.write(
        "WEIGHTED SOFT VOTING SEARCH\n"
    )

    file.write(
        "=" * 60 + "\n\n"
    )

    for result in validation_results:

        file.write(
            f"CNN1={result['cnn1_weight']:.2f}, "
            f"CNN2={result['cnn2_weight']:.2f}, "
            f"CNN3={result['cnn3_weight']:.2f} "
            f"-> Validation Accuracy="
            f"{result['validation_accuracy'] * 100:.2f}%\n"
        )

    file.write(
        "\nBEST WEIGHTS\n"
    )

    file.write(
        f"CNN1={w1:.2f}\n"
    )

    file.write(
        f"CNN2={w2:.2f}\n"
    )

    file.write(
        f"CNN3={w3:.2f}\n"
    )

    file.write(
        f"Validation Accuracy="
        f"{best_accuracy * 100:.2f}%\n"
    )


# ============================================================
# SAVE FINAL METRICS
# ============================================================

metrics_path = os.path.join(
    RESULTS_DIR,
    "weighted_ensemble_metrics.txt"
)

with open(
    metrics_path,
    "w"
) as file:

    file.write(
        "WEIGHTED SOFT VOTING RESULTS\n"
    )

    file.write(
        "=" * 60 + "\n\n"
    )

    file.write(
        f"CNN 1 Weight : {w1:.2f}\n"
    )

    file.write(
        f"CNN 2 Weight : {w2:.2f}\n"
    )

    file.write(
        f"CNN 3 Weight : {w3:.2f}\n\n"
    )

    file.write(
        f"Validation Accuracy : "
        f"{best_accuracy:.4f}\n"
    )

    file.write(
        f"Test Accuracy : "
        f"{accuracy:.4f}\n"
    )

    file.write(
        f"Test Precision : "
        f"{precision:.4f}\n"
    )

    file.write(
        f"Test Recall : "
        f"{recall:.4f}\n"
    )

    file.write(
        f"Test F1-score : "
        f"{f1:.4f}\n"
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("WEIGHTED SOFT VOTING COMPLETED")
print("=" * 60)

print(
    f"Best weights: "
    f"CNN1={w1:.2f}, "
    f"CNN2={w2:.2f}, "
    f"CNN3={w3:.2f}"
)

print(
    f"Validation Accuracy : "
    f"{best_accuracy * 100:.2f}%"
)

print(
    f"Test Accuracy       : "
    f"{accuracy * 100:.2f}%"
)

print(
    f"Test Precision      : "
    f"{precision * 100:.2f}%"
)

print(
    f"Test Recall         : "
    f"{recall * 100:.2f}%"
)

print(
    f"Test F1-score       : "
    f"{f1 * 100:.2f}%"
)

print(
    f"\nResults saved to:\n"
    f"{metrics_path}"
)