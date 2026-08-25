#!/usr/bin/env python
"""
Casting Defect Detection - Lightweight Demo (No TensorFlow required)
This demonstrates the CNN architecture and data pipeline without training.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import os

print("\n" + "="*70)
print("🚀 CASTING DEFECT DETECTION SYSTEM - DEMO")
print("="*70)

# ============================================================================
# PART 1: DATASET OVERVIEW
# ============================================================================
print("\n1️⃣  DATASET OVERVIEW")
print("-" * 70)

data_path = Path("data/train")
ok_front_path = data_path / "ok_front"
def_front_path = data_path / "def_front"

ok_images = list(ok_front_path.glob("*"))
def_images = list(def_front_path.glob("*"))

print(f"✅ Non-defective images (ok_front): {len(ok_images)}")
print(f"❌ Defective images (def_front): {len(def_images)}")
print(f"📊 Total images: {len(ok_images) + len(def_images)}")

# Check balance
total = len(ok_images) + len(def_images)
ok_pct = (len(ok_images) / total) * 100
def_pct = (len(def_images) / total) * 100
print(f"\nClass Distribution:")
print(f"  Non-defective: {ok_pct:.1f}%")
print(f"  Defective: {def_pct:.1f}%")

# ============================================================================
# PART 2: SAMPLE IMAGE VISUALIZATION
# ============================================================================
print("\n2️⃣  LOADING SAMPLE IMAGES")
print("-" * 70)

fig, axes = plt.subplots(2, 3, figsize=(12, 8))
fig.suptitle("Sample Images from Dataset", fontsize=14, fontweight='bold')

# Show 3 non-defective and 3 defective
for i in range(3):
    img = Image.open(ok_images[i])
    axes[0, i].imshow(img)
    axes[0, i].set_title(f"Non-defective #{i+1}")
    axes[0, i].axis('off')
    print(f"  Loaded: {ok_images[i].name}")

for i in range(3):
    img = Image.open(def_images[i])
    axes[1, i].imshow(img)
    axes[1, i].set_title(f"Defective #{i+1}")
    axes[1, i].axis('off')
    print(f"  Loaded: {def_images[i].name}")

plt.tight_layout()
plt.savefig("reports/demo_samples.png", dpi=100, bbox_inches='tight')
print("\n✅ Saved: reports/demo_samples.png")
plt.show()

# ============================================================================
# PART 3: IMAGE PREPROCESSING PIPELINE
# ============================================================================
print("\n3️⃣  IMAGE PREPROCESSING PIPELINE")
print("-" * 70)

target_size = (224, 224)
print(f"Target image size: {target_size}")
print(f"Normalization: 0-255 → 0-1 range")
print(f"Data augmentation: Applied to training data only")

# Load and preprocess sample image
sample_img = Image.open(ok_images[0])
print(f"\nOriginal image shape: {sample_img.size}")

# Resize
resized = sample_img.resize(target_size)
print(f"Resized shape: {resized.size}")

# Convert to array and normalize
img_array = np.array(resized) / 255.0
print(f"Normalized pixel range: [{img_array.min():.3f}, {img_array.max():.3f}]")

# ============================================================================
# PART 4: CNN ARCHITECTURE DIAGRAM
# ============================================================================
print("\n4️⃣  CNN ARCHITECTURE")
print("-" * 70)

architecture = """
INPUT LAYER
    ↓ (224×224×3 RGB image)
DATA AUGMENTATION
    ↓ (horizontal flip, rotation, zoom, translation, contrast)
NORMALIZATION
    ↓ (divide by 255)
CONVOLUTION BLOCK 1
    ├─ Conv2D (32 filters, 3×3 kernel, ReLU)
    └─ MaxPooling2D (2×2)
CONVOLUTION BLOCK 2
    ├─ Conv2D (64 filters, 3×3 kernel, ReLU)
    └─ MaxPooling2D (2×2)
CONVOLUTION BLOCK 3
    ├─ Conv2D (128 filters, 3×3 kernel, ReLU)
    └─ MaxPooling2D (2×2)
GLOBAL AVERAGE POOLING
    ↓ (reduce to 128 values)
DROPOUT (40%)
DENSE LAYER (64 units, ReLU)
DROPOUT (30%)
OUTPUT LAYER
    ↓ (Sigmoid activation)
BINARY PREDICTION (0.0 → 1.0)
    ├─ < 0.5 = Non-defective (0)
    └─ ≥ 0.5 = Defective (1)
"""

print(architecture)

# ============================================================================
# PART 5: DATA AUGMENTATION PREVIEW
# ============================================================================
print("\n5️⃣  DATA AUGMENTATION TECHNIQUES")
print("-" * 70)
print("✅ Horizontal Flip    - Simulates viewing from opposite angle")
print("✅ Random Rotation    - Small rotations (±5%)")
print("✅ Random Zoom        - Camera closer/farther (±10%)")
print("✅ Random Translation - Off-center positioning (±5%)")
print("✅ Contrast Adjust    - Lighting variations (±10%)")

# ============================================================================
# PART 6: TRAINING CONFIGURATION
# ============================================================================
print("\n6️⃣  TRAINING CONFIGURATION")
print("-" * 70)
config = {
    "Optimizer": "Adam (learning_rate=0.001)",
    "Loss Function": "Binary Cross-Entropy",
    "Batch Size": 32,
    "Epochs": 25,
    "Train/Val/Test Split": "70% / 10% / 20%",
    "Regularization": "Dropout + Early Stopping + LR Reduction",
    "Metrics": "Accuracy, Precision, Recall"
}

for key, value in config.items():
    print(f"  {key:<25} : {value}")

# ============================================================================
# PART 7: EVALUATION METRICS
# ============================================================================
print("\n7️⃣  EVALUATION METRICS (What to Expect)")
print("-" * 70)
print("📊 Accuracy")
print("   Total correct predictions / Total predictions")
print()
print("🎯 Precision")
print("   Of all predicted defects, how many were actually defective?")
print("   High precision = fewer good products rejected")
print()
print("🔍 Recall")
print("   Of all actual defects, how many did we catch?")
print("   High recall = fewer defects slip through")
print()
print("⚠️  False Negatives (Most Important!)")
print("   Defective products marked as good → CRITICAL RISK")
print()
print("📉 Confusion Matrix")
print("            Predicted")
print("         Good  Defective")
print("Actual")
print("Good     TN      FP")
print("Defect   FN      TP")

# ============================================================================
# PART 8: NEXT STEPS
# ============================================================================
print("\n8️⃣  NEXT STEPS TO TRAIN THE MODEL")
print("-" * 70)
print("""
🚀 TO RUN FULL TRAINING:

Option A - Google Colab (Recommended):
   1. Go to: https://colab.research.google.com
   2. Upload: notebooks/casting_defect_detection.ipynb
   3. Run all cells (Colab has TensorFlow pre-installed)

Option B - Local with Python 3.11/3.12:
   1. pip install -r requirements.txt
   2. python -m jupyter notebook notebooks/casting_defect_detection.ipynb
   3. Run all cells

Option C - Command line training (if TensorFlow installed):
   1. python train_model.py

📊 Expected Results:
   - Test Accuracy: 90-95%
   - Training Time: 10-30 minutes (GPU faster)
   - Model saved to: models/best_casting_defect_model.keras
""")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✅ DEMO COMPLETE")
print("="*70)
print(f"""
Dataset Status: ✅ READY ({len(ok_images) + len(def_images)} images)
  ├─ Non-defective: {len(ok_images)} images
  └─ Defective: {len(def_images)} images

Files Created:
  ✅ reports/demo_samples.png (sample visualization)

To start training, visit Google Colab or follow Option B above.
""")
print("="*70 + "\n")
