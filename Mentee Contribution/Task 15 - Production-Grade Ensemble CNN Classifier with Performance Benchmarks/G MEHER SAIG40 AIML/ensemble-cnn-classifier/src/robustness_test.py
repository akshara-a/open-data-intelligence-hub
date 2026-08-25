import os
import numpy as np
import tensorflow as tf

from sklearn.metrics import accuracy_score

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
# MODEL PATHS
# ============================================================

MODEL_PATHS = {

    "CNN 1": os.path.join(
        MODEL_DIR,
        "cnn_baseline.keras"
    ),

    "CNN 2": os.path.join(
        MODEL_DIR,
        "cnn_regularized.keras"
    ),

    "CNN 3": os.path.join(
        MODEL_DIR,
        "cnn_deep.keras"
    )
}


# ============================================================
# WEIGHTED ENSEMBLE WEIGHTS
# ============================================================

WEIGHTS = {
    "CNN 1": 0.20,
    "CNN 2": 0.10,
    "CNN 3": 0.70
}


# ============================================================
# LOAD DATASET
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
print("LOADING MODELS")
print("=" * 60)

models = {}

for name, path in MODEL_PATHS.items():

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Model not found:\n{path}"
        )

    print(
        f"Loading {name}..."
    )

    models[name] = tf.keras.models.load_model(
        path
    )

    print(
        f"{name} loaded successfully."
    )


# ============================================================
# ROBUSTNESS FUNCTIONS
# ============================================================

def add_gaussian_noise(
    images,
    noise_std=0.10
):

    noise = np.random.normal(
        loc=0.0,
        scale=noise_std,
        size=images.shape
    )

    noisy_images = images + noise

    return np.clip(
        noisy_images,
        0.0,
        1.0
    ).astype(
        np.float32
    )


def reduce_brightness(
    images,
    factor=0.60
):

    dark_images = images * factor

    return np.clip(
        dark_images,
        0.0,
        1.0
    ).astype(
        np.float32
    )


def apply_blur(
    images,
    filter_size=5
):

    images_tensor = tf.convert_to_tensor(
        images,
        dtype=tf.float32
    )

    blurred_images = tf.nn.avg_pool2d(
        images_tensor,
        ksize=filter_size,
        strides=1,
        padding="SAME"
    )

    return blurred_images.numpy()


# ============================================================
# CREATE DEGRADATION DATASETS
# ============================================================

np.random.seed(42)

datasets = {

    "Clean": x_test,

    "Gaussian Noise": add_gaussian_noise(
        x_test,
        noise_std=0.10
    ),

    "Brightness Reduction": reduce_brightness(
        x_test,
        factor=0.60
    ),

    "Blur": apply_blur(
        x_test,
        filter_size=5
    )
}


# ============================================================
# EVALUATION
# ============================================================

results = {}


for condition, images in datasets.items():

    print("\n" + "=" * 60)
    print(
        f"TESTING CONDITION: {condition}"
    )
    print("=" * 60)

    model_probabilities = {}

    condition_results = {}


    # --------------------------------------------------------
    # Individual CNNs
    # --------------------------------------------------------

    for name, model in models.items():

        print(
            f"\nPredicting with {name}..."
        )

        probabilities = model.predict(
            images,
            batch_size=32,
            verbose=1
        )

        predictions = np.argmax(
            probabilities,
            axis=1
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        model_probabilities[name] = probabilities

        condition_results[name] = accuracy

        print(
            f"{name} Accuracy: "
            f"{accuracy * 100:.2f}%"
        )


    # --------------------------------------------------------
    # Weighted Ensemble
    # --------------------------------------------------------

    ensemble_probabilities = (

        WEIGHTS["CNN 1"]
        * model_probabilities["CNN 1"]

        +

        WEIGHTS["CNN 2"]
        * model_probabilities["CNN 2"]

        +

        WEIGHTS["CNN 3"]
        * model_probabilities["CNN 3"]
    )

    ensemble_predictions = np.argmax(
        ensemble_probabilities,
        axis=1
    )

    ensemble_accuracy = accuracy_score(
        y_test,
        ensemble_predictions
    )

    condition_results[
        "Weighted Ensemble"
    ] = ensemble_accuracy

    print(
        f"\nWeighted Ensemble Accuracy: "
        f"{ensemble_accuracy * 100:.2f}%"
    )

    results[
        condition
    ] = condition_results


# ============================================================
# DISPLAY SUMMARY
# ============================================================

print("\n\n" + "=" * 80)
print("ROBUSTNESS TEST RESULTS")
print("=" * 80)

header = (
    f"{'Condition':<25}"
    f"{'CNN 1':>12}"
    f"{'CNN 2':>12}"
    f"{'CNN 3':>12}"
    f"{'Weighted Ensemble':>20}"
)

print(header)

print("-" * 80)

for condition, values in results.items():

    print(
        f"{condition:<25}"
        f"{values['CNN 1'] * 100:>11.2f}%"
        f"{values['CNN 2'] * 100:>11.2f}%"
        f"{values['CNN 3'] * 100:>11.2f}%"
        f"{values['Weighted Ensemble'] * 100:>19.2f}%"
    )


# ============================================================
# CALCULATE ACCURACY DROP
# ============================================================

clean_results = results["Clean"]


print("\n" + "=" * 80)
print("ACCURACY DROP FROM CLEAN TEST DATA")
print("=" * 80)

for condition, values in results.items():

    if condition == "Clean":
        continue

    print(
        f"\n{condition}"
    )

    for model_name in values:

        clean_accuracy = (
            clean_results[model_name]
        )

        degraded_accuracy = (
            values[model_name]
        )

        drop = (
            clean_accuracy
            - degraded_accuracy
        )

        print(
            f"{model_name:<20}"
            f"Drop: {drop * 100:.2f} percentage points"
        )


# ============================================================
# SAVE RESULTS
# ============================================================

results_path = os.path.join(
    RESULTS_DIR,
    "robustness_results.txt"
)

with open(
    results_path,
    "w"
) as file:

    file.write(
        "ROBUSTNESS TEST RESULTS\n"
    )

    file.write(
        "=" * 80 + "\n\n"
    )

    file.write(
        "Weighted Ensemble Weights:\n"
    )

    file.write(
        "CNN 1 = 0.20\n"
    )

    file.write(
        "CNN 2 = 0.10\n"
    )

    file.write(
        "CNN 3 = 0.70\n\n"
    )


    for condition, values in results.items():

        file.write(
            f"{condition}\n"
        )

        file.write(
            "-" * 40 + "\n"
        )

        for model_name, accuracy in values.items():

            file.write(
                f"{model_name}: "
                f"{accuracy * 100:.2f}%\n"
            )

        file.write("\n")


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 60)
print("ROBUSTNESS TESTING COMPLETED")
print("=" * 60)

print(
    f"Results saved to:\n"
    f"{results_path}"
)