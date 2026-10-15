# Task 13: Automated Casting Defect Detection Using CNN

## Overview
This project implements an industrial binary image classification pipeline using a Convolutional Neural Network (CNN) to detect defects in metal casting products (`0 = Non-defective`, `1 = Defective`).

## Model Architecture & Key Components
- **Data Augmentation:** Horizontal flip, rotation, zoom, translation, and contrast adjustments applied exclusively to training data.
- **Feature Extraction:** 3 Conv2D blocks with ReLU activation and MaxPooling2D layers.
- **Regularization & Optimization:** GlobalAveragePooling2D, Dropout (0.40, 0.30), EarlyStopping, and ReduceLROnPlateau callbacks with Adam optimizer.

## Files Included
- `task13_casting_defect_detection.ipynb`
- `casting_defect_script.py`
- `best_casting_defect_model.keras`
- `training_performance.png`
- `confusion_matrix.png`
- `defect_detection_summary.md`
- `requirements.txt`
- `README.md`