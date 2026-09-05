"""
preprocessing.py

Shared preprocessing utilities. Rescaling itself is baked into each model
(see src/models/*.py, first layer after augmentation), so this module holds
the pieces that are useful outside the model graph — e.g. for inspecting or
sanity-checking raw arrays before they hit the pipeline.
"""

import numpy as np


def rescale(images):
    """Scale uint8 images in [0, 255] to float32 in [0, 1]."""
    return images.astype(np.float32) / 255.0


def summarize(images, labels, class_names):
    """Print a quick shape/class-balance summary of a loaded split."""
    print(f"images: {images.shape}, dtype={images.dtype}")
    print(f"labels: {labels.shape}, dtype={labels.dtype}")
    counts = np.bincount(labels, minlength=len(class_names))
    for name, count in zip(class_names, counts):
        print(f"  {name:12s}: {count}")
