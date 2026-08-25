#!/usr/bin/env python
"""
Quick Start Script - Test Data Loading Without TensorFlow
This script validates your dataset structure and displays sample images.
"""

import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from pathlib import Path

# Configuration
data_path = Path("data")
train_path = data_path / "train"

def check_dataset_structure():
    """Check if dataset is properly organized."""
    print("=" * 60)
    print("CHECKING DATASET STRUCTURE")
    print("=" * 60)
    
    if not train_path.exists():
        print(f"❌ ERROR: {train_path} not found!")
        print("   Please download dataset from Kaggle and extract to 'data/train' folder")
        return False
    
    classes = ["ok_front", "def_front"]
    total_images = 0
    
    for class_name in classes:
        class_path = train_path / class_name
        if class_path.exists():
            images = list(class_path.glob("*"))
            count = len(images)
            total_images += count
            print(f"✅ {class_name}: {count} images")
        else:
            print(f"❌ {class_name}: NOT FOUND")
    
    print(f"\nTotal training images: {total_images}")
    print("=" * 60)
    return total_images > 0

def display_sample_images():
    """Display sample images from each class."""
    print("\nDisplaying sample images...\n")
    
    classes = ["ok_front", "def_front"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    for idx, class_name in enumerate(classes):
        class_path = train_path / class_name
        images = list(class_path.glob("*"))
        
        if images:
            # Load first image
            img_path = images[0]
            img = Image.open(img_path)
            
            # Display
            axes[idx].imshow(img)
            axes[idx].set_title(f"{class_name}\n({len(images)} total images)")
            axes[idx].axis("off")
    
    plt.tight_layout()
    plt.savefig("reports/dataset_samples.png", dpi=100, bbox_inches='tight')
    print("✅ Sample images saved to: reports/dataset_samples.png")
    plt.show()

def main():
    print("\n")
    print("🚀 CASTING DEFECT DETECTION - QUICK START")
    print("\n")
    
    # Check dataset
    if not check_dataset_structure():
        print("\n⚠️  NEXT STEPS:")
        print("1. Download: https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product")
        print("2. Extract to: data/train/ and data/test/")
        print("3. Folder structure:")
        print("   data/train/ok_front/")
        print("   data/train/def_front/")
        print("4. Re-run this script")
        return
    
    # Display samples
    try:
        display_sample_images()
    except Exception as e:
        print(f"⚠️  Could not display images: {e}")
    
    print("\n" + "=" * 60)
    print("READY TO RUN JUPYTER NOTEBOOK")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Install TensorFlow (or use Google Colab):")
    print("   pip install tensorflow")
    print("\n2. Start Jupyter:")
    print("   python -m jupyter notebook notebooks/casting_defect_detection.ipynb")
    print("\n3. Run all cells to train the model")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
