import tensorflow as tf
from .config import IMAGE_SIZE, BATCH_SIZE, SEED


def decode_and_resize(path, label):
    image_bytes = tf.io.read_file(path)

    image = tf.io.decode_image(
        image_bytes,
        channels=3,
        expand_animations=False
    )

    image.set_shape([None, None, 3])

    image = tf.image.resize(
        image,
        IMAGE_SIZE,
        antialias=True
    )

    # Normalize pixel values to approximately 0.0 - 1.0
    image = tf.cast(image, tf.float32) / 255.0

    # Clip tiny floating-point values outside the range
    image = tf.clip_by_value(image, 0.0, 1.0)

    return image, tf.cast(label, tf.int32)


def build_dataset(df, training=False):
    paths = df["path"].astype(str).to_numpy()
    labels = df["label"].astype("int32").to_numpy()

    ds = tf.data.Dataset.from_tensor_slices((paths, labels))

    if training:
        ds = ds.shuffle(
            buffer_size=len(df),
            seed=SEED,
            reshuffle_each_iteration=True
        )

    ds = ds.map(
        decode_and_resize,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    ds = ds.batch(
        BATCH_SIZE,
        drop_remainder=False
    )

    ds = ds.prefetch(tf.data.AUTOTUNE)

    return ds


def sanity_check_dataset(ds, expected_classes=6):
    images, labels = next(iter(ds.take(1)))

    min_value = float(tf.reduce_min(images))
    max_value = float(tf.reduce_max(images))
    min_label = int(tf.reduce_min(labels))
    max_label = int(tf.reduce_max(labels))

    print("Sanity check:")
    print("  Image batch shape:", images.shape)
    print("  Image range:", min_value, "to", max_value)
    print(
        "  Labels in first batch:",
        sorted(set(labels.numpy().tolist()))
    )

    # Check RGB channels
    if images.shape[-1] != 3:
        raise RuntimeError(
            f"Expected 3-channel RGB images, but found "
            f"{images.shape[-1]} channels."
        )

    # Check image normalization with floating-point tolerance
    if min_value < -1e-5 or max_value > 1.00001:
        raise RuntimeError(
            f"Images are not correctly normalized. "
            f"Range found: {min_value} to {max_value}"
        )

    # Check labels
    if min_label < 0 or max_label >= expected_classes:
        raise RuntimeError(
            f"Invalid class labels found. "
            f"Expected labels from 0 to {expected_classes - 1}, "
            f"but found range {min_label} to {max_label}."
        )

    print("  Dataset sanity check passed successfully.")