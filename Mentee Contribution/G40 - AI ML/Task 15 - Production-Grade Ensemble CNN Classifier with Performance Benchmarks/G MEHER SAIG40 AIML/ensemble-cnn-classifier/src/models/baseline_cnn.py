import tensorflow as tf


def build_baseline_cnn(input_shape=(32, 32, 3), num_classes=10):
    """
    Build the baseline CNN model.

    Architecture:
    Input
      ↓
    Conv2D
      ↓
    ReLU
      ↓
    MaxPooling
      ↓
    Conv2D
      ↓
    ReLU
      ↓
    MaxPooling
      ↓
    Flatten
      ↓
    Dense
      ↓
    Output
    """

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=input_shape),

            # First convolution block
            tf.keras.layers.Conv2D(
                32,
                (3, 3),
                activation="relu",
                padding="same"
            ),
            tf.keras.layers.MaxPooling2D(
                pool_size=(2, 2)
            ),

            # Second convolution block
            tf.keras.layers.Conv2D(
                64,
                (3, 3),
                activation="relu",
                padding="same"
            ),
            tf.keras.layers.MaxPooling2D(
                pool_size=(2, 2)
            ),

            # Classification layers
            tf.keras.layers.Flatten(),

            tf.keras.layers.Dense(
                128,
                activation="relu"
            ),

            tf.keras.layers.Dense(
                num_classes,
                activation="softmax"
            )
        ],
        name="baseline_cnn"
    )

    return model


if __name__ == "__main__":

    model = build_baseline_cnn()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()