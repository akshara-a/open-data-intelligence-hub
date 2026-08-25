"""
Shared utility functions: logging setup, reproducibility, and dataset
validation helpers used before training starts.
"""

import json
import logging
import os
import random
from pathlib import Path

import numpy as np

from src import config


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def get_logger(name: str = "casting_inspection") -> logging.Logger:
    """
    Return a configured logger that prints readable INFO-level messages,
    e.g. 'INFO: Loading dataset'.

    Calling this multiple times will not attach duplicate handlers.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = get_logger()


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
def set_global_seeds(seed: int = config.RANDOM_SEED) -> None:
    """
    Set Python, NumPy, and TensorFlow seeds so that dataset splitting,
    weight initialization, and augmentation are as reproducible as
    practical across runs.
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        # TensorFlow may not be installed yet when this is imported by
        # lightweight tooling (e.g. linting). Skip silently in that case.
        pass


# ---------------------------------------------------------------------------
# Dataset validation
# ---------------------------------------------------------------------------
class DatasetValidationError(Exception):
    """Raised when the dataset directory structure or contents are invalid."""


VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def _list_image_files(folder: Path) -> list:
    return [
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in VALID_IMAGE_EXTENSIONS
    ]


def validate_dataset_structure(
    train_dir: Path = config.TRAIN_DIR,
    test_dir: Path = config.TEST_DIR,
    class_folder_names: list = None,
) -> dict:
    """
    Validate that the dataset directories exist and contain images for
    both classes, in both the train and test splits.

    Returns a dictionary with per-folder image counts on success.
    Raises DatasetValidationError with a clear, beginner-friendly message
    on failure.
    """
    if class_folder_names is None:
        class_folder_names = config.CLASS_FOLDER_NAMES

    counts = {}

    for split_name, split_dir in (("train", train_dir), ("test", test_dir)):
        if not split_dir.exists():
            raise DatasetValidationError(
                f"The '{split_name}' dataset directory was not found at: "
                f"{split_dir}\n"
                f"Please create it and place your images inside, following "
                f"the structure described in the README."
            )

        for class_name in class_folder_names:
            class_dir = split_dir / class_name

            if not class_dir.exists():
                raise DatasetValidationError(
                    f"Expected class folder '{class_name}' was not found "
                    f"inside {split_dir}.\n"
                    f"Please make sure your dataset follows this structure:\n"
                    f"  data/{split_name}/ok_front/\n"
                    f"  data/{split_name}/def_front/"
                )

            images = _list_image_files(class_dir)

            if len(images) == 0:
                raise DatasetValidationError(
                    f"No image files were found in {class_dir}.\n"
                    f"Supported extensions: {sorted(VALID_IMAGE_EXTENSIONS)}"
                )

            counts[f"{split_name}/{class_name}"] = len(images)

    logger.info("Dataset validation passed.")
    for key, value in counts.items():
        logger.info("  %s: %d images", key, value)

    return counts


def check_images_openable(folder: Path, max_check: int = None) -> list:
    """
    Attempt to open every image (or the first `max_check` images) in a
    folder with Pillow to detect corrupted / unreadable files.

    Returns a list of paths that failed to open. An empty list means
    every checked image is readable.
    """
    from PIL import Image

    broken = []
    image_files = _list_image_files(folder)

    if max_check is not None:
        image_files = image_files[:max_check]

    for image_path in image_files:
        try:
            with Image.open(image_path) as img:
                img.verify()
        except Exception:
            broken.append(image_path)

    return broken


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------
def save_json(data: dict, path: Path) -> None:
    """Save a dictionary as pretty-printed JSON, creating parent dirs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info("Saved: %s", path)


def load_json(path: Path) -> dict:
    """Load a JSON file into a dictionary."""
    with open(path, "r") as f:
        return json.load(f)
