# Binary Image Classification Using a Convolutional Neural Network

**Task 14 Mini Project: Quality Inspection for Casting Products**

This repository contains a complete TensorFlow / Keras implementation of a Convolutional Neural Network (CNN) designed to classify industrial casting product images into two categories:
- `ok_front`: Non-defective product (Class 0)
- `def_front`: Defective product (Class 1)

---

## 📁 Repository Structure

```text
Task 14 - Binary Image Classification CNN/
├── data/
│   ├── train/          # Training images (ok_front, def_front)
│   ├── validation/     # Validation images (ok_front, def_front)
│   └── test/           # Test evaluation images (ok_front, def_front)
├── models/
│   └── best_cnn_model.keras   # Saved trained Keras model
├── notebooks/
│   └── task14_cnn_classification.ipynb  # Executable Jupyter notebook
├── predictions/
│   ├── prediction_1.png  # Annotated unseen test sample predictions
│   ├── prediction_2.png
│   ├── prediction_3.png
│   ├── prediction_4.png
│   └── prediction_5.png
├── reports/
│   ├── accuracy_graph.png    # Training & validation accuracy curve
│   ├── loss_graph.png        # Training & validation loss curve
│   ├── confusion_matrix.png  # Confusion matrix heatmap
│   ├── model_summary.txt     # Keras model.summary() output
│   └── findings_report.md    # Documented design decision table & analysis
├── src/
│   ├── generate_dataset.py   # Dataset generation script
│   ├── train.py              # CNN model creation, callbacks & training
│   ├── evaluate.py           # Test evaluation & metrics reporting
│   └── predict.py            # Unseen sample prediction & visual output
├── requirements.txt          # Required Python packages
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset
```bash
python src/generate_dataset.py
```

### 3. Train Model
```bash
python src/train.py
```

### 4. Evaluate Model Metrics
```bash
python src/evaluate.py
```

### 5. Run Unseen Sample Predictions
```bash
python src/predict.py
```

---

## 📊 Design Decisions Summary

- **Input Dimensions**: `224 x 224 x 3`
- **Architecture**: `32 -> 64 -> 128 Conv2D` with `MaxPooling2D`, `GlobalAveragePooling2D`, `Dropout(0.40)`
- **Activation**: Hidden `ReLU`, Output `Sigmoid`
- **Optimizer**: `Adam(lr=0.001)`
- **Loss Function**: `binary_crossentropy`
- **Metrics**: Accuracy, Precision, Recall

