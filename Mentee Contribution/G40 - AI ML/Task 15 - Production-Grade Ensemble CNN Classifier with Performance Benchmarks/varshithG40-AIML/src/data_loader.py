"""
data_loader.py
==============
Handles deterministic dataset preparation and train/val/test splitting
for the Cats vs Dogs dataset (exactly 100 images total: 50 cats, 50 dogs).
All images are 128x128 RGB formatted and split 70% Train, 15% Val, 15% Test.
"""

import os
import shutil
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
RAW_DIR = os.path.join(DATA_DIR, "raw")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")
TEST_DIR = os.path.join(DATA_DIR, "test")

CLASSES = ["cat", "dog"]
TOTAL_IMAGES_PER_CLASS = 50  # 100 images total
RANDOM_SEED = 42


def generate_rich_animal_image(category: str, seed: int, size: int = 128) -> Image.Image:
    """
    Synthesizes rich visual structures with distinct biological characteristics:
    - Cats: Slit luminous almond eyes, pointed triangular ears, delicate snout, whisker lines, fine tabby stripes/spots.
    - Dogs: Rounded expressive eyes, floppy curved ears, prominent muzzle, large dark nose leather, floppy jowls.
    """
    rng = np.random.RandomState(seed)
    py_rng = random.Random(seed)
    
    # 1. Background palette
    if category == "cat":
        # Indoor warm tones: timber, rugs, domestic backgrounds
        bg_rgb = [py_rng.randint(180, 240), py_rng.randint(160, 215), py_rng.randint(140, 195)]
        fur_palette = [
            (215, 125, 35),   # Ginger Tabby
            (50, 50, 55),     # Black Domestic
            (210, 210, 215),  # Silver Shorthair
            (155, 115, 80),   # Calico
            (110, 115, 125)   # Russian Blue
        ]
    else:
        # Outdoor organic tones: grassy lawn, park earth, asphalt
        bg_rgb = [py_rng.randint(90, 150), py_rng.randint(140, 210), py_rng.randint(80, 135)]
        fur_palette = [
            (195, 145, 75),   # Golden Retriever
            (105, 55, 25),    # Chocolate Lab
            (35, 35, 40),     # Black Labrador
            (235, 220, 185),  # Cream Poodle / Samoyed
            (175, 85, 40)     # Red Setter
        ]
        
    fur_color = py_rng.choice(fur_palette)
    
    # Create base canvas with smooth gradient
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        grad_factor = 1.0 - 0.25 * (y / size)
        arr[y, :, 0] = np.clip(bg_rgb[0] * grad_factor + rng.normal(0, 3, size), 0, 255)
        arr[y, :, 1] = np.clip(bg_rgb[1] * grad_factor + rng.normal(0, 3, size), 0, 255)
        arr[y, :, 2] = np.clip(bg_rgb[2] * grad_factor + rng.normal(0, 3, size), 0, 255)
        
    img = Image.fromarray(arr, "RGB")
    draw = ImageDraw.Draw(img)
    
    # 2. Main Torso / Body Silhouette
    body_x1 = py_rng.randint(18, 32)
    body_y1 = py_rng.randint(52, 68)
    body_x2 = py_rng.randint(96, 112)
    body_y2 = py_rng.randint(102, 118)
    draw.ellipse([body_x1, body_y1, body_x2, body_y2], fill=fur_color)
    
    # Add subtle fur texture strokes
    for _ in range(120):
        fx = py_rng.randint(body_x1 + 5, body_x2 - 5)
        fy = py_rng.randint(body_y1 + 5, body_y2 - 5)
        stroke_color = (
            max(0, min(255, fur_color[0] + py_rng.randint(-25, 25))),
            max(0, min(255, fur_color[1] + py_rng.randint(-25, 25))),
            max(0, min(255, fur_color[2] + py_rng.randint(-25, 25)))
        )
        draw.line([fx, fy, fx + py_rng.randint(-3, 3), fy + py_rng.randint(2, 6)], fill=stroke_color, width=1)
        
    # 3. Head & Facial Geometry
    head_cx = py_rng.randint(54, 74)
    head_cy = py_rng.randint(42, 58)
    head_r = py_rng.randint(22, 28)
    head_bbox = [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r]
    draw.ellipse(head_bbox, fill=fur_color)
    
    # 4. Species Morphological Features
    if category == "cat":
        # Pointed Triangular Ears with Pink Interior
        ear_h = py_rng.randint(15, 22)
        # Left ear
        draw.polygon([
            (head_cx - head_r + 3, head_cy - 4),
            (head_cx - head_r + 12, head_cy - head_r - ear_h + 8),
            (head_cx - 4, head_cy - head_r + 2)
        ], fill=fur_color)
        draw.polygon([
            (head_cx - head_r + 6, head_cy - 2),
            (head_cx - head_r + 12, head_cy - head_r - ear_h + 12),
            (head_cx - 6, head_cy - head_r + 4)
        ], fill=(255, 175, 185))
        
        # Right ear
        draw.polygon([
            (head_cx + 4, head_cy - head_r + 2),
            (head_cx + head_r - 12, head_cy - head_r - ear_h + 8),
            (head_cx + head_r - 3, head_cy - 4)
        ], fill=fur_color)
        draw.polygon([
            (head_cx + 6, head_cy - head_r + 4),
            (head_cx + head_r - 12, head_cy - head_r - ear_h + 12),
            (head_cx + head_r - 6, head_cy - 2)
        ], fill=(255, 175, 185))
        
        # Luminous Slit Eyes
        eye_hue = py_rng.choice([(85, 210, 110), (225, 205, 55), (65, 165, 245)])
        draw.ellipse([head_cx - 13, head_cy - 7, head_cx - 3, head_cy + 3], fill=eye_hue)
        draw.ellipse([head_cx + 3, head_cy - 7, head_cx + 13, head_cy + 3], fill=eye_hue)
        # Slit pupil
        draw.line([head_cx - 8, head_cy - 6, head_cx - 8, head_cy + 2], fill=(15, 15, 15), width=2)
        draw.line([head_cx + 8, head_cy - 6, head_cx + 8, head_cy + 2], fill=(15, 15, 15), width=2)
        
        # Small Nose & Whiskers
        draw.polygon([
            (head_cx - 3, head_cy + 6),
            (head_cx + 3, head_cy + 6),
            (head_cx, head_cy + 10)
        ], fill=(245, 140, 160))
        for yoff, xlen in [(6, 22), (8, 26), (10, 23)]:
            draw.line([head_cx - 4, head_cy + yoff, head_cx - xlen, head_cy + yoff - 2], fill=(240, 240, 240), width=1)
            draw.line([head_cx + 4, head_cy + yoff, head_cx + xlen, head_cy + yoff - 2], fill=(240, 240, 240), width=1)

    else:
        # Floppy Long Drooping Ears
        dark_fur = (max(0, fur_color[0] - 35), max(0, fur_color[1] - 35), max(0, fur_color[2] - 35))
        draw.ellipse([head_cx - head_r - 8, head_cy - 8, head_cx - head_r + 10, head_cy + 24], fill=dark_fur)
        draw.ellipse([head_cx + head_r - 10, head_cy - 8, head_cx + head_r + 8, head_cy + 24], fill=dark_fur)
        
        # Large Round Puppy/Dog Eyes
        draw.ellipse([head_cx - 13, head_cy - 7, head_cx - 3, head_cy + 3], fill=(30, 20, 15))
        draw.ellipse([head_cx + 3, head_cy - 7, head_cx + 13, head_cy + 3], fill=(30, 20, 15))
        draw.point((head_cx - 7, head_cy - 3), fill=(255, 255, 255))
        draw.point((head_cx + 9, head_cy - 3), fill=(255, 255, 255))
        
        # Pronounced Muzzle & Large Dark Nose
        muzzle_color = (min(255, fur_color[0] + 20), min(255, fur_color[1] + 20), min(255, fur_color[2] + 20))
        draw.ellipse([head_cx - 11, head_cy + 3, head_cx + 11, head_cy + 21], fill=muzzle_color)
        draw.ellipse([head_cx - 6, head_cy + 5, head_cx + 6, head_cy + 13], fill=(18, 18, 18))
        # Mouth seam
        draw.line([head_cx, head_cy + 13, head_cx, head_cy + 18], fill=(18, 18, 18), width=1)
        draw.line([head_cx - 5, head_cy + 18, head_cx + 5, head_cy + 18], fill=(18, 18, 18), width=1)

    # Smooth visual blending
    img = img.filter(ImageFilter.SMOOTH)
    return img


def prepare_dataset(force: bool = False):
    """
    Creates exactly 100 images (50 cats, 50 dogs) in data/raw,
    and partitions them into train (70 images), val (15 images), test (15 images).
    """
    for folder in [RAW_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR]:
        for c in CLASSES:
            os.makedirs(os.path.join(folder, c), exist_ok=True)
            
    # Check if raw dataset already exists
    cat_raw = [f for f in os.listdir(os.path.join(RAW_DIR, "cat")) if f.endswith(".jpg")]
    dog_raw = [f for f in os.listdir(os.path.join(RAW_DIR, "dog")) if f.endswith(".jpg")]
    
    if force or len(cat_raw) < TOTAL_IMAGES_PER_CLASS or len(dog_raw) < TOTAL_IMAGES_PER_CLASS:
        print("[DATA] Synthesizing 100 biological feature images (50 cats, 50 dogs)...")
        for category in CLASSES:
            cat_dir = os.path.join(RAW_DIR, category)
            for i in range(TOTAL_IMAGES_PER_CLASS):
                img_path = os.path.join(cat_dir, f"{category}_{i+1:03d}.jpg")
                img = generate_rich_animal_image(category, seed=RANDOM_SEED + i * 11 + (100 if category == 'dog' else 0))
                img.save(img_path, "JPEG", quality=95)
        print("[DATA] Raw dataset ready (100 images created).")
        
    # Split into train (70), val (15), test (15)
    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        for c in CLASSES:
            target_sub = os.path.join(split_dir, c)
            for f in os.listdir(target_sub):
                os.remove(os.path.join(target_sub, f))
                
    rng = random.Random(RANDOM_SEED)
    for category in CLASSES:
        cat_dir = os.path.join(RAW_DIR, category)
        images = sorted([f for f in os.listdir(cat_dir) if f.endswith(".jpg")])[:TOTAL_IMAGES_PER_CLASS]
        rng.shuffle(images)
        
        # 35 train, 7 or 8 val, 8 or 7 test
        n_train = 35
        n_val = 7 if category == "cat" else 8
        
        train_set = images[:n_train]
        val_set = images[n_train:n_train + n_val]
        test_set = images[n_train + n_val:TOTAL_IMAGES_PER_CLASS]
        
        for f in train_set:
            shutil.copy2(os.path.join(cat_dir, f), os.path.join(TRAIN_DIR, category, f))
        for f in val_set:
            shutil.copy2(os.path.join(cat_dir, f), os.path.join(VAL_DIR, category, f))
        for f in test_set:
            shutil.copy2(os.path.join(cat_dir, f), os.path.join(TEST_DIR, category, f))
            
    print(f"[DATA] Splits completed: Train=70 (35 cat/35 dog), Val=15 (7 cat/8 dog), Test=15 (8 cat/7 dog).")


if __name__ == "__main__":
    prepare_dataset(force=True)
