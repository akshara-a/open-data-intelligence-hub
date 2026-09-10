# 🔬 Binary Image Classification Using a Convolutional Neural Network for Quality

## 📋 Project Overview
This project implements a **binary image classification system** using a **Convolutional Neural Network (CNN)** to detect defects in manufactured casting products. The model classifies product images as either **Non‑defective (0)** or **Defective (1)** – automating quality control in industrial production lines.

### Problem Statement
Manual visual inspection is error‑prone, slow, and inconsistent. Our CNN solution provides:
- **High speed** – inference in milliseconds.
- **High accuracy** – 98.3% on test data.
- **Consistency** – same decision every time.
- **Scalability** – can process thousands of images per day.

---

## 📊 Dataset

**Source**: [Casting Product Image Data for Quality Inspection](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product)

- **Non‑defective** (`ok_front`) → label **0**
- **Defective** (`def_front`) → label **1**

| Set | Non‑defective | Defective | Total |
|-----|---------------|-----------|-------|
| Training | 2,875 | 3,761 | 6,636 |
| Test | 500 | 500 | 1,000 |

---

## 🧠 Model Architecture

We designed a **lightweight CNN** with documented design choices:

### Key Design Decisions
| Component | Choice | Reason |
|-----------|--------|--------|
| Input size | 128×128 | Balances speed and accuracy |
| Conv layers | 3 blocks | Enough to learn defect patterns |
| Pooling | MaxPooling | Preserves important features |
| Regularization | Dropout (0.3, 0.2) | Prevents overfitting |
| Output | Sigmoid | Binary classification probability |

---

## ⚙️ Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam (lr=0.001) |
| Loss | Binary Cross‑Entropy |
| Batch size | 32 |
| Epochs | 15 (early stopping) |
| Validation split | 20% |
| Early stopping patience | 4 |
| LR reduction patience | 2 |
| Metrics | Accuracy, Precision, Recall |

**Callbacks**: `EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`.

---

## 📊 Results

We performed a **bonus experiment** comparing dropout values.

| Model | Dropout | Test Accuracy | Precision | Recall | F1 | AUC |
|-------|---------|---------------|-----------|--------|----|-----|
| Original | 0.40 | **95.7%** | 0.95 | 0.94 | 0.945 | 0.98 |
| Bonus | 0.20 | **98.3%** | 0.98 | 0.97 | 0.975 | 0.99 |

**Confusion Matrix (Bonus, threshold=0.50)**:
