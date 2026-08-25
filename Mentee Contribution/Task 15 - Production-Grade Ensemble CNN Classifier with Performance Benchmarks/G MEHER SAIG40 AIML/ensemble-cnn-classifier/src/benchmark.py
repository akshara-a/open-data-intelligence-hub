import os
import time
import numpy as np
import tensorflow as tf

from data_loader import load_cifar10


# ============================================================
# PROJECT PATHS
# ============================================================

SRC_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    SRC_DIR
)

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)

RESULTS_DIR = os.path.join(
    PROJECT_ROOT,
    "results"
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATHS = {

    "CNN 1": os.path.join(
        MODEL_DIR,
        "cnn_baseline.keras"
    ),

    "CNN 2": os.path.join(
        MODEL_DIR,
        "cnn_regularized.keras"
    ),

    "CNN 3": os.path.join(
        MODEL_DIR,
        "cnn_deep.keras"
    )
}


# ============================================================
# WEIGHTED ENSEMBLE
# ============================================================

WEIGHTS = {

    "CNN 1": 0.20,
    "CNN 2": 0.10,
    "CNN 3": 0.70
}


# ============================================================
# BENCHMARK CONFIGURATION
# ============================================================

BATCH_SIZE = 32

# Number of warm-up predictions
WARMUP_RUNS = 3

# Number of timed prediction runs
TIMED_RUNS = 10

# Number of images used for latency test
LATENCY_IMAGES = 1000


# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 60)
print("LOADING TEST DATA")
print("=" * 60)

(
    x_train,
    y_train,
    x_val,
    y_val,
    x_test,
    y_test
) = load_cifar10()


benchmark_images = x_test[
    :LATENCY_IMAGES
]


# ============================================================
# LOAD MODELS
# ============================================================

print("\n" + "=" * 60)
print("LOADING MODELS")
print("=" * 60)

models = {}

for name, path in MODEL_PATHS.items():

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Model not found:\n{path}"
        )

    print(
        f"\nLoading {name}..."
    )

    models[name] = tf.keras.models.load_model(
        path
    )

    print(
        f"{name} loaded successfully."
    )


# ============================================================
# GET MODEL INFORMATION
# ============================================================

def get_model_size_mb(path):

    size_bytes = os.path.getsize(
        path
    )

    return size_bytes / (
        1024 * 1024
    )


model_info = {}


for name, model in models.items():

    model_info[name] = {

        "parameters": model.count_params(),

        "size_mb": get_model_size_mb(
            MODEL_PATHS[name]
        )
    }


# ============================================================
# BENCHMARK INDIVIDUAL MODELS
# ============================================================

benchmark_results = {}


print("\n" + "=" * 60)
print("INDIVIDUAL MODEL BENCHMARKING")
print("=" * 60)


for name, model in models.items():

    print(
        f"\nBenchmarking {name}..."
    )


    # --------------------------------------------------------
    # Warm-up
    # --------------------------------------------------------

    for _ in range(
        WARMUP_RUNS
    ):

        model.predict(
            benchmark_images,
            batch_size=BATCH_SIZE,
            verbose=0
        )


    # --------------------------------------------------------
    # Timed runs
    # --------------------------------------------------------

    times = []


    for _ in range(
        TIMED_RUNS
    ):

        start_time = time.perf_counter()


        model.predict(
            benchmark_images,
            batch_size=BATCH_SIZE,
            verbose=0
        )


        end_time = time.perf_counter()


        elapsed = (
            end_time
            - start_time
        )

        times.append(
            elapsed
        )


    times = np.array(
        times
    )


    average_time = np.mean(
        times
    )

    std_time = np.std(
        times
    )


    # --------------------------------------------------------
    # Per-image latency
    # --------------------------------------------------------

    latency_ms = (
        average_time
        / LATENCY_IMAGES
        * 1000
    )


    # --------------------------------------------------------
    # Throughput
    # --------------------------------------------------------

    throughput = (
        LATENCY_IMAGES
        / average_time
    )


    benchmark_results[name] = {

        "parameters":
            model_info[name]["parameters"],

        "size_mb":
            model_info[name]["size_mb"],

        "average_time":
            average_time,

        "std_time":
            std_time,

        "latency_ms":
            latency_ms,

        "throughput":
            throughput
    }


    print(
        f"Parameters : "
        f"{model_info[name]['parameters']:,}"
    )

    print(
        f"Model Size : "
        f"{model_info[name]['size_mb']:.2f} MB"
    )

    print(
        f"Average Time : "
        f"{average_time:.4f} seconds"
    )

    print(
        f"Latency : "
        f"{latency_ms:.3f} ms/image"
    )

    print(
        f"Throughput : "
        f"{throughput:.2f} images/sec"
    )


# ============================================================
# BENCHMARK WEIGHTED ENSEMBLE
# ============================================================

print("\n" + "=" * 60)
print("BENCHMARKING WEIGHTED ENSEMBLE")
print("=" * 60)


# ------------------------------------------------------------
# Warm-up ensemble
# ------------------------------------------------------------

for _ in range(
    WARMUP_RUNS
):

    ensemble_probabilities = []

    for name, model in models.items():

        probabilities = model.predict(
            benchmark_images,
            batch_size=BATCH_SIZE,
            verbose=0
        )

        ensemble_probabilities.append(
            probabilities
        )


    final_probabilities = (

        WEIGHTS["CNN 1"]
        * ensemble_probabilities[0]

        +

        WEIGHTS["CNN 2"]
        * ensemble_probabilities[1]

        +

        WEIGHTS["CNN 3"]
        * ensemble_probabilities[2]
    )


# ------------------------------------------------------------
# Timed ensemble runs
# ------------------------------------------------------------

ensemble_times = []


for _ in range(
    TIMED_RUNS
):

    start_time = time.perf_counter()


    ensemble_probabilities = []


    for name, model in models.items():

        probabilities = model.predict(
            benchmark_images,
            batch_size=BATCH_SIZE,
            verbose=0
        )

        ensemble_probabilities.append(
            probabilities
        )


    final_probabilities = (

        WEIGHTS["CNN 1"]
        * ensemble_probabilities[0]

        +

        WEIGHTS["CNN 2"]
        * ensemble_probabilities[1]

        +

        WEIGHTS["CNN 3"]
        * ensemble_probabilities[2]
    )


    # Convert probabilities into predictions
    np.argmax(
        final_probabilities,
        axis=1
    )


    end_time = time.perf_counter()


    elapsed = (
        end_time
        - start_time
    )

    ensemble_times.append(
        elapsed
    )


ensemble_times = np.array(
    ensemble_times
)


ensemble_average_time = np.mean(
    ensemble_times
)

ensemble_std_time = np.std(
    ensemble_times
)


ensemble_latency_ms = (
    ensemble_average_time
    / LATENCY_IMAGES
    * 1000
)


ensemble_throughput = (
    LATENCY_IMAGES
    / ensemble_average_time
)


# ============================================================
# ENSEMBLE MODEL SIZE
# ============================================================

ensemble_size_mb = sum(
    info["size_mb"]
    for info in model_info.values()
)


ensemble_parameters = sum(
    info["parameters"]
    for info in model_info.values()
)


print(
    f"\nEnsemble Parameters : "
    f"{ensemble_parameters:,}"
)

print(
    f"Ensemble Model Size : "
    f"{ensemble_size_mb:.2f} MB"
)

print(
    f"Average Time : "
    f"{ensemble_average_time:.4f} seconds"
)

print(
    f"Latency : "
    f"{ensemble_latency_ms:.3f} ms/image"
)

print(
    f"Throughput : "
    f"{ensemble_throughput:.2f} images/sec"
)


# ============================================================
# FINAL BENCHMARK TABLE
# ============================================================

print("\n\n" + "=" * 100)
print("PRODUCTION BENCHMARK RESULTS")
print("=" * 100)


print(
    f"{'Model':<22}"
    f"{'Parameters':>15}"
    f"{'Size(MB)':>12}"
    f"{'Latency(ms)':>15}"
    f"{'Throughput':>15}"
)

print("-" * 100)


for name, result in benchmark_results.items():

    print(
        f"{name:<22}"
        f"{result['parameters']:>15,}"
        f"{result['size_mb']:>12.2f}"
        f"{result['latency_ms']:>15.3f}"
        f"{result['throughput']:>15.2f}"
    )


print(
    f"{'Weighted Ensemble':<22}"
    f"{ensemble_parameters:>15,}"
    f"{ensemble_size_mb:>12.2f}"
    f"{ensemble_latency_ms:>15.3f}"
    f"{ensemble_throughput:>15.2f}"
)


# ============================================================
# SAVE RESULTS
# ============================================================

results_path = os.path.join(
    RESULTS_DIR,
    "production_benchmark.txt"
)


with open(
    results_path,
    "w"
) as file:

    file.write(
        "PRODUCTION BENCHMARK RESULTS\n"
    )

    file.write(
        "=" * 100 + "\n\n"
    )


    file.write(
        f"{'Model':<22}"
        f"{'Parameters':>15}"
        f"{'Size(MB)':>12}"
        f"{'Latency(ms)':>15}"
        f"{'Throughput':>15}\n"
    )


    file.write(
        "-" * 100 + "\n"
    )


    for name, result in benchmark_results.items():

        file.write(
            f"{name:<22}"
            f"{result['parameters']:>15,}"
            f"{result['size_mb']:>12.2f}"
            f"{result['latency_ms']:>15.3f}"
            f"{result['throughput']:>15.2f}\n"
        )


    file.write(
        f"{'Weighted Ensemble':<22}"
        f"{ensemble_parameters:>15,}"
        f"{ensemble_size_mb:>12.2f}"
        f"{ensemble_latency_ms:>15.3f}"
        f"{ensemble_throughput:>15.2f}\n"
    )


    file.write(
        "\nWeighted Ensemble Weights:\n"
    )

    file.write(
        "CNN 1 = 0.20\n"
    )

    file.write(
        "CNN 2 = 0.10\n"
    )

    file.write(
        "CNN 3 = 0.70\n"
    )


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 60)
print("PRODUCTION BENCHMARKING COMPLETED")
print("=" * 60)

print(
    f"Results saved to:\n"
    f"{results_path}"
)