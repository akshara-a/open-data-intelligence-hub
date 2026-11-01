# Automated Casting Defect Detection Using a Convolutional Neural Network (CNN)

![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)
![TensorFlow Version](https://img.shields.io/badge/TensorFlow-2.20-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An industrial-grade, end-to-end computer vision binary image classification system that inspects manufactured casting products (metal pump impellers) and determines whether a product is **Non-defective (0)** or **Defective (1)**.

---

## 1. Case & Business Scenario

Manufacturing companies visually examine products on assembly lines to detect surface flaws before shipping to customers. Manual inspection is susceptible to operator fatigue, human error, inconsistent standards, and throughput bottlenecks when thousands of units are processed daily.

This system automates quality control by deploying a **Convolutional Neural Network (CNN)**. When a camera captures an image at the inspection station:
1. The image is resized to **224 × 224** and preprocessed.
2. The CNN analyzes surface features (cracks, blowholes, porosity, edge inclusions).
3. The model returns a continuous **defect probability** between `0.0` and `1.0`.
4. Based on a configurable **decision threshold** (default `0.50`), the product is flagged as `Defective` or `Non-defective`.
5. Automated action recommendations guide factory line operators (`Send for manual inspection` vs `Product may proceed`).

### Binary Labels
- **Label 0 (`ok_front`)**: Non-defective product passed inspection.
- **Label 1 (`def_front`)**: Defective product containing visible casting flaws.

---

## 2. Project Architecture & Folder Structure

```text
casting-quality-inspection/
│
├── data/                               # Dataset directory
│   ├── train/
│   │   ├── ok_front/                   # Non-defective training images (Label 0)
│   │   └── def_front/                  # Defective training images (Label 1)
│   │
│   └── test/
│       ├── ok_front/                   # Non-defective test images
│       └── def_front/                  # Defective test images
│
├── src/                                # Modular Python package
│   ├── __init__.py                     # Package initializer
│   ├── data_loader.py                  # tf.data dataset creation, splits, prefetching
│   ├── augmentation.py                 # Keras Sequential data augmentation pipeline
│   ├── model.py                        # Custom 3-Block CNN architecture definition
│   ├── train.py                        # Training pipeline with regularization callbacks
│   ├── evaluate.py                     # Evaluation, confusion matrix, threshold tuning
│   ├── predict.py                      # Single image inference CLI & python function
│   └── utils.py                        # Helper plotting routines & report saving
│
├── notebooks/
│   └── casting_defect_detection.ipynb  # Interactive step-by-step Jupyter Notebook
│
├── models/
│   └── best_casting_defect_model.keras # Saved best trained model weights
│
├── reports/                            # Generated evaluation figures & text reports
│   ├── accuracy_graph.png
│   ├── loss_graph.png
│   ├── confusion_matrix.png
│   └── classification_report.txt
│
├── sample_images/                      # Pre-packaged sample factory images
│   ├── sample_ok_1.jpg
│   ├── sample_ok_2.jpg
│   ├── sample_def_1.jpg
│   ├── sample_def_2.jpg
│   └── sample_def_3.jpg
│
├── app.py                              # Streamlit Industrial Inspection Dashboard
├── generate_dataset.py                 # Synthetic dataset generator for instant execution
├── requirements.txt                    # Project dependencies
└── README.md                           # Documentation
```

---

## 3. Neural Network Architecture

The CNN design balances high feature extraction capacity with regularization to prevent overfitting on factory data:

```text
Input Image (224 x 224 x 3)
    │
Data Augmentation (Flip, Rotation, Zoom, Translation, Contrast - Training only)
    │
Rescaling (Normalize pixel values 0-255 -> 0.0-1.0)
    │
Conv2D (32 filters, 3x3 kernel, ReLU) ──> MaxPooling2D (2x2)
    │
Conv2D (64 filters, 3x3 kernel, ReLU) ──> MaxPooling2D (2x2)
    │
Conv2D (128 filters, 3x3 kernel, ReLU) ──> MaxPooling2D (2x2)
    │
GlobalAveragePooling2D
    │
Dropout (0.40)
    │
Dense (64 units, ReLU)
    │
Dropout (0.30)
    │
Dense (1 unit, Sigmoid) ──> Defect Probability [0.0 - 1.0]
```

### Component Summary
| Layer | Purpose |
| :--- | :--- |
| `Conv2D` | Detects spatial patterns (edges, cracks, surface pits, dark patches) |
| `MaxPooling2D` | Downsamples feature maps while preserving key visual signals |
| `GlobalAveragePooling2D` | Converts feature maps to flat 128-dim vector without spatial distortion |
| `Dropout (0.40 / 0.30)` | Prevents co-adaptation of neurons and reduces overfitting |
| `Sigmoid Output` | Produces probability score for binary classification |

---

## 4. Installation & Requirements

### Prerequisites
- Python 3.10+
- Pip package manager

### Environment Setup
```bash
# Clone or navigate to the repository
cd casting-quality-inspection

# Install required dependencies
pip install -r requirements.txt
```

---

## 5. Usage & Execution Workflow

### Step 1: Generate / Configure Dataset
To run immediately out of the box with realistic synthetic metallic casting images:
```bash
python generate_dataset.py
```
> **Note**: To use the official Kaggle dataset (*Casting Product Image Data for Quality Inspection*), simply place `ok_front` and `def_front` folders inside `data/train/` and `data/test/`. No code changes are required.

### Step 2: Train the Model
Train the CNN model with Adam optimizer, binary cross-entropy loss, and EarlyStopping/ReduceLROnPlateau callbacks:
```bash
python -m src.train
```
- Saved model output: `models/best_casting_defect_model.keras`
- Generated graphs: `reports/accuracy_graph.png`, `reports/loss_graph.png`

### Step 3: Evaluate Model Performance
Evaluate the model on unseen test data and generate classification reports and confusion matrices:
```bash
python -m src.evaluate
```
- Generated reports: `reports/confusion_matrix.png`, `reports/classification_report.txt`

### Step 4: Single Image Inference (CLI)
Run quality inspection on any single product image:
```bash
python -m src.predict --image sample_images/sample_def_1.jpg --threshold 0.50
```

#### Example CLI Output:
```text
==================================================
      INDUSTRIAL QUALITY INSPECTION RESULT      
==================================================
Image File          : sample_def_1.jpg
Prediction          : Defective
Defect Probability  : 94.70%
Decision Threshold  : 50.00%
Recommended Action  : Send for manual inspection
==================================================
```

### Step 5: Launch Streamlit Web App
Launch an interactive industrial dashboard in your browser:
```bash
streamlit run app.py
```

---

## 6. Training Dynamics & Regularization Callbacks

- **Optimizer**: Adam (learning rate = 0.001)
- **Loss Function**: `binary_crossentropy`
- **Callbacks**:
  - `EarlyStopping`: Stops training if `val_loss` does not improve for 5 consecutive epochs, restoring best weights.
  - `ReduceLROnPlateau`: Halves learning rate (`factor=0.5`) if `val_loss` plateaus for 2 epochs.
  - `ModelCheckpoint`: Saves only the best model checkpoint based on lowest validation loss.

---

## 7. Decision Threshold & False Negative Analysis

In quality control, **False Negatives (FN)**—classifying a defective product as non-defective—are far more costly than False Positives (FP), as shipping a defective component damages customer trust.

The default decision threshold is `0.50`. Factory operators can adjust the threshold (e.g., to `0.40` or `0.30`) via the Streamlit web dashboard or CLI:
- **Lower Threshold (e.g., 0.35)**: Increases recall, catches more subtle defects, minimizes False Negatives.
- **Higher Threshold (e.g., 0.65)**: Increases precision, reduces unnecessary rejections of acceptable products.

---

## 8. License & Acknowledgments

Developed as a demonstration of computer vision and deep learning best practices in industrial quality inspection and manufacturing automation.
