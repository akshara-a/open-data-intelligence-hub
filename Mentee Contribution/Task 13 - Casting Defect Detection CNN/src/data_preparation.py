from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_DIR / "data" / "casting_data"

TRAIN_DIR = DATASET_DIR / "train"
TEST_DIR = DATASET_DIR / "test"


# Image settings
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32


def load_dataset():
    """
    Loads training and testing images from the dataset folders.
    """

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.2
    )

    test_datagen = ImageDataGenerator(
        rescale=1.0 / 255
    )

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        subset="training",
        shuffle=True
    )

    validation_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        subset="validation",
        shuffle=False
    )

    test_generator = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        shuffle=False
    )

    print("Class labels:", train_generator.class_indices)
    print("Training images:", train_generator.samples)
    print("Validation images:", validation_generator.samples)
    print("Testing images:", test_generator.samples)

    return train_generator, validation_generator, test_generator


if __name__ == "__main__":
    load_dataset()