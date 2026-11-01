# Casting Defect Detection Using CNN

## 1. Project Overview

This project uses a Convolutional Neural Network (CNN) to automatically detect defects in casting product images.

The system classifies casting images into two categories:

- OK / Acceptable
- Defective

## 2. Technologies Used

- Python
- TensorFlow
- Keras
- CNN
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook

## 3. Dataset

The dataset contains casting product images divided into training and testing sets.

Classes:
- def_front
- ok_front

## 4. Model

A CNN model was developed using convolutional layers, max-pooling layers, dense layers and dropout.

The input image size is 224 × 224 pixels.

## 5. Results

Test Accuracy: 98.04%

Test Loss: 0.0433

### Classification Performance

| Class | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| OK / Acceptable | 0.95 | 1.00 | 0.97 |
| Defective | 1.00 | 0.97 | 0.98 |

Overall Accuracy: 98%

## 6. Project Structure

```text
casting-quality-inspection-project/
│
├── data/
│   ├── train/
│   │   ├── def_front/
│   │   └── ok_front/
│   └── test/
│       ├── def_front/
│       └── ok_front/
│
├── models/
│   └── casting_defect_model.keras
│
├── notebooks/
│   └── casting_defect_detection.ipynb
│
├── reports/
│   ├── accuracy_graph.png
│   ├── loss_graph.png
│   ├── confusion_matrix.png
│   └── model_results.txt
│
├── sample_images/
│   └── test_casting.jpeg
│
├── src/
│   └── train_model.py
│
├── requirements.txt
└── README.md