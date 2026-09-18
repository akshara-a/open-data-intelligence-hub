import time

import tensorflow as tf

from src.data_loader import load_mnist_data
from src.preprocessing import normalize_images


def benchmark_model():
    print("Loading MNIST dataset...")

    _, _, x_test, y_test = load_mnist_data()

    _, x_test = normalize_images(
        x_test,
        x_test
    )

    print("Loading trained CNN model...")

    model = tf.keras.models.load_model(
        "models/cnn_model_2.keras"
    )

    print("Running prediction benchmark...")

    start_time = time.time()

    predictions = model.predict(
        x_test,
        verbose=0
    )

    end_time = time.time()

    total_time = end_time - start_time

    average_time = total_time / len(x_test)

    loss, accuracy = model.evaluate(
        x_test,
        y_test,
        verbose=0
    )

    print("\nBenchmark Results")
    print("-----------------")
    print("Number of test images:", len(x_test))
    print("Model accuracy:", accuracy)
    print("Total prediction time:", total_time, "seconds")
    print(
        "Average prediction time per image:",
        average_time,
        "seconds"
    )
    print(
        "Predictions generated:",
        predictions.shape
    )


if __name__ == "__main__":
    benchmark_model()