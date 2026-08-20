# Task 15 - Ensemble CNN Classifier

## 📌 Project Overview

This project implements multiple Convolutional Neural Network (CNN) architectures for image classification using the CIFAR-10 dataset.

Three different CNN models were developed and compared:

1. Baseline CNN
2. Regularized CNN
3. Deep CNN

The models were evaluated individually and then combined using a weighted ensemble approach.

The project also includes:

- Model evaluation
- Weighted ensemble learning
- Performance benchmarking
- Robustness testing
- Image prediction

---

# 📂 Project Structure

```text
Task 15 - Ensemble CNN Classifier/
│
├── data/
│
├── models/
│   ├── baseline_cnn.keras
│   ├── regularized_cnn.keras
│   └── deep_cnn.keras
│
├── results/
│   ├── baseline_cnn_confusion_matrix.png
│   ├── regularized_cnn_confusion_matrix.png
│   ├── deep_cnn_confusion_matrix.png
│   ├── model_comparison.csv
│   ├── ensemble_results.csv
│   ├── benchmark_results.csv
│   └── robustness_results.csv
│
├── src/
│   ├── data_loader.py
│   ├── models.py
│   ├── train.py
│   ├── evaluate.py
│   ├── ensemble.py
│   ├── benchmark.py
│   ├── robustness_test.py
│   └── predict.py
│
├── requirements.txt
└── README.md