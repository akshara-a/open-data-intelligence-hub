from pathlib import Path
import tensorflow as tf


IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_datasets():
    """Load train, validation and test datasets."""

    train_dir = DATA_DIR / "train"
    validation_dir = DATA_DIR / "validation"
    test_dir = DATA_DIR / "test"

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_names=["def_front", "ok_front"],
        shuffle=True,
        seed=SEED,
    )

    validation_ds = tf.keras.utils.image_dataset_from_directory(
        validation_dir,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_names=["def_front", "ok_front"],
        shuffle=False,
    )

    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_names=["def_front", "ok_front"],
        shuffle=False,
    )

    return train_ds, validation_ds, test_ds


def optimize_dataset(ds):
    """Optimize TensorFlow dataset performance."""
    return ds.cache().prefetch(tf.data.AUTOTUNE)


if __name__ == "__main__":
    train_ds, validation_ds, test_ds = load_datasets()

    print("\nClass names:")
    print(train_ds.class_names)

    print("\nDataset loaded successfully.")

    train_ds = optimize_dataset(train_ds)
    validation_ds = optimize_dataset(validation_ds)
    test_ds = optimize_dataset(test_ds)

    print("Datasets optimized with cache + prefetch.")