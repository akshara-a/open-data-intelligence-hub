import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split


def load_cifar10():
    """
    Load CIFAR-10 and create a 70/15/15
    train-validation-test split.
    """

    # Load CIFAR-10
    (x_train, y_train), (x_test_original, y_test_original) = (
        tf.keras.datasets.cifar10.load_data()
    )

    # Combine the original train and test sets
    x = np.concatenate((x_train, x_test_original), axis=0)
    y = np.concatenate((y_train, y_test_original), axis=0)

    # Flatten labels
    y = y.flatten()

    # Normalize pixel values from [0, 255] to [0, 1]
    x = x.astype("float32") / 255.0

    # First split:
    # 70% training, 30% temporary
    x_train, x_temp, y_train, y_temp = train_test_split(
        x,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y
    )

    # Second split:
    # 15% validation, 15% test
    x_val, x_test, y_val, y_test = train_test_split(
        x_temp,
        y_temp,
        test_size=0.50,
        random_state=42,
        stratify=y_temp
    )

    print("\nDataset loaded successfully!")
    print("-" * 40)

    print(f"Training data   : {x_train.shape}")
    print(f"Validation data : {x_val.shape}")
    print(f"Testing data    : {x_test.shape}")

    print("\nClass distribution:")
    for class_id in range(10):
        print(
            f"Class {class_id}: "
            f"{np.sum(y_train == class_id)} training samples"
        )

    print("\nPixel range:")
    print(f"Minimum: {x_train.min():.2f}")
    print(f"Maximum: {x_train.max():.2f}")

    return (
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test
    )


if __name__ == "__main__":
    load_cifar10()