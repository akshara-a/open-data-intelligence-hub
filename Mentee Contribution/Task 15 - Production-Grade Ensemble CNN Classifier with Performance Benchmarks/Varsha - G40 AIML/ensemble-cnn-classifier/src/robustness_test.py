import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

from src.data_loader import load_small_cifar10


MODEL_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)


# --------------------------------------------------
# LOAD TEST DATA
# --------------------------------------------------

print("=" * 60)
print("ROBUSTNESS TESTING")
print("=" * 60)

print("\nLoading test dataset...")

data = load_small_cifar10()

X_test = data[4].astype("float32") / 255.0
y_test = data[5].reshape(-1)

print("Test images:", X_test.shape)


# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

model_paths = {
    "CNN1_Baseline": os.path.join(
        MODEL_DIR,
        "cnn_baseline.keras"
    ),

    "CNN2_Regularized": os.path.join(
        MODEL_DIR,
        "cnn_regularized.keras"
    ),

    "CNN3_Deep": os.path.join(
        MODEL_DIR,
        "cnn_deep.keras"
    )
}


models = {}

print("\nLoading models...")

for name, path in model_paths.items():

    if not os.path.exists(path):

        print("Model not found:", path)
        continue

    models[name] = tf.keras.models.load_model(path)

    print("Loaded:", name)


# --------------------------------------------------
# IMAGE TRANSFORMATIONS
# --------------------------------------------------

def add_noise(images):

    rng = np.random.default_rng(42)

    noise = rng.normal(
        0,
        0.08,
        images.shape
    ).astype("float32")

    return np.clip(
        images + noise,
        0,
        1
    )


def darken(images):

    return np.clip(
        images * 0.55,
        0,
        1
    )


def brighten(images):

    return np.clip(
        images * 1.30,
        0,
        1
    )


def blur(images):

    output = []

    for image in images:

        # Simple average blur without extra packages
        padded = np.pad(
            image,
            ((1, 1), (1, 1), (0, 0)),
            mode="edge"
        )

        blurred = np.zeros_like(image)

        for i in range(32):
            for j in range(32):

                region = padded[
                    i:i + 3,
                    j:j + 3
                ]

                blurred[i, j] = np.mean(
                    region,
                    axis=(0, 1)
                )

        output.append(blurred)

    return np.array(
        output,
        dtype="float32"
    )


def rotate(images):

    output = []

    for image in images:

        # Rotate approximately 15 degrees
        h, w = image.shape[:2]

        center = (
            w // 2,
            h // 2
        )

        # Manual lightweight rotation using TensorFlow
        rotated = tf.image.rot90(
            image,
            k=1
        )

        output.append(
            rotated.numpy()
        )

    return np.array(
        output,
        dtype="float32"
    )


# --------------------------------------------------
# CREATE ROBUSTNESS DATASETS
# --------------------------------------------------

print("\nCreating modified test images...")

# Use 50 images to keep the laptop workload small
X = X_test[:50]
Y = y_test[:50]

test_conditions = {

    "Original": X,

    "Noisy": add_noise(X),

    "Darkened": darken(X),

    "Brightened": brighten(X),

    "Blurred": blur(X),

    "Rotated": rotate(X)
}


# --------------------------------------------------
# TEST INDIVIDUAL MODELS
# --------------------------------------------------

results = []

for condition, images in test_conditions.items():

    print("\n" + "=" * 60)

    print(
        "Testing condition:",
        condition
    )

    print("=" * 60)

    all_probabilities = []

    for model_name, model in models.items():

        probabilities = model.predict(
            images,
            verbose=0
        )

        predictions = np.argmax(
            probabilities,
            axis=1
        )

        accuracy = accuracy_score(
            Y,
            predictions
        )

        print(
            f"{model_name}: "
            f"{accuracy:.4f}"
        )

        results.append({

            "Condition": condition,

            "Model": model_name,

            "Accuracy": accuracy

        })

        all_probabilities.append(
            probabilities
        )


    # --------------------------------------------------
    # SOFT VOTING ENSEMBLE
    # --------------------------------------------------

    if len(all_probabilities) > 0:

        average_probability = np.mean(
            all_probabilities,
            axis=0
        )

        ensemble_prediction = np.argmax(
            average_probability,
            axis=1
        )

        ensemble_accuracy = accuracy_score(
            Y,
            ensemble_prediction
        )

        print(
            f"Soft Voting Ensemble: "
            f"{ensemble_accuracy:.4f}"
        )

        results.append({

            "Condition": condition,

            "Model": "Soft_Voting_Ensemble",

            "Accuracy": ensemble_accuracy

        })


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(
    results
)

csv_path = os.path.join(
    RESULTS_DIR,
    "robustness_results.csv"
)

results_df.to_csv(
    csv_path,
    index=False
)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\n")
print("=" * 60)
print("ROBUSTNESS TEST RESULTS")
print("=" * 60)

print(
    results_df.to_string(
        index=False
    )
)

print("\nResults saved to:")

print(csv_path)

print("\n")
print("=" * 60)
print("ROBUSTNESS TESTING COMPLETED")
print("=" * 60)