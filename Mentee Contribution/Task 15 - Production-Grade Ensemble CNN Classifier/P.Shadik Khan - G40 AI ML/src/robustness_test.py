from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score

from src.data_loader import load_datasets, optimize_dataset


BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
MODELS_DIR = BASE_DIR / "models"


IMG_SIZE = (224, 224)


def load_models():
    """Load all trained CNN models."""

    model_paths = {
        "baseline_cnn": MODELS_DIR / "baseline_cnn.keras",
        "deep_cnn": MODELS_DIR / "deep_cnn.keras",
        "regularized_cnn": MODELS_DIR / "regularized_cnn.keras",
    }

    models = {}

    print("\n" + "=" * 70)
    print("LOADING TRAINED MODELS")
    print("=" * 70)

    for name, path in model_paths.items():

        if not path.exists():
            raise FileNotFoundError(
                f"Model not found: {path}"
            )

        print(f"Loading {name}...")
        models[name] = tf.keras.models.load_model(path)

    print(f"\nSuccessfully loaded {len(models)} models.")

    return models


def collect_test_data(test_ds):
    """Convert TensorFlow dataset into NumPy arrays."""

    images = []
    labels = []

    for batch_images, batch_labels in test_ds:
        images.append(batch_images.numpy())
        labels.append(batch_labels.numpy())

    images = np.concatenate(images, axis=0)
    labels = np.concatenate(labels, axis=0)

    return images, labels


def add_gaussian_noise(images, noise_level):
    """Add Gaussian noise to images."""

    images = images.astype(np.float32)

    noise = np.random.normal(
        loc=0.0,
        scale=noise_level,
        size=images.shape,
    )

    noisy_images = images + noise

    return np.clip(noisy_images, 0, 255)


def change_brightness(images, factor):
    """Change image brightness."""

    images = images.astype(np.float32)

    adjusted = images * factor

    return np.clip(adjusted, 0, 255)


def horizontal_flip(images):
    """Flip images horizontally."""

    return np.flip(images, axis=2)


def ensemble_predict(models, images):
    """Generate ensemble predictions."""

    predictions = []

    for name, model in models.items():

        print(f"Predicting with {name}...")

        pred = model.predict(
            images,
            batch_size=32,
            verbose=0,
        )

        pred = pred.reshape(-1)

        predictions.append(pred)

    predictions = np.array(predictions)

    ensemble_probability = np.mean(
        predictions,
        axis=0,
    )

    ensemble_prediction = (
        ensemble_probability >= 0.5
    ).astype(int)

    return ensemble_prediction


def evaluate_condition(
    models,
    images,
    labels,
    condition_name,
):
    """Evaluate ensemble under a specific image condition."""

    print(f"\nTesting condition: {condition_name}")

    predictions = ensemble_predict(
        models,
        images,
    )

    accuracy = accuracy_score(
        labels,
        predictions,
    )

    print(f"Accuracy: {accuracy:.4f}")

    return accuracy


def main():

    print("=" * 70)
    print("TASK 15 - ROBUSTNESS TESTING")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------

    print("\nLoading test dataset...")

    _, _, test_ds = load_datasets()

    test_ds = optimize_dataset(test_ds)

    images, labels = collect_test_data(test_ds)

    print(f"Test images: {len(images)}")
    print(f"Image shape: {images.shape}")
    print(f"Labels: {len(labels)}")

    # ---------------------------------------------------------
    # Load models
    # ---------------------------------------------------------

    models = load_models()

    # ---------------------------------------------------------
    # Baseline
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("BASELINE PERFORMANCE")
    print("=" * 70)

    baseline_accuracy = evaluate_condition(
        models,
        images,
        labels,
        "Original images",
    )

    # ---------------------------------------------------------
    # Gaussian noise
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("NOISE ROBUSTNESS")
    print("=" * 70)

    noise_levels = [
        5,
        10,
        20,
    ]

    noise_results = []

    for noise_level in noise_levels:

        noisy_images = add_gaussian_noise(
            images,
            noise_level,
        )

        accuracy = evaluate_condition(
            models,
            noisy_images,
            labels,
            f"Gaussian noise - {noise_level}",
        )

        noise_results.append(
            {
                "condition": f"gaussian_noise_{noise_level}",
                "accuracy": accuracy,
            }
        )

    # ---------------------------------------------------------
    # Brightness robustness
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("BRIGHTNESS ROBUSTNESS")
    print("=" * 70)

    brightness_levels = [
        0.7,
        1.3,
    ]

    brightness_results = []

    for factor in brightness_levels:

        adjusted_images = change_brightness(
            images,
            factor,
        )

        accuracy = evaluate_condition(
            models,
            adjusted_images,
            labels,
            f"Brightness factor - {factor}",
        )

        brightness_results.append(
            {
                "condition": f"brightness_{factor}",
                "accuracy": accuracy,
            }
        )

    # ---------------------------------------------------------
    # Horizontal flip
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("HORIZONTAL FLIP ROBUSTNESS")
    print("=" * 70)

    flipped_images = horizontal_flip(images)

    flip_accuracy = evaluate_condition(
        models,
        flipped_images,
        labels,
        "Horizontal flip",
    )

    # ---------------------------------------------------------
    # Combine results
    # ---------------------------------------------------------

    results = [
        {
            "condition": "original",
            "accuracy": baseline_accuracy,
        }
    ]

    results.extend(noise_results)
    results.extend(brightness_results)

    results.append(
        {
            "condition": "horizontal_flip",
            "accuracy": flip_accuracy,
        }
    )

    results_df = pd.DataFrame(results)

    # ---------------------------------------------------------
    # Save results
    # ---------------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        RESULTS_DIR / "robustness_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False,
    )

    # ---------------------------------------------------------
    # Display final results
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("ROBUSTNESS TEST RESULTS")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    print("\nResults saved to:")
    print(output_file)

    print("\n" + "=" * 70)
    print("ROBUSTNESS TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()