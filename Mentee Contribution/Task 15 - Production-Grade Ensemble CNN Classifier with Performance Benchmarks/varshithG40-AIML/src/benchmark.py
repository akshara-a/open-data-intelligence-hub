"""
benchmark.py
============
Production-Grade Benchmarking Suite for individual CNNs and Ensemble Classifier.
Measures:
  1. Inference Latency (Avg, Min, Max, Std in milliseconds)
  2. Throughput (Images/second)
  3. Disk Footprint / Model Size (MB)
  4. Total & Trainable Parameters
  5. Peak Memory Usage (RAM in MB via psutil)
  6. Sequential vs Parallel ThreadPool Inference Comparison
Outputs formatted benchmark tables to results/benchmark_results.csv and results/final_comparison.csv.
"""

import os
import time
import psutil
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tensorflow import keras

from .preprocessing import load_full_dataset
from .ensemble import EnsembleClassifier

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")

NUM_WARMUP = 5
NUM_BENCHMARK_RUNS = 40


def get_model_size_mb(filepath: str) -> float:
    """Returns disk file size in megabytes."""
    if os.path.exists(filepath):
        return round(os.path.getsize(filepath) / (1024 * 1024), 3)
    return 0.0


def count_parameters(model: keras.Model) -> tuple:
    """Returns (total_params, trainable_params)."""
    total = sum(p.numpy().size for p in model.weights)
    trainable = sum(p.numpy().size for p in model.trainable_weights)
    return total, trainable


def measure_single_model_performance(model: keras.Model, sample_image: np.ndarray, num_runs: int = NUM_BENCHMARK_RUNS) -> dict:
    """
    Benchmarks latency, throughput, and memory consumption for one model.
    """
    # 1. Warm-up runs to eliminate cold-start/compilation overhead
    for _ in range(NUM_WARMUP):
        _ = model.predict(sample_image, verbose=0)
        
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)
    
    latencies = []
    t_start = time.perf_counter()
    for _ in range(num_runs):
        t0 = time.perf_counter()
        _ = model.predict(sample_image, verbose=0)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)  # ms
        
    total_time = time.perf_counter() - t_start
    mem_after = process.memory_info().rss / (1024 * 1024)
    
    avg_latency = float(np.mean(latencies))
    min_latency = float(np.min(latencies))
    max_latency = float(np.max(latencies))
    std_latency = float(np.std(latencies))
    throughput = float(num_runs / total_time)
    ram_usage = round(max(mem_after, mem_before), 2)
    
    return {
        "Avg Latency (ms)": round(avg_latency, 2),
        "Min Latency (ms)": round(min_latency, 2),
        "Max Latency (ms)": round(max_latency, 2),
        "Std Latency (ms)": round(std_latency, 2),
        "Throughput (img/s)": round(throughput, 1),
        "RAM Usage (MB)": ram_usage
    }


def measure_ensemble_performance(ensemble: EnsembleClassifier, sample_image: np.ndarray, num_runs: int = NUM_BENCHMARK_RUNS) -> dict:
    """
    Benchmarks latency, throughput, and memory for both Sequential and Parallel ensemble inference.
    """
    # Warm-up
    for _ in range(NUM_WARMUP):
        _ = ensemble.predict_soft_voting(sample_image)
        
    # --- Sequential Benchmark ---
    seq_latencies = []
    t_seq_start = time.perf_counter()
    for _ in range(num_runs):
        t0 = time.perf_counter()
        _ = ensemble.predict_soft_voting(sample_image)
        t1 = time.perf_counter()
        seq_latencies.append((t1 - t0) * 1000.0)
    total_seq_time = time.perf_counter() - t_seq_start

    # --- Parallel Benchmark via ThreadPoolExecutor ---
    par_latencies = []
    t_par_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=len(ensemble.models)) as executor:
        for _ in range(num_runs):
            t0 = time.perf_counter()
            futures = [executor.submit(m.predict, sample_image, 0) for m in ensemble.models]
            all_preds = [f.result() for f in futures]
            mean_probs = np.mean(all_preds, axis=0)
            _ = np.argmax(mean_probs, axis=1)
            t1 = time.perf_counter()
            par_latencies.append((t1 - t0) * 1000.0)
    total_par_time = time.perf_counter() - t_par_start

    process = psutil.Process(os.getpid())
    ram_usage = round(process.memory_info().rss / (1024 * 1024), 2)
    
    return {
        "Sequential": {
            "Avg Latency (ms)": round(float(np.mean(seq_latencies)), 2),
            "Min Latency (ms)": round(float(np.min(seq_latencies)), 2),
            "Max Latency (ms)": round(float(np.max(seq_latencies)), 2),
            "Std Latency (ms)": round(float(np.std(seq_latencies)), 2),
            "Throughput (img/s)": round(float(num_runs / total_seq_time), 1),
            "RAM Usage (MB)": ram_usage
        },
        "Parallel": {
            "Avg Latency (ms)": round(float(np.mean(par_latencies)), 2),
            "Min Latency (ms)": round(float(np.min(par_latencies)), 2),
            "Max Latency (ms)": round(float(np.max(par_latencies)), 2),
            "Std Latency (ms)": round(float(np.std(par_latencies)), 2),
            "Throughput (img/s)": round(float(num_runs / total_par_time), 1),
            "RAM Usage (MB)": ram_usage
        }
    }


def run_full_benchmark_suite():
    """
    Executes complete production benchmarking and writes results to CSVs.
    """
    print("\n=======================================================")
    print(" Running Production-Grade Performance Benchmarking")
    print("=======================================================")
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    _, _, (X_test, y_test), _ = load_full_dataset()
    sample_img = X_test[0:1]  # Single image batch (1, 128, 128, 3)
    
    # Load Models
    m1 = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_baseline.keras"))
    m2 = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_regularized.keras"))
    m3 = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_deep.keras"))
    
    models = {
        "CNN 1 (Baseline)": (m1, os.path.join(MODELS_DIR, "cnn_baseline.keras")),
        "CNN 2 (Regularized)": (m2, os.path.join(MODELS_DIR, "cnn_regularized.keras")),
        "CNN 3 (Deeper)": (m3, os.path.join(MODELS_DIR, "cnn_deep.keras"))
    }
    
    records = []
    for name, (model, path) in models.items():
        total_p, train_p = count_parameters(model)
        size_mb = get_model_size_mb(path)
        perf = measure_single_model_performance(model, sample_img)
        
        records.append({
            "Architecture": name,
            "Parameters (Trainable)": f"{train_p:,}",
            "Model Size (MB)": size_mb,
            "Avg Latency (ms)": perf["Avg Latency (ms)"],
            "Min Latency (ms)": perf["Min Latency (ms)"],
            "Max Latency (ms)": perf["Max Latency (ms)"],
            "Throughput (img/s)": perf["Throughput (img/s)"],
            "RAM Memory (MB)": perf["RAM Usage (MB)"]
        })
        
    # Ensemble Benchmark
    ensemble = EnsembleClassifier([m1, m2, m3])
    ens_perf = measure_ensemble_performance(ensemble, sample_img)
    total_ens_params = sum(count_parameters(m)[1] for m in [m1, m2, m3])
    total_ens_size = sum(get_model_size_mb(p) for _, (_, p) in models.items())
    
    records.append({
        "Architecture": "Ensemble (Sequential Soft Voting)",
        "Parameters (Trainable)": f"{total_ens_params:,} (Combined)",
        "Model Size (MB)": round(total_ens_size, 3),
        "Avg Latency (ms)": ens_perf["Sequential"]["Avg Latency (ms)"],
        "Min Latency (ms)": ens_perf["Sequential"]["Min Latency (ms)"],
        "Max Latency (ms)": ens_perf["Sequential"]["Max Latency (ms)"],
        "Throughput (img/s)": ens_perf["Sequential"]["Throughput (img/s)"],
        "RAM Memory (MB)": ens_perf["Sequential"]["RAM Usage (MB)"]
    })
    
    records.append({
        "Architecture": "Ensemble (Parallel Soft Voting)",
        "Parameters (Trainable)": f"{total_ens_params:,} (Combined)",
        "Model Size (MB)": round(total_ens_size, 3),
        "Avg Latency (ms)": ens_perf["Parallel"]["Avg Latency (ms)"],
        "Min Latency (ms)": ens_perf["Parallel"]["Min Latency (ms)"],
        "Max Latency (ms)": ens_perf["Parallel"]["Max Latency (ms)"],
        "Throughput (img/s)": ens_perf["Parallel"]["Throughput (img/s)"],
        "RAM Memory (MB)": ens_perf["Parallel"]["RAM Usage (MB)"]
    })
    
    bench_df = pd.DataFrame(records)
    csv_path = os.path.join(RESULTS_DIR, "benchmark_results.csv")
    bench_df.to_csv(csv_path, index=False)
    print(f"[SAVE] Benchmarking table saved to: {csv_path}")
    print("\n", bench_df.to_string(index=False))
    return bench_df


if __name__ == "__main__":
    run_full_benchmark_suite()
