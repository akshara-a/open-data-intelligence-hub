# Task 13 - Casting Defect Detection CNN

## Project Overview

This project uses a Convolutional Neural Network (CNN) to classify casting images into two categories:

- Defective Casting
- OK Casting

A Streamlit application is included for image prediction.

## Objectives

- Detect defects in casting images.
- Train a CNN image classification model.
- Evaluate the model using test images.
- Create an image prediction application.

## Technologies Used

- Python
- TensorFlow
- Keras
- CNN
- NumPy
- Matplotlib
- Pillow
- Streamlit

## Dataset

The dataset contains two classes:

- `def_front`
- `ok_front`

The dataset used in this project contains:

| Dataset | Images |
|---|---:|
| Training | 1041 |
| Validation | 259 |
| Testing | 1300 |
| Total | 2600 |

## Model Architecture

The CNN contains:

1. Convolutional layer with 32 filters
2. Max pooling layer
3. Convolutional layer with 64 filters
4. Max pooling layer
5. Convolutional layer with 128 filters
6. Max pooling layer
7. Flatten layer
8. Dense layer with 128 neurons
9. Dropout layer
10. Sigmoid output layer

## Model Results

| Metric | Result |
|---|---:|
| Training Accuracy | 91.35% |
| Validation Accuracy | 89.58% |
| Test Accuracy | 93.31% |
| Test Loss | 0.1680 |

## Project Structure

```text
Task 13 - Casting Defect Detection CNN
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data
│   └── casting_data
│       ├── train
│       │   ├── def_front
│       │   └── ok_front
│       └── test
│           ├── def_front
│           └── ok_front
│
├── models
│   └── casting_defect_cnn.keras
│
├── reports
│   ├── training_accuracy.png
│   └── training_loss.png
│
└── src
    ├── data_preparation.py
    └── train_model.py