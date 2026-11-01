import tensorflow as tf


def build_regularized_cnn(
    input_shape=(32, 32, 3),
    num_classes=10
):
    """
    CNN 2 - Regularized CNN

    Features:
    - Batch Normalization
    - Dropout
    - Three convolutional blocks
    - Global Average Pooling
    """

    inputs = tf.keras.Input(
        shape=input_shape,
        name="input_image"
    )

    # --------------------------------------------------------
    # Block 1
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        32,
        (3, 3),
        padding="same",
        use_bias=False
    )(inputs)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    )(x)

    x = tf.keras.layers.Dropout(
        0.20
    )(x)

    # --------------------------------------------------------
    # Block 2
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        64,
        (3, 3),
        padding="same",
        use_bias=False
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    )(x)

    x = tf.keras.layers.Dropout(
        0.25
    )(x)

    # --------------------------------------------------------
    # Block 3
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        128,
        (3, 3),
        padding="same",
        use_bias=False
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    )(x)

    x = tf.keras.layers.Dropout(
        0.30
    )(x)

    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------

    x = tf.keras.layers.GlobalAveragePooling2D()(x)

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

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="regularized_cnn"
    )

    return model


# ============================================================
# Test Model
# ============================================================

if __name__ == "__main__":

    model = build_regularized_cnn()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()