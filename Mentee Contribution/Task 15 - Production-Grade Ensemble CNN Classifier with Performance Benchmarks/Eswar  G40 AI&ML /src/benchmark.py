"""
benchmark.py

Measures ensemble-level latency, throughput, total model size, total
parameter count, and approximate memory footprint (sum across the three
models run back-to-back per prediction).
"""

import time
import numpy as np


def benchmark_ensemble(trained_models, model_names, test_images, individual_results):
    single_image = test_images[0:1]

    latencies = []
    for _ in range(100):
        t_start = time.time()
        for name in model_names:
            trained_models[name].predict(single_image, verbose=0)
        latencies.append((time.time() - t_start) * 1000)
    latencies = np.array(latencies)

    n_throughput = min(1000, len(test_images))
    t_start = time.time()
    for name in model_names:
        trained_models[name].predict(test_images[:n_throughput], batch_size=64, verbose=0)
    throughput = n_throughput / (time.time() - t_start)

    return {
        "latency_ms_avg": float(latencies.mean()),
        "latency_ms_min": float(latencies.min()),
        "latency_ms_max": float(latencies.max()),
        "throughput_img_per_sec": float(throughput),
        "total_model_size_mb": float(sum(individual_results[n]["model_size_mb"] for n in model_names)),
        "total_param_count": int(sum(individual_results[n]["param_count"] for n in model_names)),
        "approx_memory_mb": float(sum(individual_results[n]["memory_delta_mb"] for n in model_names)),
    }
