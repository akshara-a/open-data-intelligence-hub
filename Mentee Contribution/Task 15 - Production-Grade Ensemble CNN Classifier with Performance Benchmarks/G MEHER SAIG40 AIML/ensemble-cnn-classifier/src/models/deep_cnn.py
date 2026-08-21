import tensorflow as tf


def build_deep_cnn(
    input_shape=(32, 32, 3),
    num_classes=10
):
    """
    CNN 3 - Deep CNN

    A deeper CNN designed to learn more complex
    visual representations.

    Features:
    - Multiple convolutional layers
    - Batch Normalization
    - Max Pooling
    - Global Average Pooling
    - Dense classification layer
    """

    inputs = tf.keras.Input(
        shape=input_shape,
        name="input_image"
    )

    # ========================================================
    # BLOCK 1
    # ========================================================

    x = tf.keras.layers.Conv2D(
        32,
        (3, 3),
        padding="same",
        activation="relu"
    )(inputs)

    x = tf.keras.layers.Conv2D(
        32,
        (3, 3),
        padding="same",
        activation="relu"
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    )(x)

    # ========================================================
    # BLOCK 2
    # ========================================================

    x = tf.keras.layers.Conv2D(
        64,
        (3, 3),
        padding="same",
        activation="relu"
    )(x)

    x = tf.keras.layers.Conv2D(
        64,
        (3, 3),
        padding="same",
        activation="relu"
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    )(x)

    # ========================================================
    # BLOCK 3
    # ========================================================

    x = tf.keras.layers.Conv2D(
        128,
        (3, 3),
        padding="same",
        activation="relu"
    )(x)

    x = tf.keras.layers.Conv2D(
        128,
        (3, 3),
        padding="same",
        activation="relu"
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    )(x)

    # ========================================================
    # GLOBAL AVERAGE POOLING
    # ========================================================

    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    x = tf.keras.layers.Dense(
        128,
        activation="relu"
    )(x)

    x = tf.keras.layers.Dropout(
        0.40
    )(x)

    outputs = tf.keras.layers.Dense(
        num_classes,
        activation="softmax",
        name="class_output"
    )(x)

    # ========================================================
    # CREATE MODEL
    # ========================================================

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="deep_cnn"
    )

    return model


# ============================================================
# TEST MODEL
# ============================================================

if __name__ == "__main__":

    model = build_deep_cnn()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()