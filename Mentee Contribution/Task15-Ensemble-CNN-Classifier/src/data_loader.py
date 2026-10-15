import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


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
    "truck",
]

NUM_CLASSES = 10
BATCH_SIZE = 32
RANDOM_SEED = 42

# CIFAR-10 is stored outside OneDrive.
CIFAR10_DIR = r"C:\Task15-CIFAR10\cifar-10-batches-py"


def load_batch(file_path):
    """Load one CIFAR-10 batch file."""

    with open(file_path, "rb") as file:
        batch = pickle.load(file, encoding="bytes")

    images = batch[b"data"]
    labels = batch[b"labels"]

    # CIFAR-10 stores images as:
    # 3072 = 3 channels * 32 * 32
    images = images.reshape(-1, 3, 32, 32)
    images = images.transpose(0, 2, 3, 1)

    return images, np.array(labels)


def load_cifar10_local():
    """Load CIFAR-10 directly from the extracted local files."""

    print("Loading CIFAR-10 from local files...")
    print(f"Dataset location: {CIFAR10_DIR}")

    if not os.path.isdir(CIFAR10_DIR):
        raise FileNotFoundError(
            f"CIFAR-10 directory not found: {CIFAR10_DIR}"
        )

    train_images = []
    train_labels = []

    for i in range(1, 6):
        file_path = os.path.join(
            CIFAR10_DIR,
            f"data_batch_{i}",
        )

        print(f"Loading data_batch_{i}...")

        images, labels = load_batch(file_path)

        train_images.append(images)
        train_labels.append(labels)

    x_train = np.concatenate(train_images, axis=0)
    y_train = np.concatenate(train_labels, axis=0)

    test_file = os.path.join(
        CIFAR10_DIR,
        "test_batch",
    )

    print("Loading test_batch...")

    x_test, y_test = load_batch(test_file)

    print(f"Training images: {len(x_train)}")
    print(f"Test images: {len(x_test)}")
    print(f"Image shape: {x_train.shape[1:]}")
    print(f"Number of classes: {NUM_CLASSES}")

    return x_train, y_train, x_test, y_test


def prepare_datasets():
    """Prepare training, validation and test datasets."""

    x_train, y_train, x_test, y_test = load_cifar10_local()

    # Normalize pixels from 0-255 to 0-1.
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # Use 5,000 training images for validation.
    x_val = x_train[-5000:]
    y_val = y_train[-5000:]

    x_train = x_train[:-5000]
    y_train = y_train[:-5000]

    print("\nDataset preparation complete:")
    print(f"Training:   {len(x_train)} images")
    print(f"Validation: {len(x_val)} images")
    print(f"Test:       {len(x_test)} images")

    return (
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test,
    )


def create_augmentation():
    """Create augmentation for training data only."""

    return tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip(
                "horizontal",
                seed=RANDOM_SEED,
            ),
            tf.keras.layers.RandomRotation(
                0.10,
                seed=RANDOM_SEED,
            ),
            tf.keras.layers.RandomZoom(
                0.10,
                seed=RANDOM_SEED,
            ),
            tf.keras.layers.RandomContrast(
                0.10,
                seed=RANDOM_SEED,
            ),
        ],
        name="data_augmentation",
    )


def create_tf_datasets(
    x_train,
    y_train,
    x_val,
    y_val,
    x_test,
    y_test,
):
    """Create TensorFlow datasets."""

    augmentation = create_augmentation()

    train_ds = tf.data.Dataset.from_tensor_slices(
        (x_train, y_train)
    )

    val_ds = tf.data.Dataset.from_tensor_slices(
        (x_val, y_val)
    )

    test_ds = tf.data.Dataset.from_tensor_slices(
        (x_test, y_test)
    )

    # Augmentation ONLY for training.
    train_ds = (
        train_ds
        .shuffle(
            len(x_train),
            seed=RANDOM_SEED,
            reshuffle_each_iteration=True,
        )
        .batch(BATCH_SIZE)
        .map(
            lambda images, labels: (
                augmentation(images, training=True),
                labels,
            ),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
        .prefetch(tf.data.AUTOTUNE)
    )

    # No augmentation for validation.
    val_ds = (
        val_ds
        .batch(BATCH_SIZE)
        .prefetch(tf.data.AUTOTUNE)
    )

    # No augmentation for test.
    test_ds = (
        test_ds
        .batch(BATCH_SIZE)
        .prefetch(tf.data.AUTOTUNE)
    )

    return train_ds, val_ds, test_ds


def visualize_samples(
    x_train,
    y_train,
    output_path,
):
    """Save sample CIFAR-10 images."""

    directory = os.path.dirname(output_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    plt.figure(figsize=(12, 8))

    for i in range(12):
        plt.subplot(3, 4, i + 1)

        plt.imshow(x_train[i])

        plt.title(
            CLASS_NAMES[y_train[i]]
        )

        plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=150,
    )

    plt.close()

    print(
        f"Sample visualization saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":

    print("=" * 60)
    print("TASK 15 - CIFAR-10 DATA PREPARATION")
    print("=" * 60)

    (
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test,
    ) = prepare_datasets()

    train_ds, val_ds, test_ds = create_tf_datasets(
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test,
    )

    visualize_samples(
        x_train,
        y_train,
        "reports/cifar10_samples.png",
    )

    print("\nTensorFlow datasets created successfully.")

    print(
        "Training batches:   "
        f"{tf.data.experimental.cardinality(train_ds).numpy()}"
    )

    print(
        "Validation batches: "
        f"{tf.data.experimental.cardinality(val_ds).numpy()}"
    )

    print(
        "Test batches:       "
        f"{tf.data.experimental.cardinality(test_ds).numpy()}"
    )

    print(
        "\nTASK 15 DATA PIPELINE COMPLETED SUCCESSFULLY."
    )