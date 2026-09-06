import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import tensorflow as tf

# ---------------------------------------------------------
# Project path setup
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

sys.path.append(CURRENT_DIR)

from data_loader import load_small_cifar10


# ---------------------------------------------------------
# CIFAR-10 class names
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Create results folder
# ---------------------------------------------------------

RESULTS_DIR = os.path.join(PROJECT_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)


# ---------------------------------------------------------
# Load test data
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("LOADING TEST DATA")
print("=" * 60)

data = load_small_cifar10()

X_train = data[0]
y_train = data[1]

X_val = data[2]
y_val = data[3]

X_test = data[4]
y_test = data[5]

print("Training data :", X_train.shape)
print("Validation data:", X_val.shape)
print("Testing data  :", X_test.shape)


# ---------------------------------------------------------
# Safe normalization
# ---------------------------------------------------------
# If the data is already normalized (0-1), don't normalize
# again.
# If it is still 0-255, normalize it once.
# ---------------------------------------------------------

X_test = X_test.astype("float32")

if X_test.max() > 1.0:
    print("\nTest data is 0-255.")
    print("Normalizing test data once...")
    X_test = X_test / 255.0
else:
    print("\nTest data is already normalized.")
    print("No additional normalization applied.")


# ---------------------------------------------------------
# Convert labels to 1D
# ---------------------------------------------------------

y_test = np.asarray(y_test).reshape(-1)


# ---------------------------------------------------------
# Model information
# ---------------------------------------------------------

models_info = {
    "CNN1_Baseline": os.path.join(
        PROJECT_DIR,
        "models",
        "cnn_baseline.keras"
    ),

    "CNN2_Regularized": os.path.join(
        PROJECT_DIR,
        "models",
        "cnn_regularized.keras"
    ),

    "CNN3_Deep": os.path.join(
        PROJECT_DIR,
        "models",
        "cnn_deep.keras"
    )
}


# ---------------------------------------------------------
# Evaluation function
# ---------------------------------------------------------

def evaluate_model(model_name, model_path):

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)

    # Check model exists
    if not os.path.exists(model_path):
        print("ERROR: Model file not found:")
        print(model_path)
        return None

    print("Loading model...")

    model = tf.keras.models.load_model(model_path)

    print("Model loaded successfully.")

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    print("Making predictions...")

    predictions = model.predict(
        X_test,
        batch_size=64,
        verbose=1
    )

    # Convert probabilities to class labels
    y_pred = np.argmax(predictions, axis=1)

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0
    )

    # -----------------------------------------------------
    # Print results
    # -----------------------------------------------------

    print("\nResults:")
    print("-" * 40)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    # -----------------------------------------------------
    # Confusion Matrix
    # -----------------------------------------------------

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    plt.figure(figsize=(9, 9))

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=CLASS_NAMES
    )

    display.plot(
        xticks_rotation=45
    )

    plt.title(f"{model_name} - Confusion Matrix")

    plt.tight_layout()

    confusion_path = os.path.join(
        RESULTS_DIR,
        f"{model_name.lower()}_confusion_matrix.png"
    )

    plt.savefig(
        confusion_path,
        dpi=150
    )

    plt.close()

    print(f"Confusion matrix saved:")
    print(confusion_path)

    # -----------------------------------------------------
    # Return results
    # -----------------------------------------------------

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "predictions": y_pred,
        "probabilities": predictions
    }


# ---------------------------------------------------------
# Evaluate all three CNN models
# ---------------------------------------------------------

all_results = {}

for model_name, model_path in models_info.items():

    result = evaluate_model(
        model_name,
        model_path
    )

    if result is not None:
        all_results[model_name] = result


# ---------------------------------------------------------
# Final summary
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("INDIVIDUAL MODEL RESULTS")
print("=" * 60)

for model_name, result in all_results.items():

    print(f"\n{model_name}")

    print(
        f"Accuracy : {result['accuracy']:.4f}"
    )

    print(
        f"Precision: {result['precision']:.4f}"
    )

    print(
        f"Recall   : {result['recall']:.4f}"
    )

    print(
        f"F1 Score : {result['f1']:.4f}"
    )


# ---------------------------------------------------------
# Save results to CSV
# ---------------------------------------------------------

import pandas as pd

summary_rows = []

for model_name, result in all_results.items():

    summary_rows.append({
        "Model": model_name,
        "Accuracy": result["accuracy"],
        "Precision": result["precision"],
        "Recall": result["recall"],
        "F1_Score": result["f1"]
    })


results_df = pd.DataFrame(summary_rows)

csv_path = os.path.join(
    RESULTS_DIR,
    "individual_model_results.csv"
)

results_df.to_csv(
    csv_path,
    index=False
)

print("\nResults saved to:")
print(csv_path)


# ---------------------------------------------------------
# Completion message
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("INDIVIDUAL EVALUATION COMPLETED SUCCESSFULLY")
print("=" * 60)