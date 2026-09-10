import numpy as np


def normalize_images(images):

    images = images.astype("float32")

    images = images / 255.0

    return images


def preprocess_dataset(
    X_train,
    y_train,
    X_val,
    y_val,
    X_test,
    y_test
):

    X_train = normalize_images(X_train)
    X_val = normalize_images(X_val)
    X_test = normalize_images(X_test)

    return (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test
    )