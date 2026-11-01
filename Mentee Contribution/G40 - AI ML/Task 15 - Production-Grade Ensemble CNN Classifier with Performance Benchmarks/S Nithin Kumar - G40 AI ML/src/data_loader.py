import numpy as np
from tensorflow.keras.datasets import cifar10
from sklearn.model_selection import train_test_split


def load_and_prepare_data():
    """
    Load CIFAR-10 dataset, normalize images,
    and create training, validation, and test sets.
    """

    print("Loading CIFAR-10 dataset...")

    # Load CIFAR-10
    (X_train_full, y_train_full), (X_test, y_test) = cifar10.load_data()

    # Convert labels from shape (n, 1) to (n,)
    y_train_full = y_train_full.flatten()
    y_test = y_test.flatten()

    # Normalize pixel values from 0-255 to 0-1
    X_train_full = X_train_full.astype("float32") / 255.0
    X_test = X_test.astype("float32") / 255.0

    # Create validation set from training data
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full,
        y_train_full,
        test_size=0.15,
        random_state=42,
        stratify=y_train_full
    )

    class_names = [
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

    print("\nDataset loaded successfully!")
    print(f"Training images   : {X_train.shape}")
    print(f"Validation images : {X_val.shape}")
    print(f"Test images       : {X_test.shape}")
    print(f"Number of classes : {len(class_names)}")

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        class_names
    )


if __name__ == "__main__":
    load_and_prepare_data()