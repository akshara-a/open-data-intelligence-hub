"""
CNN architecture for the casting defect binary classifier.

Architecture:

    Input (224, 224, 3)
      -> Data augmentation (train-time only, no-op at inference)
      -> Rescaling 1/255
      -> Conv2D 32 + ReLU -> MaxPooling
      -> Conv2D 64 + ReLU -> MaxPooling
      -> Conv2D 128 + ReLU -> MaxPooling
      -> GlobalAveragePooling2D
      -> Dropout
      -> Dense 64 + ReLU
      -> Dropout
      -> Dense 1 + Sigmoid
"""

import tensorflow as tf
from tensorflow.keras import layers, models

from src import config


def build_data_augmentation() -> tf.keras.Sequential:
    """
    Mild, industrially-realistic augmentation applied ONLY to training data.

    Why mild augmentation matters here:
    Casting defects (cracks, holes, rough surfaces) can be small and subtle.
    Aggressive transformations (large rotations, heavy cropping, strong
    blurring, extreme color shifts) risk destroying or hiding the very
    feature the model needs to learn, or creating images that no longer
    resemble what the factory camera actually produces. Keeping the
    transformations small teaches the model that a defect is still a
    defect under minor viewpoint/lighting variation, without inventing
    unrealistic training examples.
    """
    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.05),
            layers.RandomZoom(0.10),
            layers.RandomTranslation(height_factor=0.05, width_factor=0.05),
            layers.RandomContrast(0.10),
        ],
        name="data_augmentation",
    )


def create_model(image_size=config.IMAGE_SIZE) -> tf.keras.Model:
    """
    Build (but do not compile) the CNN.

    Data augmentation and rescaling live inside the model itself so that
    the same saved .keras file can accept raw 0-255 pixel images at
    inference time (e.g. from the Gradio app) without requiring callers
    to remember to normalize manually. Keras automatically disables the
    augmentation layers during inference (model.predict / model()
    with training=False).
    """
    data_augmentation = build_data_augmentation()

    model = models.Sequential(
        [
            layers.Input(shape=(image_size[0], image_size[1], 3)),

            data_augmentation,
            layers.Rescaling(1.0 / 255),

            layers.Conv2D(32, kernel_size=3, activation="relu"),
            layers.MaxPooling2D(),

            layers.Conv2D(64, kernel_size=3, activation="relu"),
            layers.MaxPooling2D(),

            layers.Conv2D(128, kernel_size=3, activation="relu"),
            layers.MaxPooling2D(),

            layers.GlobalAveragePooling2D(),

            layers.Dropout(config.DROPOUT_1),

            layers.Dense(64, activation="relu"),
            layers.Dropout(config.DROPOUT_2),

            layers.Dense(1, activation="sigmoid"),
        ],
        name="casting_defect_cnn",
    )

    return model


def compile_model(model: tf.keras.Model, learning_rate: float = config.LEARNING_RATE) -> tf.keras.Model:
    """
    Compile the model with binary cross-entropy loss, Adam optimizer,
    and accuracy/precision/recall metrics (all required for a
    quality-control system where false negatives matter).
    """
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
        ],
    )
    return model


def create_and_compile_model(image_size=config.IMAGE_SIZE, learning_rate=config.LEARNING_RATE) -> tf.keras.Model:
    """Convenience function combining create_model() and compile_model()."""
    model = create_model(image_size=image_size)
    model = compile_model(model, learning_rate=learning_rate)
    return model


if __name__ == "__main__":
    # Quick manual smoke test: python -m src.model
    cnn = create_and_compile_model()
    cnn.summary()
