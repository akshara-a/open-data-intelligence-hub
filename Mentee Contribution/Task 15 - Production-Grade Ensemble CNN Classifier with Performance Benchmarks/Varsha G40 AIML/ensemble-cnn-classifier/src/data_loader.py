import numpy as np
import tensorflow as tf


def load_cifar10_subset():
    """
    Load the same CIFAR-10 subset used by the project.

    Returns:
        X_test: 200 test images
        y_test: 200 test labels
    """

    print("Downloading/loading CIFAR-10...")

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

    # Select 20 test images from each of the 10 classes = 200 images
    selected_indices = []

    for class_id in range(10):
        class_indices = np.where(y_test.flatten() == class_id)[0]
        selected_indices.extend(class_indices[:20])

    selected_indices = np.array(selected_indices)

    X_test = x_test[selected_indices]
    y_test = y_test[selected_indices].flatten()

    print("Selected test images:", X_test.shape)
    print("Selected test labels:", y_test.shape)

    return X_test, y_test