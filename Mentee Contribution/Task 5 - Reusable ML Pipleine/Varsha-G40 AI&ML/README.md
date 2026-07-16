# Customer Churn Prediction Pipeline

## Project Overview

This project implements a reusable machine learning pipeline using Scikit-learn to predict customer churn.

## Dataset

Telco Customer Churn Dataset

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib

## Project Structure

customer-churn-pipeline/

├── data/

│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv

├── models/

│   └── churn_pipeline.pkl

├── src/

│   ├── train.py

│   └── predict.py

├── requirements.txt

└── README.md

## Pipeline Workflow

1. Load dataset
2. Clean data
3. Handle missing values
4. Encode categorical features
5. Scale numerical features
6. Train Random Forest Classifier
7. Evaluate model performance
8. Save trained pipeline
9. Predict customer churn

## Model Performance

Accuracy: 79.4%

## Run Training

python src/train.py

## Run Prediction

python src/predict.py

## Sample Output

Prediction: No
