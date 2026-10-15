# Production-Grade Ensemble CNN Classifier with Performance Benchmarks

## 1. Project Overview

This project implements an image classification system using three different Convolutional Neural Network (CNN) architectures and ensemble prediction methods.

The project compares individual CNN models with ensemble methods using performance, robustness, and resource-utilization metrics.

## 2. Objective

The main objectives are:

- Build three different CNN architectures.
- Train and evaluate the CNN models.
- Combine CNN predictions using ensemble methods.
- Compare accuracy, precision, recall, and F1-score.
- Measure model parameters, model size, latency, throughput, and memory usage.
- Analyze model robustness under different image conditions.
- Analyze prediction disagreement between CNN models.
- Identify the most suitable model for deployment.

## 3. Dataset

The project uses the CIFAR-10 image classification dataset.

Due to hardware and training-time constraints, a subset of CIFAR-10 was used.

Dataset configuration:

- Total images: 2,000
- Training images: 1,600
- Validation images: 200
- Test images: 200
- Classes: 10
- Image size: 32 × 32 pixels

The subset was used to make the project practical on limited hardware.

## 4. CNN Models

### CNN1 - Baseline CNN

The baseline model contains:

- Conv2D
- ReLU activation
- MaxPooling
- Conv2D
- ReLU activation
- MaxPooling
- Flatten
- Dense layer
- Output layer

### CNN2 - Regularized CNN

The regularized model contains:

- Conv2D
- Batch Normalization
- ReLU
- MaxPooling
- Dropout
- Conv2D
- Batch Normalization
- ReLU
- MaxPooling
- Dropout
- Dense layer
- Output layer

### CNN3 - Deep CNN

The deeper model contains:

- Multiple convolution layers
- Batch Normalization
- MaxPooling
- Global Average Pooling
- Dense layer
- Output layer

## 5. Training Configuration

The models were trained using:

- Optimizer: Adam
- Learning rate: 0.001
- Batch size: 64
- Maximum epochs: 5
- Image size: 32 × 32
- Early stopping
- Data augmentation during training

## 6. Ensemble Methods

Two ensemble approaches were evaluated:

### Majority Voting

Each CNN provides a predicted class. The final prediction is selected using the majority of model predictions.

### Soft Voting

The probability outputs from the CNN models are combined to obtain the final prediction.

## 7. Evaluation Metrics

The following metrics were used:

- Accuracy
- Precision
- Recall
- F1-score
- Model parameters
- Model size
- Inference latency
- Throughput
- Memory usage
- Robustness
- Prediction disagreement

## 8. Performance Comparison

The final comparison is available in:

`results/final_comparison.csv`

Performance graphs are available in:

`results/plots/`

The graphs compare:

- Accuracy
- Precision
- Recall
- F1-score
- Parameters
- Model size
- Latency
- Throughput
- Memory usage

## 9. Robustness Analysis

The models were tested under different image conditions:

- Original
- Noisy
- Darkened
- Brightened
- Blurred
- Rotated

The results are available in:

`results/final_robustness_summary.csv`

and

`results/robustness_results.csv`

## 10. Disagreement Analysis

Prediction disagreement between the CNN models was analyzed to understand how differently the architectures classify the same images.

The analysis includes:

- Agreement rate
- Overall disagreement rate
- CNN1 vs CNN2 disagreement
- CNN1 vs CNN3 disagreement
- CNN2 vs CNN3 disagreement
- Average prediction confidence

Results are available in:

`results/final_disagreement_analysis.csv`

## 11. Project Structure

```text
ensemble-cnn-classifier/
│
├── data/
│
├── models/
│   ├── cnn_baseline.keras
│   ├── cnn_regularized.keras
│   └── cnn_deep.keras
│
├── results/
│   ├── individual_model_results.csv
│   ├── ensemble_results.csv
│   ├── ensemble_predictions.csv
│   ├── benchmark_results.csv
│   ├── robustness_results.csv
│   ├── disagreement_results.csv
│   ├── disagreement_summary.csv
│   ├── final_comparison.csv
│   ├── final_robustness_summary.csv
│   ├── final_disagreement_analysis.csv
│   │
│   └── plots/
│       ├── accuracy_comparison.png
│       ├── precision_comparison.png
│       ├── recall_comparison.png
│       ├── f1_comparison.png
│       ├── parameter_comparison.png
│       ├── model_size_comparison.png
│       ├── latency_comparison.png
│       ├── throughput_comparison.png
│       └── memory_comparison.png
│
├── src/
│   ├── data_loader.py
│   ├── final_comparison.py
│   ├── generate_plots.py
│   └── final_analysis.py
│
├── requirements.txt
└── README.md