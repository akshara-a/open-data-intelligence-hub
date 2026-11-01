"""
Part 8 — Production Benchmark (Sections 46-54).
Measures latency, throughput, model size, parameter count, memory.
"""

import os
import time
import psutil
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from data_loader import load_cifar10
from preprocessing import prepare_dataset

MODELS_DIR = "models"
RESULTS_DIR = "results"
N_RUNS = 100  # repeated single-image predictions for stable latency stats


def measure_latency(model, sample, n_runs=N_RUNS):
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        model.predict(sample, verbose=0)
        times.append((time.perf_counter() - start) * 1000)  # ms
    return {
        "avg_latency_ms": float(np.mean(times)),
        "min_latency_ms": float(np.min(times)),
        "max_latency_ms": float(np.max(times)),
    }


def measure_throughput(model, x_batch):
    start = time.perf_counter()
    model.predict(x_batch, verbose=0)
    elapsed = time.perf_counter() - start
    return len(x_batch) / elapsed  # images/sec


def get_model_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def get_param_count(model):
    return model.count_params()


def measure_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def benchmark_single(model, model_path, sample, x_batch):
    mem_before = measure_memory_mb()
    latency_stats = measure_latency(model, sample)
    throughput = measure_throughput(model, x_batch)
    mem_after = measure_memory_mb()

    return {
        **latency_stats,
        "throughput_img_per_sec": throughput,
        "model_size_mb": get_model_size_mb(model_path),
        "parameters": get_param_count(model),
        "memory_mb": mem_after - mem_before,
    }


def benchmark_ensemble(models, sample, x_batch):
    mem_before = measure_memory_mb()

    times = []
    for _ in range(N_RUNS):
        start = time.perf_counter()
        for m in models:
            m.predict(sample, verbose=0)
        times.append((time.perf_counter() - start) * 1000)

    start = time.perf_counter()
    for m in models:
        m.predict(x_batch, verbose=0)
    elapsed = time.perf_counter() - start
    throughput = len(x_batch) / elapsed

    mem_after = measure_memory_mb()

    return {
        "avg_latency_ms": float(np.mean(times)),
        "min_latency_ms": float(np.min(times)),
        "max_latency_ms": float(np.max(times)),
        "throughput_img_per_sec": throughput,
        "memory_mb": mem_after - mem_before,
    }


def main():
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()
    (_, _), (_, _), (x_test, y_test) = prepare_dataset(
        x_train, y_train, x_val, y_val, x_test, y_test
    )

    sample = x_test[:1]
    x_batch = x_test[:64]

    model_names = ["cnn_baseline", "cnn_regularized", "cnn_deep"]
    paths = [os.path.join(MODELS_DIR, f"{n}.keras") for n in model_names]
    if not all(os.path.exists(p) for p in paths):
        print("Train all three models first (src/train.py).")
        return

    models = [load_model(p) for p in paths]
    results = []

    for name, path, model in zip(model_names, paths, models):
        stats = benchmark_single(model, path, sample, x_batch)
        stats["model"] = name
        results.append(stats)
        print(name, stats)

    ensemble_stats = benchmark_ensemble(models, sample, x_batch)
    ensemble_stats["model"] = "ensemble_sequential"
    ensemble_stats["model_size_mb"] = sum(get_model_size_mb(p) for p in paths)
    ensemble_stats["parameters"] = sum(get_param_count(m) for m in models)
    results.append(ensemble_stats)
    print("ensemble", ensemble_stats)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame(results).to_csv(
        os.path.join(RESULTS_DIR, "benchmark_results.csv"), index=False
    )


if __name__ == "__main__":
    main()
