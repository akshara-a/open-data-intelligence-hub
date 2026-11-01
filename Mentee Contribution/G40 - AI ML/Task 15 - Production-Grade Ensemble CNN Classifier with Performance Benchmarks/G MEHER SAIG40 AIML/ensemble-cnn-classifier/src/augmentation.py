import tensorflow as tf


def create_data_augmentation():
    """
    Data augmentation pipeline for training images.

    Augmentation is applied only to training data.
    """

    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip(
                mode="horizontal"
            ),

            tf.keras.layers.RandomRotation(
                factor=0.10
            ),

            tf.keras.layers.RandomZoom(
                height_factor=0.10,
                width_factor=0.10
            ),

            tf.keras.layers.RandomContrast(
                factor=0.10
            ),
        ],
        name="data_augmentation"
    )

    return augmentation


if __name__ == "__main__":

    augmentation = create_data_augmentation()

    print("Data augmentation pipeline created successfully!")
    print("-" * 50)

    for layer in augmentation.layers:
        print(f"{layer.name}: {layer.__class__.__name__}")