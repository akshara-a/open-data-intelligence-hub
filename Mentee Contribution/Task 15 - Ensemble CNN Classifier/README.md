@"
# Task 15 - Ensemble CNN Classifier

## Project Overview

This project implements an Ensemble CNN Classifier using the MNIST handwritten digit dataset.

Two different Convolutional Neural Network models are trained independently. Their prediction probabilities are combined by averaging the predictions.

The final class is selected using the highest ensemble probability.

## Objectives

- Train two different CNN models.
- Compare the performance of individual CNN models.
- Combine model predictions using ensemble learning.
- Measure prediction speed.
- Test model robustness using noisy images.

## Technologies Used

- Python
- TensorFlow
- Keras
- NumPy
- Convolutional Neural Networks
- Ensemble Learning
- MNIST Dataset

## Dataset

The project uses the MNIST handwritten digit dataset.

Dataset details:

- Training images: 10,000
- Test images: 2,000
- Image size: 28 × 28 pixels
- Number of classes: 10
- Classes: Digits 0 to 9

## CNN Models

### CNN Model 1

- One convolutional layer
- One max pooling layer
- Flatten layer
- Dense layer
- Output layer with 10 classes

### CNN Model 2

- Two convolutional layers
- Two max pooling layers
- Flatten layer
- Dense layer
- Output layer with 10 classes

## Ensemble Method

The predictions from both CNN models are averaged.

```text
Ensemble Prediction = (Model 1 Prediction + Model 2 Prediction) / 2