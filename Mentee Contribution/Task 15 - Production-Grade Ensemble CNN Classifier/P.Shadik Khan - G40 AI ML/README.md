# Task 15 - Production-Grade Ensemble CNN Classifier

## Student
P.Shadik Khan - G40 AI ML

## Project Overview
This project implements a production-oriented ensemble CNN classifier for binary image classification of casting products. The objective is to classify casting images into defective and non-defective categories using multiple CNN models and an ensemble prediction approach.

## Project Structure
- data/: Training, validation and test image data
- models/: Trained CNN models
- results/: Evaluation, benchmark and robustness results
- src/: Source code for preprocessing, training, evaluation and prediction
- notebooks/: Experiment notebooks

## Models
The project includes three CNN architectures:
1. Baseline CNN
2. Regularized CNN
3. Deep CNN

The trained models are combined for ensemble prediction.

## Dataset
The dataset contains casting product images classified into:
- Defective
- Non-defective

The data is divided into training, validation and test sets.

## Key Evaluation Results
The ensemble was evaluated on 197 test images.

- Accuracy: 0.6396
- Precision: 1.0000
- Recall: 0.1013
- F1 Score: 0.1839

## Benchmark Results
The baseline CNN provided the fastest inference performance at approximately 3.32 milliseconds per image and approximately 301.5 images per second.

## Robustness Testing
The ensemble was tested under:
- Gaussian noise
- Brightness variation
- Horizontal flipping

Detailed results are available in results/robustness_results.csv.

## How to Run
Install dependencies:
pip install -r requirements.txt

Train models:
python -m src.train

Run ensemble prediction:
python -m src.ensemble

Evaluate:
python -m src.evaluate

Run benchmark:
python -m src.benchmark

Run robustness testing:
python -m src.robustness_test

## Important Limitation
The current ensemble achieves moderate overall accuracy but low recall for one class. Further class balancing, threshold tuning and model improvement are recommended before real production deployment.
