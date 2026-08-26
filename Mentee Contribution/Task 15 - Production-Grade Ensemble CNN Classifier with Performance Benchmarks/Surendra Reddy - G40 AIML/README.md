# Production-Grade Ensemble CNN Classifier with Performance Benchmarks

## Overview
This project builds three diverse CNN architectures on CIFAR-10, combines their predictions using Majority Voting, Soft Voting, and Weighted Soft Voting, and benchmarks the ensemble against individual models on accuracy, latency, throughput, model size, and robustness to image perturbations.

## Setup

Install dependencies:
pip install -r requirements.txt

Open and run ensemble_cnn_classifier.ipynb top to bottom. CIFAR-10 downloads automatically on first run via Keras.

## Project Structure
Surendra Reddy - G40 AIML/
- ensemble_cnn_classifier.ipynb   (Full pipeline: data, training, ensembling, benchmarking, robustness)
- requirements.txt
- findings_report.md              (Full results, analysis, and answers to required questions)
- models/                         (Three trained .keras models)
- results/                        (Confusion matrices, training curves, and CSV result tables)

## Key Results
- Best individual CNN: CNN Deep (79.61% test accuracy)
- Best ensemble strategy: Weighted Soft Voting (81.56% test accuracy)
- Ensemble improved robustness on rotated, blurred, and noisy images, at the cost of higher latency and larger model size.

See findings_report.md for full metrics, benchmarks, robustness analysis, and answers to all required questions.
