import os
import time
import numpy as np
import pandas as pd
import tensorflow as tf
import psutil

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("=" * 60)
print("CNN MODEL PERFORMANCE BENCHMARK")
print("=" * 60)

print("\nLoading CIFAR-10 subset...")

from data_loader import load_small_cifar10

data = load_small_cifar10()

X_test = data[4].astype("float32") / 255.0

print("Test images:", X_test.shape)

# --------------------------------------------------
# MODEL INFORMATION
# --------------------------------------------------

models_info = {
    "CNN1_Baseline": os.path.join(
        MODEL_DIR, "cnn_baseline.keras"
    ),
    "CNN2_Regularized": os.path.join(
        MODEL_DIR, "cnn_regularized.keras"
    ),
    "CNN3_Deep": os.path.join(
        MODEL_DIR, "cnn_deep.keras"
    )
}

results = []

# Use only a small number of images because laptop is slow
benchmark_images = X_test[:50]

# --------------------------------------------------
# BENCHMARK EACH MODEL
# --------------------------------------------------

for model_name, model_path in models_info.items():

    print("\n" + "=" * 60)
    print("Benchmarking:", model_name)
    print("=" * 60)

    if not os.path.exists(model_path):
        print("Model not found:", model_path)
        continue

    print("Loading model...")

    model = tf.keras.models.load_model(model_path)

    # Parameters
    parameters = model.count_params()

    # Model size
    model_size_mb = os.path.getsize(model_path) / (1024 * 1024)

    # --------------------------------------------------
    # WARM-UP
    # --------------------------------------------------

    model.predict(
        benchmark_images[:5],
        verbose=0
    )

    # --------------------------------------------------
    # LATENCY
    # --------------------------------------------------

    start_time = time.perf_counter()

    model.predict(
        benchmark_images,
        verbose=0
    )

    end_time = time.perf_counter()

    total_time = end_time - start_time

    latency_ms = (total_time / len(benchmark_images)) * 1000

    # --------------------------------------------------
    # THROUGHPUT
    # --------------------------------------------------

    throughput = len(benchmark_images) / total_time

    # --------------------------------------------------
    # MEMORY
    # --------------------------------------------------

    process = psutil.Process(os.getpid())

    memory_mb = process.memory_info().rss / (1024 * 1024)

    # --------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------

    result = {
        "Model": model_name,
        "Parameters": parameters,
        "Model Size (MB)": round(model_size_mb, 3),
        "Latency (ms/image)": round(latency_ms, 3),
        "Throughput (images/sec)": round(throughput, 3),
        "Memory Usage (MB)": round(memory_mb, 2)
    }

    results.append(result)

    print("\nParameters:", parameters)
    print("Model Size:", round(model_size_mb, 3), "MB")
    print("Latency:", round(latency_ms, 3), "ms/image")
    print("Throughput:", round(throughput, 3), "images/sec")
    print("Memory:", round(memory_mb, 2), "MB")

# --------------------------------------------------
# SAVE CSV
# --------------------------------------------------

df = pd.DataFrame(results)

csv_path = os.path.join(
    RESULTS_DIR,
    "benchmark_results.csv"
)

df.to_csv(csv_path, index=False)

# --------------------------------------------------
# DISPLAY FINAL RESULTS
# --------------------------------------------------

print("\n")
print("=" * 60)
print("FINAL BENCHMARK RESULTS")
print("=" * 60)

print(df.to_string(index=False))

print("\nResults saved to:")
print(csv_path)

print("\n" + "=" * 60)
print("BENCHMARK COMPLETED SUCCESSFULLY")
print("=" * 60)