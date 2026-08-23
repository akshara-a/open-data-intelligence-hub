"""Production Resource & Latency Benchmarking Engine."""

import os
import time
import numpy as np
import pandas as pd
import psutil
import tensorflow as tf
from ensemble import soft_voting_predict


def measure_inference_latency_and_throughput(
    predict_fn, x_data: np.ndarray, num_runs: int = 100, batch_size: int = 1
) -> tuple[float, float, float, float]:
    """Measures inference time per sample and throughput.

    Args:
        predict_fn: Callable taking a batch numpy array and returning probabilities.
        x_data: Input test evaluation image tensor.
        num_runs: Total iterations over batch.
        batch_size: Samples per inference step.

    Returns:
        Tuple of (avg_latency_ms, min_latency_ms, max_latency_ms, throughput_img_per_sec).
    """
    latencies = []
    sample_batch = x_data[:batch_size]

    # Warmup invocation
    _ = predict_fn(sample_batch)

    for _ in range(num_runs):
        start = time.perf_counter()
        _ = predict_fn(sample_batch)
        elapsed = (time.perf_counter() - start) * 1000.0  # ms
        latencies.append(elapsed)

    avg_lat = float(np.mean(latencies))
    min_lat = float(np.min(latencies))
    max_lat = float(np.max(latencies))
    throughput = float((batch_size / (avg_lat / 1000.0)))

    return avg_lat, min_lat, max_lat, throughput


def run_benchmarks(
    models_dir: str = "models", results_dir: str = "results"
) -> pd.DataFrame:
    """Executes memory, disk footprint, and latency benchmarks across architectures."""
    from data_loader import load_cifar10_data
    from preprocessing import normalize_images

    _, _, (x_test, _), _ = load_cifar10_data()
    x_test_norm = normalize_images(x_test)

    model_files = {
        "CNN_Baseline": "cnn_baseline.keras",
        "CNN_Regularized": "cnn_regularized.keras",
        "CNN_Deep": "cnn_deep.keras",
    }

    loaded_models = []
    records = []

    process = psutil.Process(os.getpid())

    for name, filename in model_files.items():
        path = os.path.join(models_dir, filename)
        file_size_mb = os.path.getsize(path) / (1024 * 1024)

        mem_before = process.memory_info().rss / (1024 * 1024)
        model = tf.keras.models.load_model(path)
        mem_after = process.memory_info().rss / (1024 * 1024)

        params_count = model.count_params()
        loaded_models.append(model)

        avg_lat, min_lat, max_lat, tp = (
            measure_inference_latency_and_throughput(
                lambda x: model.predict(x, verbose=0),
                x_test_norm,
                batch_size=1,
            )
        )

        records.append(
            {
                "Model": name,
                "Model Size (MB)": round(file_size_mb, 2),
                "Parameters": params_count,
                "Memory Delta (MB)": round(mem_after - mem_before, 2),
                "Avg Latency (ms)": round(avg_lat, 2),
                "Min Latency (ms)": round(min_lat, 2),
                "Max Latency (ms)": round(max_lat, 2),
                "Throughput (img/sec)": round(tp, 2),
            }
        )

    # Ensemble execution profile
    def ensemble_pred_fn(x):
        preds = [m.predict(x, verbose=0) for m in loaded_models]
        return soft_voting_predict(preds)

    total_size = sum([r["Model Size (MB)"] for r in records])
    total_params = sum([r["Parameters"] for r in records])

    avg_lat, min_lat, max_lat, tp = measure_inference_latency_and_throughput(
        ensemble_pred_fn, x_test_norm, batch_size=1
    )

    records.append(
        {
            "Model": "Ensemble (Soft Voting)",
            "Model Size (MB)": round(total_size, 2),
            "Parameters": total_params,
            "Memory Delta (MB)": np.nan,
            "Avg Latency (ms)": round(avg_lat, 2),
            "Min Latency (ms)": round(min_lat, 2),
            "Max Latency (ms)": round(max_lat, 2),
            "Throughput (img/sec)": round(tp, 2),
        }
    )

    df = pd.DataFrame(records)
    os.makedirs(results_dir, exist_ok=True)
    df.to_csv(os.path.join(results_dir, "benchmark_results.csv"), index=False)
    return df


if __name__ == "__main__":
    benchmark_df = run_benchmarks()
    print(benchmark_df.to_string(index=False))