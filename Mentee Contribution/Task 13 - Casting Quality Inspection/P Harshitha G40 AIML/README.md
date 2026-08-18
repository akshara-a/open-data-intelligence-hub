# Casting Defect Detection Using CNN
## 1. Project Overview
Manufacturing companies need to inspect casting products to identify defective products before they reach customers.
Manual inspection can be time-consuming and may result in inconsistent decisions. This project develops an image classification system using a Convolutional Neural Network (CNN) to automatically classify casting product images into:
- Defective
- Non-defective
The system can help support automated quality inspection in a manufacturing environment.
---

## 2. Objective
The main objectives of this project are:
- Load and prepare casting product images.
- Classify images into defective and non-defective categories.
- Build a CNN-based image classification model.
- Train and validate the model.
- Evaluate model performance.
- Generate accuracy and loss graphs.
- Generate a confusion matrix.
- Calculate classification metrics.
- Save the trained model.
- Predict the class of new casting product images.
---

## 3. Dataset
The project uses a casting product image dataset containing images of:
1. `def_front` - Defective casting products
2. `ok_front` - Non-defective casting products
The dataset is organized into training and testing directories.

### Dataset Structure
Casting_Defect_Detection/
│
├── data/
│   ├── train/
│   │   ├── def_front/
│   │   └── ok_front/
│   │
│   └── test/
│       ├── def_front/
│       └── ok_front/
│
├── notebooks/
│   └── casting_defect_detection.ipynb
│
├── models/
│   ├── best_casting_defect_model.keras
│   └── casting_defect_model.keras
│
├── reports/
│   ├── accuracy_graph.png
│   ├── loss_graph.png
│   ├── confusion_matrix.png
│   └── findings_report.md
│
├── sample_images/
│   ├── sample_1_non_defective.jpeg
│   ├── sample_2_non_defective.jpeg
│   ├── sample_3_non_defective.jpeg
│   ├── sample_4_non_defective.jpeg
│   └── sample_5_non_defective.jpeg
│
├── requirements.txt
└── README.md

# Environment Setup
Python 3.12 is used for this project because TensorFlow support depends on the Python version.

# Create a virtual environment:
py -3.12 -m venv .venv

# Activate it on Windows:
.venv\Scripts\activate

# Check the Python version:
python --version

# Installation
 Install the required libraries:
pip install -r requirements.txt
The main dependencies are:
tensorflow==2.21.0
numpy
pandas
matplotlib
seaborn
scikit-learn
pillow
jupyter

# Notebook Workflow
The notebook performs the following steps:
Import required libraries.
Set dataset paths.
Check the dataset.
Load training data.
Load validation data.
Load test data.
Display sample images.
Apply data augmentation.
Build the CNN model.
Compile the model.
Train the model.
Plot training and validation accuracy.
Plot training and validation loss.
Evaluate the model.
Generate predictions.
Generate a classification report.
Generate a confusion matrix.
Save the trained model.
Predict individual sample images.

# CNN Model
The CNN model contains:
Input layer
Data augmentation
Rescaling
Convolutional layers
MaxPooling layers
Flatten layer
Dense layer
Dropout layer
Sigmoid output layer

# Images are resized to:
224 × 224 pixels
The output layer uses a sigmoid activation function for binary classification.

# Data Augmentation
The following augmentation techniques are used:
Random horizontal flipping
Random rotation
Random zoom
Random contrast
These techniques help the model generalize better to new images.

# Model Training
The model uses:
Optimizer: Adam
Learning Rate: 0.0001
Loss Function: Binary Crossentropy
Output Activation: Sigmoid

# Callbacks used during training include:
Early Stopping
Model Checkpoint
Reduce Learning Rate on Plateau

# The best model is saved as:
models/best_casting_defect_model.keras

# Model Evaluation
The model is evaluated using:
Accuracy
Precision
Recall
F1 Score
Confusion Matrix
Classification Report

# Generated reports are stored in:
reports/
The following files are generated:
accuracy_graph.png
loss_graph.png
confusion_matrix.png
findings_report.md

# Prediction
The project includes a prediction function for classifying new casting product images.
The prediction provides:
Image name
Predicted class
Defect probability
Recommended action
If the defect probability is greater than or equal to 0.50:
Defective (1)
Send product for manual inspection
Otherwise:
Non-defective (0)
Product may proceed on production line

# Model Output
The model produces a probability value between 0 and 1.
A threshold of 0.50 is used for classification:
Probability >= 0.50 → Defective
Probability < 0.50  → Non-defective

# Results
The actual model performance is recorded in:
reports/findings_report.md
The report contains the accuracy, precision, recall, and F1-score obtained during evaluation.

# Conclusion
This project demonstrates the application of deep learning and computer vision for automated casting product quality inspection.
The CNN model is trained to classify casting images into defective and non-defective categories. The system can provide a prediction and recommend whether a product should proceed on the production line or be sent for manual inspection.

# Future Improvements
Possible improvements include:
Using a larger and more diverse dataset.
Applying transfer learning using MobileNet, ResNet, or EfficientNet.
Performing hyperparameter tuning.
Handling class imbalance.
Improving image preprocessing.
Adding real-time camera-based inspection.
Deploying the model using Streamlit or Flask.
Integrating the system with an industrial production line.

# Author
P.Harshitha-G40 AIML