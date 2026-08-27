from pathlib import Path
import time

import numpy as np
import pandas as pd
import tensorflow as tf

from src.data_loader import load_datasets, optimize_dataset


BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"


MODEL_NAMES = [
    "baseline_cnn",
    "deep_cnn",
    "regularized_cnn",
]


def load_models():
    """Load all trained CNN models."""

    models = {}

    print("\n" + "=" * 70)
    print("LOADING TRAINED MODELS")
    print("=" * 70)

    for name in MODEL_NAMES:

        model_path = MODELS_DIR / f"{name}.keras"

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        print(f"Loading {name}...")

        models[name] = tf.keras.models.load_model(
            model_path
        )

    print(f"\nSuccessfully loaded {len(models)} models.")

    return models


def collect_test_data(test_ds):
    """Convert test dataset to NumPy arrays."""

    images = []
    labels = []

    for batch_images, batch_labels in test_ds:
        images.append(batch_images.numpy())
        labels.append(batch_labels.numpy())

    images = np.concatenate(images, axis=0)
    labels = np.concatenate(labels, axis=0)

    return images, labels


def benchmark_model(model, images):
    """Measure inference time and prediction throughput."""

    # Warm-up prediction
    model.predict(
        images[:1],
        verbose=0,
    )

    start_time = time.perf_counter()

    predictions = model.predict(
        images,
        batch_size=32,
        verbose=0,
    )

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    samples = len(images)

    throughput = (
        samples / elapsed_time
        if elapsed_time > 0
        else 0
    )

    latency_ms = (
        elapsed_time / samples * 1000
        if samples > 0
        else 0
    )

    return {
        "samples": samples,
        "inference_time_seconds": elapsed_time,
        "latency_ms_per_image": latency_ms,
        "throughput_images_per_second": throughput,
    }


def main():

    print("=" * 70)
    print("TASK 15 - MODEL BENCHMARKING")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load test dataset
    # ---------------------------------------------------------

    print("\nLoading test dataset...")

    _, _, test_ds = load_datasets()

    test_ds = optimize_dataset(test_ds)

    images, labels = collect_test_data(test_ds)

    print(f"Test images: {len(images)}")
    print(f"Image shape: {images.shape}")

    # ---------------------------------------------------------
    # Load models
    # ---------------------------------------------------------

    models = load_models()

    # ---------------------------------------------------------
    # Benchmark models
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("RUNNING INFERENCE BENCHMARK")
    print("=" * 70)

    results = []

    for name, model in models.items():

        print(f"\nBenchmarking {name}...")

        benchmark = benchmark_model(
            model,
            images,
        )

        model_path = MODELS_DIR / f"{name}.keras"

        model_size_mb = (
            model_path.stat().st_size
            / (1024 * 1024)
        )

        results.append(
            {
                "model": name,
                "parameters": model.count_params(),
                "model_size_mb": model_size_mb,
                "samples": benchmark["samples"],
                "inference_time_seconds": benchmark[
                    "inference_time_seconds"
                ],
                "latency_ms_per_image": benchmark[
                    "latency_ms_per_image"
                ],
                "throughput_images_per_second": benchmark[
                    "throughput_images_per_second"
                ],
            }
        )

    # ---------------------------------------------------------
    # Create results DataFrame
    # ---------------------------------------------------------

    results_df = pd.DataFrame(results)

    # ---------------------------------------------------------
    # Save benchmark results
    # ---------------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        RESULTS_DIR / "benchmark_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False,
    )

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("BENCHMARK RESULTS")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    print("\nResults saved to:")
    print(output_file)

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()