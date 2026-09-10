# 🏭 Casting Defect Detection Using Deep Learning

## 📋 Project Overview
This project implements a **binary image classification system** using a **Convolutional Neural Network (CNN)** to automatically detect defects in manufactured casting products. The model classifies product images as either **Non‑defective (0)** or **Defective (1)**.

The system is designed for industrial quality‑control pipelines where speed, accuracy, and consistency are critical.

---

## Dataset

**Source**: [Casting Product Image Data for Quality Inspection](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product)

- **Non‑defective** (`ok_front`) → label **0**
- **Defective** (`def_front`) → label **1**

### Dataset Statistics
| Set | Non‑defective | Defective | Total |
|-----|---------------|-----------|-------|
| Training | 2,875 | 3,761 | 6,636 |
| Test | 500 | 500 | 1,000 |

---

## Model Architecture

A lightweight CNN with documented design choices:

**Key Design Decisions**:
- 3 convolutional blocks to learn hierarchical features.
- GlobalAveragePooling reduces parameters and prevents overfitting.
- Dropout (0.3, 0.2) for regularisation.
- Sigmoid output for binary probability.

---

## ⚙️ Training Configuration

| Parameter | Value |
|-----------|-------|
| Image Size | 128×128 |
| Batch Size | 32 |
| Epochs | 15 (with early stopping) |
| Optimizer | Adam (lr=0.001) |
| Loss | Binary Cross‑Entropy |
| Metrics | Accuracy, Precision, Recall |
| Validation Split | 20% |
| Early Stopping | patience=4, restore best weights |
| LR Reduction | factor=0.5, patience=2 |

**Callbacks**: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint.

---

##  Results

| Design | Dropout | Test Accuracy |
|--------|---------|---------------|
| Original | 0.40 | **95.7%** |
| Bonus Experiment | 0.20 | **98.3%** |

**Confusion Matrix (Bonus)**:
