Building an Image Recognition System for Quality Control

Project Overview

This project builds a Convolutional Neural Network (CNN) based image classification system for detecting casting product defects.

The system classifies casting product images into two categories:

Non-defective (ok_front)

Defective (def_front)

The model is designed to support quality-control inspection by identifying defective products and recommending manual inspection when a defect is predicted.

Dataset

The project uses the Casting Product Image Data for Quality Inspection dataset.

Original dataset structure:

casting_512x512/
├── ok_front/
└── def_front/

The dataset was divided into:

70% Training

15% Validation

15% Testing

The classes used in the model are:

ok_front  → 0
def_front → 1

Technologies Used

Python

TensorFlow / Keras

NumPy

Matplotlib

Scikit-learn

Jupyter Notebook in VS Code

Project Workflow

Dataset
   ↓
Train / Validation / Test Split
   ↓
Image Loading
   ↓
Data Augmentation
   ↓
CNN Model
   ↓
Model Training
   ↓
Accuracy & Loss Evaluation
   ↓
Test Evaluation
   ↓
Classification Report
   ↓
Confusion Matrix
   ↓
Single Image Prediction

Data Preprocessing

Images are resized to:

224 × 224

The following data augmentation techniques are used on training images:

Horizontal Flip

Small Rotation

Zoom

Translation

Contrast Adjustment

Pixel values are normalized using rescaling by 1/255.

CNN Architecture

The CNN contains:

Input layer

3 Convolutional layers

Max Pooling layers

ReLU activation

Global Average Pooling

Dropout layers

Dense layer

Sigmoid output layer

The final sigmoid output provides the probability used for binary classification.

Model Compilation

The model uses:

Optimizer: Adam

Loss: Binary Cross-Entropy

Metrics: Accuracy, Precision, Recall

Callbacks used:

Early Stopping

ReduceLROnPlateau

Model Checkpoint

Evaluation

The model is evaluated using:

Test Accuracy

Precision

Recall

Classification Report

Confusion Matrix

False Positive (FP)

False Negative (FN)

False negatives are particularly important in quality control because a defective product incorrectly classified as non-defective may pass inspection.

Sample Predictions

Non-defective Product

A sample image from ok_front was classified as:

Prediction: Non-defective
Defect probability: 39.46%
Recommended action: Product may proceed

Defective Product

A sample image from def_front was classified as:

Prediction: Defective
Defect probability: 93.46%
Recommended action: Send for manual inspection

Recommended Action Logic

The prediction threshold is:

Probability >= 0.50 → Defective
Probability < 0.50  → Non-defective

For defective predictions, the recommended action is:

Send for manual inspection

For non-defective predictions:

Product may proceed

Project Outcome

The completed system demonstrates how CNN-based image classification can be applied to automated casting-product quality inspection. It provides classification predictions, defect probability, evaluation metrics, and an actionable recommendation for individual images.

Files

Cnn.ipynb
README.md
best_casting_defect_model.keras

Conclusion

This project implements an end-to-end deep learning workflow for casting defect detection. The system can classify product images as defective or non-defective and provide a simple quality-control recommendation based on the model prediction.