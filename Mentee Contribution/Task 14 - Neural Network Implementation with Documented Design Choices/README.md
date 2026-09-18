# Neural Network Implementation with Documented Design Choices

## Project Overview

This project implements an Artificial Neural Network using TensorFlow and Keras for binary classification.

The Breast Cancer Wisconsin dataset is used to train and evaluate the model. The project documents the reasoning behind the dataset preparation, neural network architecture, activation functions, optimizer, loss function, and evaluation metrics.

## Objectives

* Load and prepare a classification dataset.
* Perform data preprocessing and feature scaling.
* Build an Artificial Neural Network using TensorFlow/Keras.
* Train the model using training data.
* Evaluate the model using test data.
* Document the design choices made during implementation.
* Save the trained model and training results.

## Dataset

The Breast Cancer Wisconsin dataset is used in this project.

* Input features: 30 numerical features
* Target: `target`
* Problem type: Binary classification
* Training split: 80%
* Testing split: 20%

The dataset was saved as:

```text
data/breast_cancer_dataset.csv
```

## Technologies Used

* Python
* TensorFlow
* Keras
* NumPy
* Pandas
* Matplotlib
* Scikit-learn
* Jupyter Notebook

## Project Structure

```text
Task 14 - Neural Network Implementation with Documented Design Choices
│
├── data
│   └── breast_cancer_dataset.csv
│
├── models
│   └── breast_cancer_neural_network.keras
│
├── notebooks
│   └── neural_network_implementation.ipynb
│
├── outputs
│   └── training_accuracy.png
│
├── src
│
└── README.md
```

## Preprocessing

The following preprocessing steps were performed:

1. Separated input features and target values.
2. Divided the dataset into training and testing sets.
3. Used stratified splitting to preserve class distribution.
4. Applied `StandardScaler` to standardize the input features.

## Neural Network Architecture

The model contains:

1. Input layer with 30 features.
2. Dense layer with 32 neurons and ReLU activation.
3. Dropout layer with a rate of 0.2.
4. Dense layer with 16 neurons and ReLU activation.
5. Output layer with one neuron and sigmoid activation.

## Design Choices

### ReLU Activation

ReLU was used in the hidden layers to introduce non-linearity and support efficient training.

### Sigmoid Activation

Sigmoid was used in the output layer because the project is a binary classification problem.

### Binary Cross-Entropy

Binary cross-entropy was selected as the loss function because the target contains two classes.

### Adam Optimizer

Adam was selected because it adapts the learning rate during training.

### Dropout

A dropout rate of 0.2 was used to help reduce overfitting.

### Training Configuration

* Epochs: 30
* Batch size: 32
* Validation split: 20%
* Learning rate: 0.001

## Evaluation

The model was evaluated using:

* Test accuracy
* Precision
* Recall
* F1-score
* Classification report
* Confusion matrix
* Training and validation accuracy plot

## Output Files

The project saves:

```text
models/breast_cancer_neural_network.keras
outputs/training_accuracy.png
```

## How to Run

### 1. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Open the notebook

Open the notebook inside the `notebooks` folder and run the cells in order.

## Conclusion

This project demonstrates the implementation of a basic Artificial Neural Network for binary classification. It also explains the reasoning behind the preprocessing steps, model architecture, training configuration, and evaluation methods.
