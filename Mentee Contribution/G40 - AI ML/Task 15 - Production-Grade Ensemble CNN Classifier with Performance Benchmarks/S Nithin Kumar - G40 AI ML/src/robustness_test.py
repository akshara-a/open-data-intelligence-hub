import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import accuracy_score

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_prepare_data


MODEL_DIR = "models"
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# ADD GAUSSIAN NOISE
# ============================================================

def add_noise(images, noise_factor=0.1):

    noise = np.random.normal(
        loc=0.0,
        scale=noise_factor,
        size=images.shape
    )

    noisy_images = images + noise

    return np.clip(
        noisy_images,
        0.0,
        1.0
    )


# ============================================================
# DARKEN IMAGES
# ============================================================

def darken_images(images, factor=0.5):

    dark_images = images * factor

    return np.clip(
        dark_images,
        0.0,
        1.0
    )


# ============================================================
# BRIGHTEN IMAGES
# ============================================================

def brighten_images(images, factor=1.5):

    bright_images = images * factor

    return np.clip(
        bright_images,
        0.0,
        1.0
    )


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_condition(model, images, labels):

    predictions = model.predict(
        images,
        verbose=0
    )

    predicted_classes = np.argmax(
        predictions,
        axis=1
    )

    accuracy = accuracy_score(
        labels,
        predicted_classes
    )

    return accuracy


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading dataset...")

    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        class_names
    ) = load_and_prepare_data()

    # Use 2,000 images for faster testing
    X_sample = X_test[:2000]
    y_sample = y_test[:2000]

    print("\nLoading Deep CNN...")

    model = tf.keras.models.load_model(
        os.path.join(
            MODEL_DIR,
            "deep_cnn.keras"
        )
    )

    print("\nCreating image conditions...")

    original_images = X_sample

    noisy_images = add_noise(
        X_sample,
        noise_factor=0.1
    )

    dark_images = darken_images(
        X_sample,
        factor=0.5
    )

    bright_images = brighten_images(
        X_sample,
        factor=1.5
    )

    conditions = {
        "Original": original_images,
        "Noisy": noisy_images,
        "Dark": dark_images,
        "Bright": bright_images
    }

    results = []

    print("\n" + "=" * 70)
    print("ROBUSTNESS TEST RESULTS")
    print("=" * 70)

    for condition_name, images in conditions.items():

        print(f"\nTesting: {condition_name}")

        accuracy = evaluate_condition(
            model,
            images,
            y_sample
        )

        print(
            f"Accuracy: {accuracy:.4f}"
        )

        results.append({
            "Condition": condition_name,
            "Accuracy": accuracy
        })

    # Save results
    results_df = pd.DataFrame(results)

    output_path = os.path.join(
        RESULTS_DIR,
        "robustness_results.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 70)
    print("FINAL ROBUSTNESS COMPARISON")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    print("\nResults saved to:")
    print(output_path)


if __name__ == "__main__":
    main()