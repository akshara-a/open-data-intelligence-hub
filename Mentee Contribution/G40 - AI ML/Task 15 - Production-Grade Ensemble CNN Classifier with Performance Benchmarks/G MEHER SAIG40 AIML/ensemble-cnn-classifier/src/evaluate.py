import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

from data_loader import load_cifar10


# ============================================================
# CONFIGURATION
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
# MODEL CONFIGURATION
# ============================================================

MODEL_CONFIG = {

    "cnn1": {
        "model_file": "cnn_baseline.keras",
        "history_file": "cnn1_history.npy",
        "display_name": "CNN 1 - Baseline"
    },

    "cnn2": {
        "model_file": "cnn_regularized.keras",
        "history_file": "cnn2_history.npy",
        "display_name": "CNN 2 - Regularized"
    },

    "cnn3": {
        "model_file": "cnn_deep.keras",
        "history_file": "cnn3_history.npy",
        "display_name": "CNN 3 - Deep"
    }
}


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
# GET MODEL NAME
# ============================================================

if len(sys.argv) < 2:

    print("\nUsage:")
    print("  python evaluate.py cnn1")
    print("  python evaluate.py cnn2")
    print("  python evaluate.py cnn3")

    sys.exit(1)


MODEL_NAME = sys.argv[1].lower()


if MODEL_NAME not in MODEL_CONFIG:

    print(
        f"\nInvalid model: {MODEL_NAME}"
    )

    print("\nAvailable models:")

    for name in MODEL_CONFIG:
        print(f"  - {name}")

    sys.exit(1)


config = MODEL_CONFIG[MODEL_NAME]

MODEL_PATH = os.path.join(
    MODEL_DIR,
    config["model_file"]
)

HISTORY_PATH = os.path.join(
    RESULTS_DIR,
    config["history_file"]
)

DISPLAY_NAME = config["display_name"]


# ============================================================
# OUTPUT FILE PREFIX
# ============================================================

PREFIX = MODEL_NAME


# ============================================================
# START
# ============================================================

print("\n" + "=" * 60)
print(f"EVALUATING {DISPLAY_NAME}")
print("=" * 60)


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"\nModel not found:\n{MODEL_PATH}"
    )

if not os.path.exists(HISTORY_PATH):

    raise FileNotFoundError(
        f"\nTraining history not found:\n{HISTORY_PATH}"
    )


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading dataset...")

(
    x_train,
    y_train,
    x_val,
    y_val,
    x_test,
    y_test
) = load_cifar10()


# ============================================================
# LOAD MODEL
# ============================================================

print(
    f"\nLoading model:\n{MODEL_PATH}"
)

model = tf.keras.models.load_model(
    MODEL_PATH
)

print(
    f"{DISPLAY_NAME} loaded successfully!"
)


# ============================================================
# MODEL INFORMATION
# ============================================================

total_params = model.count_params()

trainable_params = np.sum(
    [
        np.prod(variable.shape)
        for variable in model.trainable_variables
    ]
)

non_trainable_params = (
    total_params - trainable_params
)


print("\nModel Information:")
print(
    f"Total parameters      : {total_params:,}"
)

print(
    f"Trainable parameters   : {trainable_params:,}"
)

print(
    f"Non-trainable params   : {non_trainable_params:,}"
)


# ============================================================
# PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

probabilities = model.predict(
    x_test,
    batch_size=32,
    verbose=1
)

y_pred = np.argmax(
    probabilities,
    axis=1
)


# ============================================================
# METRICS
# ============================================================

accuracy = np.mean(
    y_pred == y_test
)

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


# ============================================================
# DISPLAY METRICS
# ============================================================

print("\n" + "=" * 60)
print(f"{DISPLAY_NAME.upper()} RESULTS")
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
    y_pred,
    target_names=CLASS_NAMES,
    zero_division=0
)

print(report)


report_path = os.path.join(
    RESULTS_DIR,
    f"{PREFIX}_classification_report.txt"
)

with open(
    report_path,
    "w"
) as file:

    file.write(
        f"{DISPLAY_NAME} Classification Report\n"
    )

    file.write("=" * 60 + "\n\n")

    file.write(report)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\nGenerating confusion matrix...")

cm = confusion_matrix(
    y_test,
    y_pred
)

plt.figure(
    figsize=(10, 8)
)

plt.imshow(
    cm,
    interpolation="nearest"
)

plt.title(
    f"{DISPLAY_NAME} - Confusion Matrix"
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


plt.ylabel(
    "True Label"
)

plt.xlabel(
    "Predicted Label"
)

plt.tight_layout()


confusion_path = os.path.join(
    RESULTS_DIR,
    f"confusion_matrix_{PREFIX}.png"
)

plt.savefig(
    confusion_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print(
    f"Confusion matrix saved to:\n"
    f"{confusion_path}"
)


# ============================================================
# LOAD TRAINING HISTORY
# ============================================================

history = np.load(
    HISTORY_PATH,
    allow_pickle=True
).item()


# ============================================================
# ACCURACY GRAPH
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history["val_accuracy"],
    label="Validation Accuracy"
)

plt.title(
    f"{DISPLAY_NAME} - Training vs Validation Accuracy"
)

plt.xlabel(
    "Epoch"
)

plt.ylabel(
    "Accuracy"
)

plt.legend()

plt.grid(
    True
)

plt.tight_layout()


accuracy_graph_path = os.path.join(
    RESULTS_DIR,
    f"{PREFIX}_accuracy.png"
)

plt.savefig(
    accuracy_graph_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print(
    f"Accuracy graph saved to:\n"
    f"{accuracy_graph_path}"
)


# ============================================================
# LOSS GRAPH
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    history["loss"],
    label="Training Loss"
)

plt.plot(
    history["val_loss"],
    label="Validation Loss"
)

plt.title(
    f"{DISPLAY_NAME} - Training vs Validation Loss"
)

plt.xlabel(
    "Epoch"
)

plt.ylabel(
    "Loss"
)

plt.legend()

plt.grid(
    True
)

plt.tight_layout()


loss_graph_path = os.path.join(
    RESULTS_DIR,
    f"{PREFIX}_loss.png"
)

plt.savefig(
    loss_graph_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print(
    f"Loss graph saved to:\n"
    f"{loss_graph_path}"
)


# ============================================================
# SAVE METRICS
# ============================================================

metrics_path = os.path.join(
    RESULTS_DIR,
    f"{PREFIX}_metrics.txt"
)

with open(
    metrics_path,
    "w"
) as file:

    file.write(
        f"{DISPLAY_NAME} Evaluation Results\n"
    )

    file.write("=" * 60 + "\n\n")

    file.write(
        f"Accuracy  : {accuracy:.4f}\n"
    )

    file.write(
        f"Precision : {precision:.4f}\n"
    )

    file.write(
        f"Recall    : {recall:.4f}\n"
    )

    file.write(
        f"F1-score  : {f1:.4f}\n"
    )

    file.write(
        f"Total Parameters : {total_params:,}\n"
    )

    file.write(
        f"Trainable Parameters : {trainable_params:,}\n"
    )

    file.write(
        f"Non-trainable Parameters : "
        f"{non_trainable_params:,}\n"
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print(
    f"{DISPLAY_NAME.upper()} "
    "EVALUATION COMPLETED SUCCESSFULLY"
)
print("=" * 60)

print(
    f"Accuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1-score  : {f1 * 100:.2f}%"
)

print(
    f"Parameters: {total_params:,}"
)

print("\nGenerated files:")

print(
    f"1. {confusion_path}"
)

print(
    f"2. {accuracy_graph_path}"
)

print(
    f"3. {loss_graph_path}"
)

print(
    f"4. {metrics_path}"
)

print(
    f"5. {report_path}"
)