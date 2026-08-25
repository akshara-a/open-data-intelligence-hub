"""
Dataset loading utilities.

Loads casting product images from the `data/train` and `data/test`
directories into tf.data.Dataset objects ready for training and
evaluation, with an explicit, non-alphabetical class mapping:

    ok_front  -> 0 -> Non-defective
    def_front -> 1 -> Defective
"""

import tensorflow as tf

from src import config
from src.utils import get_logger, validate_dataset_structure

logger = get_logger(__name__)


def load_train_validation_test_datasets(
    train_dir=config.TRAIN_DIR,
    test_dir=config.TEST_DIR,
    image_size=config.IMAGE_SIZE,
    batch_size=config.BATCH_SIZE,
    validation_split=config.VALIDATION_SPLIT,
    seed=config.RANDOM_SEED,
    validate_first: bool = True,
):
    """
    Build the training, validation, and test tf.data.Dataset objects.

    - The TRAIN directory is split 80/20 into training and validation
      using a fixed seed, so the split is reproducible.
    - The TEST directory is loaded separately and is NEVER used for
      training or validation. It is also not shuffled, so predictions
      line up with the true labels index-for-index during evaluation.
    - class_names is passed explicitly (rather than relying on
      alphabetical folder ordering) so `ok_front` is always label 0
      and `def_front` is always label 1.

    Returns
    -------
    (train_dataset, validation_dataset, test_dataset)
    """
    if validate_first:
        validate_dataset_structure(train_dir, test_dir)

    class_names = config.CLASS_FOLDER_NAMES

    logger.info("Loading training dataset from: %s", train_dir)
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        class_names=class_names,
        validation_split=validation_split,
        subset="training",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="binary",
        shuffle=True,
    )

    logger.info("Loading validation dataset from: %s", train_dir)
    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        class_names=class_names,
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="binary",
        shuffle=True,
    )

    logger.info("Loading test dataset from: %s", test_dir)
    test_dataset = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        class_names=class_names,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="binary",
        shuffle=False,  # keep order aligned with labels for evaluation
    )

    logger.info(
        "Class mapping enforced: %s -> 0 (Non-defective), %s -> 1 (Defective)",
        class_names[0],
        class_names[1],
    )

    # Improve pipeline throughput: overlap data loading with model execution.
    autotune = tf.data.AUTOTUNE
    train_dataset = train_dataset.cache().prefetch(autotune)
    validation_dataset = validation_dataset.cache().prefetch(autotune)
    test_dataset = test_dataset.cache().prefetch(autotune)

    return train_dataset, validation_dataset, test_dataset


if __name__ == "__main__":
    # Quick manual smoke test: python -m src.data_loader
    train_ds, val_ds, test_ds = load_train_validation_test_datasets()
    logger.info("Train batches: %d", tf.data.experimental.cardinality(train_ds).numpy())
    logger.info("Validation batches: %d", tf.data.experimental.cardinality(val_ds).numpy())
    logger.info("Test batches: %d", tf.data.experimental.cardinality(test_ds).numpy())
