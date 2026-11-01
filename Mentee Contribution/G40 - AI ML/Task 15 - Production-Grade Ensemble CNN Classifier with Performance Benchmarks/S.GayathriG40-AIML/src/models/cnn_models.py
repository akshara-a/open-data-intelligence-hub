from tensorflow import keras
from tensorflow.keras import layers

from src.augmentation import create_augmentation


NUM_CLASSES = 10


def compile_model(model):

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def build_baseline_cnn():

    model = keras.Sequential([

        layers.Input(shape=(32, 32, 3)),

        create_augmentation(),

        layers.Conv2D(
            32,
            (3, 3),
            activation="relu",
            padding="same"
        ),

        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(
            64,
            (3, 3),
            activation="relu",
            padding="same"
        ),

        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),

        layers.Dense(
            128,
            activation="relu"
        ),

        layers.Dense(
            NUM_CLASSES,
            activation="softmax"
        )

    ])

    return compile_model(model)


def build_regularized_cnn():

    model = keras.Sequential([

        layers.Input(shape=(32, 32, 3)),

        create_augmentation(),

        layers.Conv2D(
            32,
            (3, 3),
            padding="same"
        ),

        layers.BatchNormalization(),

        layers.Activation("relu"),

        layers.MaxPooling2D((2, 2)),

        layers.Dropout(0.25),

        layers.Conv2D(
            64,
            (3, 3),
            padding="same"
        ),

        layers.BatchNormalization(),

        layers.Activation("relu"),

        layers.MaxPooling2D((2, 2)),

        layers.Dropout(0.30),

        layers.Conv2D(
            128,
            (3, 3),
            padding="same"
        ),

        layers.BatchNormalization(),

        layers.Activation("relu"),

        layers.MaxPooling2D((2, 2)),

        layers.Dropout(0.35),

        layers.Flatten(),

        layers.Dense(
            128,
            activation="relu"
        ),

        layers.Dropout(0.40),

        layers.Dense(
            NUM_CLASSES,
            activation="softmax"
        )

    ])

    return compile_model(model)


def build_deep_cnn():

    model = keras.Sequential([

        layers.Input(shape=(32, 32, 3)),

        create_augmentation(),

        layers.Conv2D(
            32,
            (3, 3),
            padding="same",
            activation="relu"
        ),

        layers.Conv2D(
            32,
            (3, 3),
            padding="same",
            activation="relu"
        ),

        layers.BatchNormalization(),

        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(
            64,
            (3, 3),
            padding="same",
            activation="relu"
        ),

        layers.Conv2D(
            64,
            (3, 3),
            padding="same",
            activation="relu"
        ),

        layers.BatchNormalization(),

        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(
            128,
            (3, 3),
            padding="same",
            activation="relu"
        ),

        layers.Conv2D(
            128,
            (3, 3),
            padding="same",
            activation="relu"
        ),

        layers.BatchNormalization(),

        layers.MaxPooling2D((2, 2)),

        layers.GlobalAveragePooling2D(),

        layers.Dense(
            128,
            activation="relu"
        ),

        layers.Dropout(0.35),

        layers.Dense(
            NUM_CLASSES,
            activation="softmax"
        )

    ])

    return compile_model(model)