"""
Part 2 — Data Augmentation (Section 15).
Augmentation is applied ONLY to the training dataset — never to
validation or test data, per the guide's explicit rule.
"""

from tensorflow.keras import layers, Sequential

def get_augmentation_pipeline():
    """
    Returns a Keras preprocessing pipeline implementing:
    random horizontal flip, rotation, zoom, and brightness/contrast
    adjustment (Section 15's recommended list).
    """
    return Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),      # ~ +/-30 degrees
        layers.RandomZoom(0.1),
        layers.RandomTranslation(0.1, 0.1),  # approximates random crop
        layers.RandomBrightness(0.15),
        layers.RandomContrast(0.15),
    ], name="augmentation")


def augment_dataset(x_train, batch_size=32, shuffle_buffer=2000):
    """
    Wraps a numpy array of training images in a tf.data pipeline that
    applies augmentation on the fly (memory-efficient vs. augmenting
    the whole array up front).
    """
    import tensorflow as tf

    augmenter = get_augmentation_pipeline()
    ds = tf.data.Dataset.from_tensor_slices(x_train)
    ds = ds.shuffle(shuffle_buffer).map(
        lambda img: augmenter(img, training=True),
        num_parallel_calls=tf.data.AUTOTUNE
    )
    return ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)


"""
Why augmentation is useful (Part 2 required explanation):
Real production images vary in orientation, framing, lighting and
scale. Training only on 'clean' images causes the CNN to memorize
narrow visual conditions rather than the underlying object features.
Augmentation synthetically expands the training distribution so the
model learns to recognize objects despite flips, rotation, zoom and
lighting changes — improving generalization to unseen, imperfect
production images without collecting more data.
"""
