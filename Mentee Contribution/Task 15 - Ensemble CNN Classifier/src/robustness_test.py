import numpy as np
import tensorflow as tf

from src.data_loader import load_mnist_data
from src.preprocessing import normalize_images


def add_noise(images):
    """
    Add small random noise to images.
    """

    noise = np.random.normal(
        loc=0.0,
        scale=0.10,
        size=images.shape
    )

    noisy_images = images + noise

    noisy_images = np.clip(
        noisy_images,
        0.0,
        1.0
    )

    return noisy_images


def test_model_robustness():
    print("Loading MNIST dataset...")

    _, _, x_test, y_test = load_mnist_data()

    _, x_test = normalize_images(
        x_test,
        x_test
    )

    print("Loading CNN model...")

    model = tf.keras.models.load_model(
        "models/cnn_model_2.keras"
    )

    print("Evaluating on clean images...")

    clean_loss, clean_accuracy = model.evaluate(
        x_test,
        y_test,
        verbose=0
    )

    print(
        "Accuracy on clean images:",
        clean_accuracy
    )

    print("Adding noise to test images...")

    noisy_images = add_noise(x_test)

    print("Evaluating on noisy images...")

    noisy_loss, noisy_accuracy = model.evaluate(
        noisy_images,
        y_test,
        verbose=0
    )

    print(
        "Accuracy on noisy images:",
        noisy_accuracy
    )

    accuracy_drop = (
        clean_accuracy - noisy_accuracy
    )

    print(
        "Accuracy drop:",
        accuracy_drop
    )


if __name__ == "__main__":
    test_model_robustness()