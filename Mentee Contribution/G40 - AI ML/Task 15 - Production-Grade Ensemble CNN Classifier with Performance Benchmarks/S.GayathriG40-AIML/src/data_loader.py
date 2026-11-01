import numpy as np
from tensorflow.keras.datasets import cifar10


CLASS_NAMES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]


def load_cifar10():

    (X_train, y_train), (X_test, y_test) = cifar10.load_data()

    y_train = y_train.reshape(-1)
    y_test = y_test.reshape(-1)

    return X_train, y_train, X_test, y_test


def train_val_split(X, y, validation_size=5000, seed=42):

    np.random.seed(seed)

    indexes = np.random.permutation(len(X))

    X = X[indexes]
    y = y[indexes]

    X_val = X[:validation_size]
    y_val = y[:validation_size]

    X_train = X[validation_size:]
    y_train = y[validation_size:]

    return X_train, y_train, X_val, y_val