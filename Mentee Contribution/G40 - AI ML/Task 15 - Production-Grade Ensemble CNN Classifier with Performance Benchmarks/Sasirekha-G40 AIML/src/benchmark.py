import os
import time
import numpy as np
import pandas as pd
import psutil
import tensorflow as tf
from .config import MODELS_DIR, RESULTS_DIR
from .data_loader import create_or_load_splits
from .dataset import build_dataset

MODEL_NAMES = ["cnn_baseline", "cnn_regularized", "cnn_deep"]

def keras_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def benchmark(name, models, sample, runs=100):
    for model in models:
        model(sample, training=False)

    process = psutil.Process()
    memory_before = process.memory_info().rss

    times = []
    start_total = time.perf_counter()
    for _ in range(runs):
        start = time.perf_counter()
        for model in models:
            model(sample, training=False)
        times.append((time.perf_counter() - start) * 1000)
    total_seconds = time.perf_counter() - start_total
    memory_after = process.memory_info().rss

    file_names = name.split("+")
    size = sum(
        keras_file_size_mb(MODELS_DIR / f"{file_name}.keras")
        for file_name in file_names
    )

    return {
        "model": name,
        "average_latency_ms": float(np.mean(times)),
        "min_latency_ms": float(np.min(times)),
        "max_latency_ms": float(np.max(times)),
        "throughput_images_per_second": float(runs / total_seconds),
        "estimated_process_memory_change_mb": float((memory_after - memory_before) / (1024 * 1024)),
        "model_size_mb": float(size),
        "parameters": int(sum(model.count_params() for model in models)),
    }

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    _, _, test_df = create_or_load_splits()
    sample = next(iter(build_dataset(test_df).take(1)))[0][:1]

    loaded = {name: tf.keras.models.load_model(MODELS_DIR / f"{name}.keras") for name in MODEL_NAMES}
    rows = [benchmark(name, [model], sample) for name, model in loaded.items()]
    rows.append(benchmark("+".join(MODEL_NAMES), list(loaded.values()), sample))
    pd.DataFrame(rows).to_csv(RESULTS_DIR / "benchmark_results.csv", index=False)
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
