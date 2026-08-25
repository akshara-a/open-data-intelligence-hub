# Automated Casting Defect Detection Using CNN

## Project Overview

This project implements a **binary image classification system** that automatically inspects casting product images and predicts whether they are:
- **Non-defective (0)**: Product without visible defects
- **Defective (1)**: Product with visible defects

The system uses a **Convolutional Neural Network (CNN)** trained on the Kaggle dataset: *Casting Product Image Data for Quality Inspection*.

---

## 📦 Project Size (Optimized for GitHub)

✅ **GitHub Upload**: ~500 KB (source code + notebooks only)  
✅ **No Large Files**: Data & models excluded via `.gitignore`  
✅ **Two Notebook Versions**:
- `casting_defect_detection.ipynb` - Full version with detailed explanations
- `casting_defect_detection_clean.ipynb` - Lightweight clean version (recommended for GitHub)

See [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md) for upload instructions.

---

## Business Scenario

A casting manufacturer produces metal components such as pump impellers. When a product reaches the inspection point:
1. A camera captures an image
2. The image is resized and prepared for the model
3. The CNN analyzes the image
4. The model returns a defect probability
5. The product is classified as defective or non-defective
6. Defective products are sent for manual review or removed from the production line

## Project Structure

```
casting-quality-inspection/
├── data/
│   ├── train/
│   │   ├── ok_front/        # Non-defective training images
│   │   └── def_front/       # Defective training images
│   └── test/
│       ├── ok_front/        # Non-defective test images
│       └── def_front/       # Defective test images
├── notebooks/
│   └── casting_defect_detection.ipynb
├── models/
│   └── best_casting_defect_model.keras
├── sample_images/           # For testing predictions
├── reports/                 # Visualizations and results
├── requirements.txt
└── README.md
```

## 🚀 How to Run This Project

### **FASTEST METHOD: Google Colab (Recommended)**

1. **Open Google Colab:**
   - Go to: https://colab.research.google.com
   
2. **Upload the Notebook:**
   - Click `File` → `Upload notebook`
   - Select `notebooks/casting_defect_detection.ipynb`
   
3. **Run All Cells:**
   - Click the ▶️ play button on each cell (or use Ctrl+A to select all, then Ctrl+Enter)
   - Colab has TensorFlow pre-installed
   - GPU training will take ~10-30 minutes
   
4. **View Results:**
   - Accuracy/loss graphs
   - Confusion matrix
   - Classification report
   - Model predictions

**Advantages:**
- ✅ No TensorFlow installation needed
- ✅ Free GPU access
- ✅ Works with Python 3.14
- ✅ No setup required

---

### **LOCAL METHOD A: Python 3.11 or 3.12 (Full Setup)**

```bash
# Step 1: Download Dataset from Kaggle
# Go to: https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product
# Extract to: data/train/ and data/test/

# Step 2: Install all dependencies
pip install -r requirements.txt

# Step 3: Start Jupyter
python -m jupyter notebook notebooks/casting_defect_detection.ipynb

# Step 4: Run cells sequentially (Cell 1 → Cell 22)
```

**Requirements:**
- Python 3.11 or 3.12 (NOT 3.14)
- ~500MB free disk space
- TensorFlow requires this Python version

---

### **LOCAL METHOD B: Quick Test (Python 3.14 OK)**

Test the project without training:

```bash
# Step 1: Install minimal packages
pip install numpy matplotlib scikit-learn seaborn Pillow Pillow

# Step 2: Run demo to verify dataset
python quick_start.py    # Check dataset structure (6,633 images)

# Step 3: View project overview
python demo.py           # See architecture & data preview

# Step 4: Then use Google Colab for actual training
```

---

### **LOCAL METHOD C: Google Colab Alternative**

If you can't run locally:

```bash
# Just open in browser - no installation needed
https://colab.research.google.com
# Then upload: notebooks/casting_defect_detection.ipynb
```

---

## ⚡ Quick Start (3 Steps)

### 1. Download Dataset
```bash
# Download from Kaggle:
# https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product

# Extract to:
data/train/ok_front/   # Non-defective training images
data/train/def_front/  # Defective training images
data/test/ok_front/    # Non-defective test images
data/test/def_front/   # Defective test images
```

### 2. Install Dependencies
```bash
# For Python 3.11/3.12:
pip install -r requirements.txt

# For Python 3.14 (basic only):
pip install numpy matplotlib scikit-learn seaborn Pillow jupyter ipykernel
```

### 3. Run Notebook
```bash
# Option A: Local (Python 3.11/3.12)
python -m jupyter notebook notebooks/casting_defect_detection.ipynb

# Option B: Google Colab (Any Python version)
# Go to https://colab.research.google.com and upload notebook
```

---

## ⚠️ Python 3.14 Users - TensorFlow Issue

**TensorFlow doesn't have official wheels for Python 3.14 yet.**

### **Recommended Solution: Google Colab ⚡**
1. Go to: https://colab.research.google.com
2. Upload notebook: `notebooks/casting_defect_detection.ipynb`
3. Colab has TensorFlow pre-installed
4. Run all cells (GPU available for free)

### **Alternative: Use Python 3.11 or 3.12**
```bash
pip install -r requirements.txt
python -m jupyter notebook notebooks/casting_defect_detection.ipynb
```

### **Test Without Training:**
```bash
python quick_start.py  # Validates dataset structure
python demo.py         # Shows architecture
```

---

## Setup Instructions (Full)

### 1. Download Project from GitHub

```bash
git clone https://github.com/YOUR_USERNAME/casting-defect-detection.git
cd casting-defect-detection
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Dataset

1. Go to [Kaggle - Casting Product Image Data](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product)
2. Download the dataset
3. Extract the images into the `data/train/` and `data/test/` directories following the folder structure above

### 3. Organize Data

Ensure your data is organized as:
- `data/train/ok_front/` - Training images of non-defective products
- `data/train/def_front/` - Training images of defective products
- `data/test/ok_front/` - Test images of non-defective products
- `data/test/def_front/` - Test images of defective products

### 4. Run the Notebook

```bash
python -m jupyter notebook notebooks/casting_defect_detection.ipynb
```

## Key Features

### Data Preparation
- Image resizing to 224×224 pixels
- Pixel normalization (0-1 range)
- 70-80% training, 10-20% validation, 10-20% test split

### Data Augmentation
The model uses mild augmentation on training data only:
- Horizontal flip
- Random rotation (±5%)
- Random zoom (±10%)
- Random translation (±5%)
- Random contrast adjustment (±10%)

### CNN Architecture
- **Input**: 224×224×3 RGB images
- **Convolution Layers**: 3 layers (32, 64, 128 filters)
- **Pooling Layers**: Max pooling after each convolution
- **Regularization**: Dropout (40%, 30%)
- **Output**: Sigmoid activation for binary classification

### Training Configuration
- **Optimizer**: Adam (learning rate = 0.001)
- **Loss Function**: Binary cross-entropy
- **Batch Size**: 32
- **Epochs**: 25 (with early stopping)
- **Metrics**: Accuracy, Precision, Recall

### Regularization Techniques
- Data augmentation (training only)
- Dropout layers
- Early stopping (patience=5)
- Learning rate reduction on plateau
- Model checkpointing (saves best weights)

## Model Evaluation

The model is evaluated using:
- **Accuracy**: Overall correctness
- **Precision**: Of predicted defects, how many were correct
- **Recall**: Of actual defects, how many were detected
- **Confusion Matrix**: TP, TN, FP, FN breakdown
- **F1-Score**: Balance between precision and recall

### Interpreting Results

**Good Learning**
- Training accuracy increases
- Validation accuracy also increases
- Training and validation results remain close

**Overfitting** (if observed)
- Training accuracy continues increasing
- Validation accuracy stops or decreases
- Validation loss begins increasing

**Underfitting** (if observed)
- Both accuracies remain low
- Model may need more training or complexity

## Predictions

### Single Image Prediction

```python
from casting_defect_detection import predict_product

predict_product(
    "sample_images/product_01.jpeg",
    model,
    threshold=0.50
)
```

**Example Output**:
```
Prediction: Defective
Defect probability: 94.7%
Recommended action: Send product for manual inspection
```

### Adjusting Classification Threshold

The default threshold is 0.50. For stricter quality control, adjust:

```python
threshold = 0.40  # Lower = detect more defects (higher false positives)
threshold = 0.60  # Higher = fewer rejections (more false negatives)
```

## Key Considerations

### False Positives vs. False Negatives
- **False Positive**: Rejecting a good product (waste, cost)
- **False Negative**: Allowing a defective product through (critical risk)

**Priority**: Minimize false negatives to ensure quality

### Threshold Selection
Experiment with thresholds: 0.30, 0.40, 0.50, 0.60 to find the best balance for your use case.

## Expected Deliverables

✅ Jupyter Notebook with complete implementation  
✅ Dataset description and visualization  
✅ Data preparation code  
✅ Data augmentation pipeline  
✅ CNN architecture with model summary  
✅ Training configuration with callbacks  
✅ Accuracy and loss graphs  
✅ Confusion matrix  
✅ Classification report  
✅ Predictions for unseen images  
✅ Saved best model  
✅ This README with execution instructions

## Optional Advanced Improvements

After completing the basic CNN, experiment with:
- Transfer learning (MobileNetV2, EfficientNet)
- Batch normalization
- Class weights for imbalanced data
- Threshold tuning
- Grad-CAM visualizations
- Streamlit web application
- Webcam-based inspection
- Model conversion to TensorFlow Lite

## Acceptance Criteria

- [x] Binary classification (0 = non-defective, 1 = defective)
- [x] Train/validation/test data separated
- [x] Image normalization applied
- [x] Data augmentation (training only)
- [x] Convolution and pooling layers
- [x] Sigmoid activation in output layer
- [x] Binary cross-entropy loss
- [x] Early stopping configured
- [x] Dropout regularization
- [x] Training graphs generated
- [x] Precision and recall reported
- [x] Confusion matrix generated
- [x] Model can predict new images
- [x] Best model saved

## Execution Instructions

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Download dataset** from Kaggle and organize in `data/` folder
3. **Run notebook**: `jupyter notebook notebooks/casting_defect_detection.ipynb`
4. **Review results**: Check graphs, metrics, and predictions
5. **Use for production**: Load saved model and call `predict_product()` function

## Expected Outcome

The completed system accepts a casting product image and produces:

```
Product classification: Defective
Defect probability: 91.4%
Decision threshold: 50%
Recommended action: Reject or send for manual inspection
```

This demonstrates how CNNs support industrial quality-control teams with faster and more consistent product inspection.
