# Task 13 – Casting Defect Classification using CNN

## 📌 Project Overview

This project uses a **Convolutional Neural Network (CNN)** to automatically classify casting images into two categories:

* **OK Casting (`ok_front`)**
* **Defective Casting (`def_front`)**

The model is trained using image data organized into training and testing folders. Data augmentation is used to improve model generalization, and the trained model is evaluated using multiple classification metrics.

---

## 🎯 Objective

The main objective of this task is to develop a deep learning-based image classification system that can automatically identify whether a casting component is:

* ✅ **OK**
* ❌ **Defective**

This can help reduce manual inspection effort and support automated quality-control systems in manufacturing.

---

## 📂 Dataset Structure

The dataset follows this structure:

```text
casting_data/
│
├── train/
│   ├── ok_front/
│   └── def_front/
│
└── test/
    ├── ok_front/
    └── def_front/
```

### Classes

| Class       | Description           | Label |
| ----------- | --------------------- | ----: |
| `ok_front`  | Non-defective casting |     0 |
| `def_front` | Defective casting     |     1 |

---

## 🧠 Methodology

The project follows these major steps:

```text
Dataset
   ↓
Dataset Exploration
   ↓
Image Preprocessing
   ↓
Data Augmentation
   ↓
CNN Architecture
   ↓
Model Training
   ↓
Validation
   ↓
Model Evaluation
   ↓
Classification Report
   ↓
Confusion Matrix
   ↓
False Positive / False Negative Analysis
   ↓
Threshold Comparison
   ↓
New Image Prediction
```

---

## 🔧 Technologies Used

* Python 3.12
* TensorFlow
* Keras
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Pillow
* Scikit-learn
* Jupyter Notebook / VS Code

---

## 🏗️ CNN Architecture

The CNN consists of multiple convolutional and pooling layers followed by fully connected layers.

### Architecture

```text
Input Image
    ↓
Data Augmentation
    ↓
Rescaling
    ↓
Conv2D (32 filters)
    ↓
MaxPooling
    ↓
Conv2D (64 filters)
    ↓
MaxPooling
    ↓
Conv2D (128 filters)
    ↓
MaxPooling
    ↓
Conv2D (256 filters)
    ↓
MaxPooling
    ↓
Dropout
    ↓
Flatten
    ↓
Dense (128)
    ↓
Dropout
    ↓
Sigmoid Output
    ↓
OK / Defective
```

---

## ⚙️ Data Preparation

The images are:

* Resized to **128 × 128 pixels**
* Converted into numerical tensors
* Normalized to the range **0–1**
* Divided into training and validation sets
* Loaded in batches of 32

A **20% validation split** is used from the training dataset.

---

## 🔄 Data Augmentation

The following augmentation techniques are applied:

* Random horizontal flipping
* Random rotation
* Random zoom
* Random translation

Data augmentation helps the CNN learn robust visual features and reduce overfitting.

---

## 🧪 Model Training

The model is compiled using:

```text
Optimizer: Adam
Loss: Binary Cross Entropy
Output Activation: Sigmoid
```

### Metrics

* Accuracy
* Precision
* Recall

The model uses:

* Early Stopping
* Learning Rate Reduction
* Model Checkpointing

The best-performing model is saved as:

```text
best_casting_cnn.keras
```

---

## 📊 Model Evaluation

The model is evaluated using the unseen test dataset.

The following evaluation techniques are included:

### 1. Accuracy

Measures the overall percentage of correctly classified images.

### 2. Precision

Measures how many images predicted as defective were actually defective.

### 3. Recall

Measures how many actual defective images were correctly detected.

### 4. F1-Score

Provides a balance between precision and recall.

---

## 📋 Classification Report

The classification report provides:

```text
Precision
Recall
F1-score
Support
```

for both:

* `ok_front`
* `def_front`

---

## 📉 Confusion Matrix

The confusion matrix provides four important values:

| Actual    | Predicted | Meaning        |
| --------- | --------- | -------------- |
| OK        | OK        | True Negative  |
| OK        | Defective | False Positive |
| Defective | OK        | False Negative |
| Defective | Defective | True Positive  |

### Important

For manufacturing quality inspection, **False Negatives are especially important** because they represent defective castings incorrectly classified as OK.

---

## 🔍 False Positive / False Negative Analysis

The notebook identifies and displays incorrectly classified images.

### False Positive

```text
Actual: OK
Predicted: Defective
```

This may result in an acceptable casting being rejected.

### False Negative

```text
Actual: Defective
Predicted: OK
```

This is more critical because a defective casting may pass inspection.

---

## 🎚️ Threshold Comparison

The CNN produces a probability between **0 and 1**.

The default threshold is:

```text
0.50
```

For example:

```text
Probability >= 0.50 → Defective
Probability < 0.50  → OK
```

Multiple thresholds are compared:

```text
0.20
0.30
0.40
0.50
0.60
0.70
0.80
```

The comparison includes:

* Accuracy
* Precision
* Recall
* F1-score
* False Positives
* False Negatives

A lower threshold may detect more defective castings but can increase false positives.

---

## 🖼️ New Image Prediction

The trained model can also classify a new casting image.

The prediction process is:

```text
New Image
    ↓
Resize to 128 × 128
    ↓
CNN Model
    ↓
Defective Probability
    ↓
Threshold
    ↓
OK / Defective
```

The notebook contains a `predict_new_image()` function for this purpose.

Update:

```python
NEW_IMAGE_PATH = "casting_data/test/ok_front/example.jpg"
```

with the actual image path before running the prediction cell.

---

## 📁 Project Files

Recommended project structure:

```text
Task-13-Casting-Defect-Classification/
│
├── casting_data/
│   ├── train/
│   │   ├── ok_front/
│   │   └── def_front/
│   │
│   └── test/
│       ├── ok_front/
│       └── def_front/
│
├── Task_13_Casting_Defect_CNN.ipynb
│
├── best_casting_cnn.keras
│
├── casting_defect_cnn_final.keras
│
├── casting_training_history.csv
│
└── README.md
```

> **Note:** If your repository does not contain the dataset, do not add the dataset structure as actual files. Keep the dataset description in the README and add the dataset locally when running the notebook.

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

### 2. Open the Project

```bash
cd Task-13-Casting-Defect-Classification
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

#### Windows

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install numpy pandas matplotlib seaborn pillow scikit-learn tensorflow
```

### 6. Start Jupyter

```bash
jupyter notebook
```

or open the project directly in **VS Code**.

### 7. Run the Notebook

Open:

```text
Task_13_Casting_Defect_CNN.ipynb
```

Run the cells sequentially from top to bottom.

---

## 💾 Model Output

After training, the notebook saves:

```text
best_casting_cnn.keras
```

and:

```text
casting_defect_cnn_final.keras
```

The training history is also saved as:

```text
casting_training_history.csv
```

---

## 📌 Key Learning Outcomes

Through this task, the following concepts are demonstrated:

* Image classification
* CNN architecture
* Image preprocessing
* Data augmentation
* Binary classification
* TensorFlow/Keras
* Model training
* Validation
* Model evaluation
* Classification reports
* Confusion matrices
* False positive analysis
* False negative analysis
* Probability thresholds
* New image prediction

---

## 🏭 Real-World Application

This type of system can be applied to:

* Manufacturing quality inspection
* Automated casting inspection
* Industrial defect detection
* Production-line monitoring
* Computer vision-based quality control

---

## 🔮 Future Improvements

The project can be improved by:

* Using transfer learning models such as ResNet, MobileNet or EfficientNet
* Increasing the training dataset
* Applying more advanced augmentation
* Hyperparameter tuning
* Using class weights for imbalanced datasets
* Performing cross-validation
* Deploying the model using Streamlit
* Creating a real-time camera-based inspection system

---

## ✅ Conclusion

This project demonstrates how a CNN can be used to automatically classify casting images as **OK** or **Defective**.

The complete pipeline includes dataset exploration, preprocessing, augmentation, CNN model development, training, evaluation, error analysis, threshold comparison and new-image prediction.

The approach provides a foundation for developing automated computer-vision-based quality inspection systems in manufacturing.
