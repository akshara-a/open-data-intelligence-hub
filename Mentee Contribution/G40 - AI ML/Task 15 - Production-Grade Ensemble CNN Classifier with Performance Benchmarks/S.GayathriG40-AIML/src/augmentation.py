import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def create_augmentation():
    augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10)
    ])

    return augmentation


def augment_images(images):
    augmentation = create_augmentation()
    return augmentation(images, training=True)