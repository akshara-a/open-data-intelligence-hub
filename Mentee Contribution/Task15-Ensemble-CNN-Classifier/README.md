# Task 15 - Ensemble CNN Classifier

## Overview

This project implements an ensemble-based Convolutional Neural Network (CNN) image classification system using the CIFAR-10 dataset.

Two different CNN models are trained independently and their prediction probabilities are combined using probability averaging to produce the final ensemble prediction.

The project demonstrates:

* CIFAR-10 data preparation
* Training and validation data splitting
* CNN Model 1 implementation
* CNN Model 2 implementation
* Model evaluation
* Ensemble prediction
* Confusion matrix generation
* Classification report generation
* Model accuracy comparison

---

## Dataset

The project uses the **CIFAR-10** image classification dataset.

CIFAR-10 contains:

* 50,000 training images
* 10,000 test images
* Image size: 32 × 32 pixels
* 3 color channels (RGB)
* 10 classes

### Classes

1. Airplane
2. Automobile
3. Bird
4. Cat
5. Deer
6. Dog
7. Frog
8. Horse
9. Ship
10. Truck

The dataset is prepared locally and split into:

* Training: 45,000 images
* Validation: 5,000 images
* Test: 10,000 images

---

## Project Structure

```text
Task15-Ensemble-CNN-Classifier/
│
├── src/
│   ├── data_loader.py
│   ├── cnn_model_1.py
│   ├── cnn_model_2.py
│   └── ensemble_classifier.py
│
├── models/
│   ├── cnn_model_1.keras
│   └── cnn_model_2.keras
│
├── reports/
│   ├── cifar10_samples.png
│   ├── cnn_model_1_accuracy.png
│   ├── cnn_model_1_loss.png
│   ├── cnn_model_2_accuracy.png
│   ├── cnn_model_2_loss.png
│   ├── ensemble_accuracy_comparison.png
│   ├── ensemble_classification_report.txt
│   └── ensemble_confusion_matrix.png
│
├── outputs/
│   ├── ensemble_predictions.npy
│   └── ensemble_probabilities.npy
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Data Preparation

The `data_loader.py` script loads the locally extracted CIFAR-10 dataset and creates the training, validation, and test datasets.

Run:

```powershell
python src\data_loader.py
```

The script also creates a sample visualization of CIFAR-10 images.

---

## CNN Model 1

CNN Model 1 is trained on the CIFAR-10 training dataset and evaluated on the test dataset.

Run:

```powershell
python src\cnn_model_1.py
```

### Test Result

**Test Accuracy: 74.16%**

The trained model is saved as:

```text
models/cnn_model_1.keras
```

Training graphs are saved in the `reports` directory.

---

## CNN Model 2

CNN Model 2 provides a second CNN architecture for comparison and ensemble prediction.

Run:

```powershell
python src\cnn_model_2.py
```

### Test Result

**Test Accuracy: 80.46%**

The trained model is saved as:

```text
models/cnn_model_2.keras
```

Training graphs are saved in the `reports` directory.

---

## Ensemble Classifier

The ensemble classifier loads both trained CNN models.

Each model generates class probabilities for the test images. The probabilities from both models are averaged:

```text
Ensemble Probability =
(Model 1 Probability + Model 2 Probability) / 2
```

The class with the highest averaged probability is selected as the final ensemble prediction.

Run:

```powershell
python src\ensemble_classifier.py
```

### Final Results

| Model       | Test Accuracy |
| ----------- | ------------: |
| CNN Model 1 |        74.16% |
| CNN Model 2 |        80.46% |
| Ensemble    |        79.38% |

The ensemble achieved **79.38% test accuracy** on the 10,000-image CIFAR-10 test set.

---

## Evaluation Outputs

The ensemble classifier generates:

### Confusion Matrix

```text
reports/ensemble_confusion_matrix.png
```

### Classification Report

```text
reports/ensemble_classification_report.txt
```

### Accuracy Comparison

```text
reports/ensemble_accuracy_comparison.png
```

### Ensemble Predictions

```text
outputs/ensemble_predictions.npy
```

### Ensemble Probabilities

```text
outputs/ensemble_probabilities.npy
```

---

## Technologies Used

* Python 3.13
* TensorFlow 2.21.0
* NumPy
* Pandas
* Matplotlib
* Scikit-learn
* Pillow
* psutil

---

## How to Run

### 1. Create virtual environment

```powershell
python -m venv .venv
```

### 2. Activate virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Prepare CIFAR-10 data

```powershell
python src\data_loader.py
```

### 5. Train CNN Model 1

```powershell
python src\cnn_model_1.py
```

### 6. Train CNN Model 2

```powershell
python src\cnn_model_2.py
```

### 7. Run ensemble classifier

```powershell
python src\ensemble_classifier.py
```

---

## Conclusion

This task demonstrates how multiple CNN models can be used together for image classification through probability-based ensemble prediction.

The two individual CNN models achieved different test accuracies, and their predictions were combined to generate the final ensemble result.

**Task 15 completed successfully.**
