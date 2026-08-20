import os
import sys
import time
import pandas as pd
import tensorflow as tf

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_prepare_data


MODEL_DIR = "models"
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


def get_model_size(model_path):
    """Return model file size in MB."""
    size_bytes = os.path.getsize(model_path)
    return size_bytes / (1024 * 1024)


def benchmark_model(model_name, X_test):
    """Measure model size, inference time and throughput."""

    print("\n" + "=" * 70)
    print(f"BENCHMARKING: {model_name.upper()}")
    print("=" * 70)

    model_path = os.path.join(
        MODEL_DIR,
        f"{model_name}.keras"
    )

    # Load model
    model = tf.keras.models.load_model(model_path)

    # Model size
    model_size = get_model_size(model_path)

    # Use first 1000 images for benchmarking
    X_sample = X_test[:1000]

    # Warm-up run
    print("Running warm-up...")
    _ = model.predict(X_sample[:10], verbose=0)

    # Measure inference time
    print("Measuring inference speed...")

    start_time = time.perf_counter()

    _ = model.predict(
        X_sample,
        verbose=0
    )

    end_time = time.perf_counter()

    total_time = end_time - start_time

    # Average time per image
    latency_ms = (
        total_time / len(X_sample)
    ) * 1000

    # Images per second
    throughput = (
        len(X_sample) / total_time
    )

    print(f"\nModel Size      : {model_size:.2f} MB")
    print(f"Total Time      : {total_time:.4f} seconds")
    print(f"Latency/Image   : {latency_ms:.4f} ms")
    print(f"Throughput      : {throughput:.2f} images/second")

    return {
        "Model": model_name,
        "Model_Size_MB": model_size,
        "Total_Time_1000_Images_sec": total_time,
        "Latency_per_Image_ms": latency_ms,
        "Throughput_Images_per_sec": throughput
    }


def main():

    # Load dataset
    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        class_names
    ) = load_and_prepare_data()

    model_names = [
        "baseline_cnn",
        "regularized_cnn",
        "deep_cnn"
    ]

    benchmark_results = []

    # Benchmark each model
    for model_name in model_names:

        result = benchmark_model(
            model_name,
            X_test
        )

        benchmark_results.append(result)

    # Create DataFrame
    results_df = pd.DataFrame(
        benchmark_results
    )

    # Save CSV
    output_path = os.path.join(
        RESULTS_DIR,
        "benchmark_results.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 70)
    print("FINAL BENCHMARK COMPARISON")
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