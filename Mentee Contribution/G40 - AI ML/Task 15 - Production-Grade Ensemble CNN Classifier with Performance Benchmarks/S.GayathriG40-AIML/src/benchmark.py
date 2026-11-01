import time
import numpy as np


def benchmark_model(
    model,
    X_test,
    runs=5
):

    # Warm-up
    model.predict(
        X_test[:32],
        verbose=0
    )

    times = []

    for i in range(runs):

        start = time.perf_counter()

        model.predict(
            X_test,
            verbose=0
        )

        end = time.perf_counter()

        total_time = end - start

        time_per_image = (
            total_time /
            len(X_test)
        )

        times.append(
            time_per_image * 1000
        )

    average_time = np.mean(times)

    throughput = (
        1000 /
        average_time
    )

    return {

        "average_latency_ms":
            average_time,

        "minimum_latency_ms":
            np.min(times),

        "maximum_latency_ms":
            np.max(times),

        "images_per_second":
            throughput
    }


def compare_models(
    models,
    X_test
):

    results = {}

    for name, model in models.items():

        results[name] = benchmark_model(
            model,
            X_test
        )

    return results