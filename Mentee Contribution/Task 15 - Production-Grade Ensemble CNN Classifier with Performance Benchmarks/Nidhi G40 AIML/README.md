# Production-Grade Ensemble CNN Classifier with Performance Benchmarks

## 📌 Project Overview

This project implements a production-oriented image classification system for detecting manufacturing casting defects using multiple Convolutional Neural Network (CNN) architectures.

The project trains and evaluates three different CNN models and combines their predictions using ensemble learning techniques.

The main objective is to compare:

- Individual CNN performance
- Ensemble performance
- Model size and parameters
- Inference latency
- Throughput
- Robustness to image distortions
- Model disagreement and prediction confidence

The final analysis is used to identify a suitable model for production deployment.

---

## 🎯 Objectives

The major objectives of this project are:

1. Build three different CNN classifiers.
2. Train all models using the same dataset split.
3. Evaluate each model independently.
4. Combine predictions using ensemble techniques.
5. Compare individual models with ensemble models.
6. Benchmark inference performance.
7. Test model robustness under image distortions.
8. Analyze model disagreement and prediction confidence.
9. Compare accuracy with production cost.
10. Recommend the most suitable model for deployment.

---

## 📂 Dataset

### Casting Defect Dataset

The project uses a manufacturing casting defect image dataset.

### Classes

The dataset contains two classes:

- `ok_front` — Non-defective casting
- `def_front` — Defective casting

### Image Configuration

| Parameter | Value |
|---|---|
| Image Size | 224 × 224 |
| Batch Size | 32 |
| Number of Classes | 2 |
| Problem Type | Binary Classification |

The same train, validation and test split is used for all three CNN models to ensure a fair comparison.

---

## 🔄 Data Preprocessing

The images are resized to:

```text
224 × 224