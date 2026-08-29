import tensorflow as tf


def preprocess_dataset(dataset):
    """
    Normalize image pixel values from [0, 255] to [0, 1].
    """

    normalization = tf.keras.layers.Rescaling(1.0 / 255.0)

    return dataset.map(
        lambda images, labels: (
            normalization(images),
            labels
        ),
        num_parallel_calls=tf.data.AUTOTUNE,
    ).prefetch(tf.data.AUTOTUNE)