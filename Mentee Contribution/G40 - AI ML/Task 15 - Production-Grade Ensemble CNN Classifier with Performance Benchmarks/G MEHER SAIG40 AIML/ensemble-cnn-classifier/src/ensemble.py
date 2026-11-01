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

from data_loader import load_cifar10


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
# LOAD DATA
# ============================================================

print("\n" + "=" * 60)
print("LOADING TEST DATA")
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
print("LOADING CNN MODELS")
print("=" * 60)

models = {}

for name, path in MODEL_PATHS.items():

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Model not found:\n{path}"
        )

    print(f"\nLoading {name.upper()}...")

    models[name] = tf.keras.models.load_model(
        path
    )

    print(
        f"{name.upper()} loaded successfully."
    )


# ============================================================
# GENERATE PROBABILITY PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("GENERATING MODEL PREDICTIONS")
print("=" * 60)

probabilities = {}

predictions = {}

for name, model in models.items():

    print(
        f"\nPredicting with {name.upper()}..."
    )

    probs = model.predict(
        x_test,
        batch_size=32,
        verbose=1
    )

    probabilities[name] = probs

    predictions[name] = np.argmax(
        probs,
        axis=1
    )


# ============================================================
# HARD / MAJORITY VOTING
# ============================================================

print("\n" + "=" * 60)
print("HARD / MAJORITY VOTING")
print("=" * 60)

prediction_matrix = np.column_stack(
    [
        predictions["cnn1"],
        predictions["cnn2"],
        predictions["cnn3"]
    ]
)


hard_predictions = []


for row in prediction_matrix:

    counts = np.bincount(
        row,
        minlength=len(CLASS_NAMES)
    )

    majority_class = np.argmax(
        counts
    )

    hard_predictions.append(
        majority_class
    )


hard_predictions = np.array(
    hard_predictions
)


# ============================================================
# SOFT VOTING
# ============================================================

print("\n" + "=" * 60)
print("SOFT VOTING")
print("=" * 60)


soft_probabilities = (
    probabilities["cnn1"]
    + probabilities["cnn2"]
    + probabilities["cnn3"]
) / 3.0


soft_predictions = np.argmax(
    soft_probabilities,
    axis=1
)


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate_ensemble(
    name,
    y_true,
    y_pred
):

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

    print("\n" + "=" * 60)
    print(name.upper())
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

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            y_pred,
            target_names=CLASS_NAMES,
            zero_division=0
        )
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# ============================================================
# EVALUATE HARD VOTING
# ============================================================

hard_metrics = evaluate_ensemble(
    "Hard Voting Ensemble",
    y_test,
    hard_predictions
)


# ============================================================
# EVALUATE SOFT VOTING
# ============================================================

soft_metrics = evaluate_ensemble(
    "Soft Voting Ensemble",
    y_test,
    soft_predictions
)


# ============================================================
# CONFUSION MATRICES
# ============================================================

def save_confusion_matrix(
    name,
    y_true,
    y_pred,
    filename
):

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    import matplotlib.pyplot as plt

    plt.figure(
        figsize=(10, 8)
    )

    plt.imshow(
        cm,
        interpolation="nearest"
    )

    plt.title(
        name
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

    output_path = os.path.join(
        RESULTS_DIR,
        filename
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_path}"
    )


save_confusion_matrix(
    "Hard Voting Ensemble - Confusion Matrix",
    y_test,
    hard_predictions,
    "confusion_matrix_hard_voting.png"
)


save_confusion_matrix(
    "Soft Voting Ensemble - Confusion Matrix",
    y_test,
    soft_predictions,
    "confusion_matrix_soft_voting.png"
)


# ============================================================
# SAVE ENSEMBLE METRICS
# ============================================================

metrics_path = os.path.join(
    RESULTS_DIR,
    "ensemble_metrics.txt"
)

with open(
    metrics_path,
    "w"
) as file:

    file.write(
        "ENSEMBLE EVALUATION RESULTS\n"
    )

    file.write(
        "=" * 60 + "\n\n"
    )

    file.write(
        "Hard Voting\n"
    )

    file.write(
        f"Accuracy  : "
        f"{hard_metrics['accuracy']:.4f}\n"
    )

    file.write(
        f"Precision : "
        f"{hard_metrics['precision']:.4f}\n"
    )

    file.write(
        f"Recall    : "
        f"{hard_metrics['recall']:.4f}\n"
    )

    file.write(
        f"F1-score  : "
        f"{hard_metrics['f1']:.4f}\n\n"
    )

    file.write(
        "Soft Voting\n"
    )

    file.write(
        f"Accuracy  : "
        f"{soft_metrics['accuracy']:.4f}\n"
    )

    file.write(
        f"Precision : "
        f"{soft_metrics['precision']:.4f}\n"
    )

    file.write(
        f"Recall    : "
        f"{soft_metrics['recall']:.4f}\n"
    )

    file.write(
        f"F1-score  : "
        f"{soft_metrics['f1']:.4f}\n"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ENSEMBLE EVALUATION COMPLETED")
print("=" * 60)

print(
    f"Hard Voting Accuracy : "
    f"{hard_metrics['accuracy'] * 100:.2f}%"
)

print(
    f"Soft Voting Accuracy : "
    f"{soft_metrics['accuracy'] * 100:.2f}%"
)

print(
    f"\nResults saved to:"
)

print(
    metrics_path
)