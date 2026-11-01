"""
preprocessing.py
================
Standardized image preprocessing and dataset tensor formatting.
Ensures image resizing (128x128), [0, 1] normalization, and categorical label encoding.
"""

import os
import numpy as np
from PIL import Image
from typing import Tuple, List, Union

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
IMAGE_SIZE = (128, 128)
CLASSES = ["cat", "dog"]
CLASS_TO_IDX = {"cat": 0, "dog": 1}
IDX_TO_CLASS = {0: "cat", 1: "dog"}


def preprocess_image(image_input: Union[str, Image.Image, np.ndarray], target_size: Tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
    """
    Standardizes any input image into normalized float32 tensor of shape (1, H, W, 3).
    Pixel values scaled to [0.0, 1.0].
    """
    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            raise FileNotFoundError(f"Image not found at path: {image_input}")
        img = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, np.ndarray):
        if image_input.dtype != np.uint8:
            image_input = (np.clip(image_input, 0, 1) * 255).astype(np.uint8)
        img = Image.fromarray(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        img = image_input.convert("RGB")
    else:
        raise ValueError("Unsupported image input type. Expected file path, PIL Image, or numpy array.")
        
    img = img.resize(target_size, Image.Resampling.BILINEAR)
    arr = np.array(img, dtype=np.float32) / 255.0
    
    # Add batch dimension if single image
    if len(arr.shape) == 3:
        arr = np.expand_dims(arr, axis=0)
        
    return arr


def load_dataset_split(split_name: str, target_size: Tuple[int, int] = IMAGE_SIZE) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Loads all images for a given split ('train', 'val', 'test').
    Returns:
        X: np.ndarray of shape (N, 128, 128, 3) in range [0, 1]
        y: np.ndarray of shape (N, 2) one-hot encoded
        filenames: List of original file paths
    """
    split_dir = os.path.join(DATA_DIR, split_name)
    if not os.path.exists(split_dir):
        raise FileNotFoundError(f"Split directory not found: {split_dir}. Please run data_loader.py first.")
        
    images = []
    labels = []
    file_paths = []
    
    for category in CLASSES:
        cat_dir = os.path.join(split_dir, category)
        if not os.path.exists(cat_dir):
            continue
        label_idx = CLASS_TO_IDX[category]
        
        for fname in sorted(os.listdir(cat_dir)):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                fpath = os.path.join(cat_dir, fname)
                img = Image.open(fpath).convert("RGB")
                img = img.resize(target_size, Image.Resampling.BILINEAR)
                arr = np.array(img, dtype=np.float32) / 255.0
                
                images.append(arr)
                labels.append(label_idx)
                file_paths.append(fpath)
                
    X = np.array(images, dtype=np.float32)
    y_int = np.array(labels, dtype=np.int32)
    
    # One-hot encode (N, 2)
    y_one_hot = np.zeros((len(y_int), 2), dtype=np.float32)
    for i, l in enumerate(y_int):
        y_one_hot[i, l] = 1.0
        
    return X, y_one_hot, file_paths


def load_full_dataset(target_size: Tuple[int, int] = IMAGE_SIZE):
    """
    Convenience method returning ((X_train, y_train), (X_val, y_val), (X_test, y_test)).
    """
    X_train, y_train, _ = load_dataset_split("train", target_size)
    X_val, y_val, _ = load_dataset_split("val", target_size)
    X_test, y_test, test_paths = load_dataset_split("test", target_size)
    return (X_train, y_train), (X_val, y_val), (X_test, y_test), test_paths


if __name__ == "__main__":
    (X_tr, y_tr), (X_v, y_v), (X_te, y_te), paths = load_full_dataset()
    print(f"X_train shape: {X_tr.shape}, y_train shape: {y_tr.shape}")
    print(f"X_val shape:   {X_v.shape}, y_val shape:   {y_v.shape}")
    print(f"X_test shape:  {X_te.shape}, y_test shape:  {y_te.shape}")
