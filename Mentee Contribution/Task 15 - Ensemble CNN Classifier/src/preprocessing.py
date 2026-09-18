import numpy as np


def normalize_images(x_train, x_test):
    """
    Normalize image pixel values from 0-255 to 0-1.
    """

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    return x_train, x_test


def add_channel_dimension(x_train, x_test):
    """
    Add the channel dimension required by CNN models.
    """

    if len(x_train.shape) == 3:
        x_train = x_train[..., np.newaxis]

    if len(x_test.shape) == 3:
        x_test = x_test[..., np.newaxis]

    return x_train, x_test