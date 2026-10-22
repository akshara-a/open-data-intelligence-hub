import tensorflow as tf
from tensorflow.keras import layers, models


# ============================================================
# CNN 1 - BASELINE CNN
# ============================================================

def build_baseline_cnn(input_shape=(32, 32, 3), num_classes=10):

    model = models.Sequential([
        layers.Input(shape=input_shape),

        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),

        layers.Dense(128, activation="relu"),

        layers.Dense(num_classes, activation="softmax")
    ], name="baseline_cnn")

    return model


# ============================================================
# CNN 2 - REGULARIZED CNN
# Batch Normalization + Dropout
# ============================================================

def build_regularized_cnn(input_shape=(32, 32, 3), num_classes=10):

    model = models.Sequential([
        layers.Input(shape=input_shape),

        layers.Conv2D(32, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        layers.Conv2D(64, (3, 3), padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.30),

        layers.Flatten(),

        layers.Dense(128, activation="relu"),
        layers.Dropout(0.40),

        layers.Dense(num_classes, activation="softmax")
    ], name="regularized_cnn")

    return model


# ============================================================
# CNN 3 - DEEPER CNN
# ============================================================

def build_deep_cnn(input_shape=(32, 32, 3), num_classes=10):

    model = models.Sequential([
        layers.Input(shape=input_shape),

        # Block 1
        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Block 2
        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Block 3
        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),

        layers.GlobalAveragePooling2D(),

        layers.Dense(128, activation="relu"),

        layers.Dense(num_classes, activation="softmax")
    ], name="deep_cnn")

    return model


# ============================================================
# TEST MODELS
# ============================================================

if __name__ == "__main__":

    model1 = build_baseline_cnn()
    model2 = build_regularized_cnn()
    model3 = build_deep_cnn()

    print("\n" + "=" * 60)
    print("CNN 1 - BASELINE")
    print("=" * 60)
    model1.summary()

    print("\n" + "=" * 60)
    print("CNN 2 - REGULARIZED")
    print("=" * 60)
    model2.summary()

    print("\n" + "=" * 60)
    print("CNN 3 - DEEP")
    print("=" * 60)
    model3.summary()