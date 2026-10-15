import tensorflow as tf


def load_mnist_data():
    """
    Load the MNIST handwritten digit dataset.
    """

    print("Loading MNIST dataset...")

    (x_train, y_train), (x_test, y_test) = (
        tf.keras.datasets.mnist.load_data()
    )

    # Use a smaller subset for faster training
    x_train = x_train[:10000]
    y_train = y_train[:10000]

    x_test = x_test[:2000]
    y_test = y_test[:2000]

    # Add channel dimension
    x_train = x_train[..., tf.newaxis]
    x_test = x_test[..., tf.newaxis]

    print("Dataset loaded successfully")
    print("Training images:", x_train.shape)
    print("Training labels:", y_train.shape)
    print("Test images:", x_test.shape)
    print("Test labels:", y_test.shape)

    return x_train, y_train, x_test, y_test


if __name__ == "__main__":
    load_mnist_data()