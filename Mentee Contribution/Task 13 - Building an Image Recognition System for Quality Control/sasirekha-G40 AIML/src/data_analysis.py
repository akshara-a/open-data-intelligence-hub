"""
Dataset exploration helpers used by notebooks/01_data_exploration.ipynb.

Keeping these as reusable functions (rather than inline notebook code)
keeps the notebook clean and presentation-ready, while the actual
production training pipeline still lives entirely in src/train.py.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

from src import config
from src.utils import check_images_openable, get_logger

logger = get_logger(__name__)

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def count_images_per_class(split_dir: Path, class_folder_names=None) -> dict:
    """Count image files in each class subfolder of a split directory."""
    if class_folder_names is None:
        class_folder_names = config.CLASS_FOLDER_NAMES

    counts = {}
    for class_name in class_folder_names:
        class_dir = split_dir / class_name
        if not class_dir.exists():
            counts[class_name] = 0
            continue
        counts[class_name] = len(
            [f for f in class_dir.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS]
        )
    return counts


def summarize_dataset() -> dict:
    """
    Return image counts for train/ok_front, train/def_front,
    test/ok_front, test/def_front, plus totals.
    """
    train_counts = count_images_per_class(config.TRAIN_DIR)
    test_counts = count_images_per_class(config.TEST_DIR)

    summary = {
        "train": train_counts,
        "test": test_counts,
        "train_total": sum(train_counts.values()),
        "test_total": sum(test_counts.values()),
    }
    return summary


def plot_class_distribution(summary: dict, save_path: Path = None):
    """Bar chart of image counts per class, per split."""
    splits = ["train", "test"]
    class_names = config.CLASS_FOLDER_NAMES

    fig, ax = plt.subplots(figsize=(7, 5))
    width = 0.35
    x = range(len(class_names))

    for i, split in enumerate(splits):
        counts = [summary[split].get(c, 0) for c in class_names]
        ax.bar([xi + i * width for xi in x], counts, width, label=split)

    ax.set_xticks([xi + width / 2 for xi in x])
    ax.set_xticklabels(class_names)
    ax.set_ylabel("Image count")
    ax.set_title("Class Distribution (Train vs. Test)")
    ax.legend()
    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200)
        logger.info("Saved: %s", save_path)

    return fig


def get_sample_image_paths(class_name: str, split: str = "train", n: int = 5) -> list:
    """Return up to n image file paths for a given class/split."""
    split_dir = config.TRAIN_DIR if split == "train" else config.TEST_DIR
    class_dir = split_dir / class_name

    if not class_dir.exists():
        return []

    files = [f for f in class_dir.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS]
    return files[:n]


def plot_sample_images(class_name: str, split: str = "train", n: int = 5, save_path: Path = None):
    """Display (and optionally save) a row of sample images for a class."""
    paths = get_sample_image_paths(class_name, split=split, n=n)

    if not paths:
        logger.info("No images found for class '%s' in split '%s'.", class_name, split)
        return None

    fig, axes = plt.subplots(1, len(paths), figsize=(3 * len(paths), 3))
    if len(paths) == 1:
        axes = [axes]

    for ax, path in zip(axes, paths):
        img = Image.open(path)
        ax.imshow(img)
        ax.set_title(path.name, fontsize=8)
        ax.axis("off")

    fig.suptitle(f"{split} / {class_name}")
    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200)
        logger.info("Saved: %s", save_path)

    return fig


def get_image_dimensions_sample(class_name: str, split: str = "train", n: int = 20) -> list:
    """Return (width, height) tuples for a sample of images in a class."""
    paths = get_sample_image_paths(class_name, split=split, n=n)
    dimensions = []
    for path in paths:
        try:
            with Image.open(path) as img:
                dimensions.append(img.size)
        except Exception:
            continue
    return dimensions


def find_corrupted_images(split: str = "train", class_folder_names=None) -> dict:
    """
    Check every image in every class of a split for corruption using
    Pillow's verify(). Returns {class_name: [broken_paths]}.
    """
    if class_folder_names is None:
        class_folder_names = config.CLASS_FOLDER_NAMES

    split_dir = config.TRAIN_DIR if split == "train" else config.TEST_DIR
    results = {}

    for class_name in class_folder_names:
        class_dir = split_dir / class_name
        if not class_dir.exists():
            results[class_name] = []
            continue
        results[class_name] = check_images_openable(class_dir)

    return results
