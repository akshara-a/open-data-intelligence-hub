# Bank Customer Churn Prediction

A complete end-to-end bank customer churn prediction project using Python, machine learning, and Flask.

## Project Overview

This project uses the Kaggle Bank Customer Churn dataset (`Churn_Modelling.csv`) to predict whether a customer will leave the bank.

Features:
- Data loading, preprocessing, and exploratory data analysis (EDA)
- Feature engineering and importance analysis
- Model training and comparison across Logistic Regression, Decision Tree, Random Forest, KNN, and SVM
- Hyperparameter tuning with GridSearchCV
- Evaluation using Accuracy, Precision, Recall, F1-score, ROC-AUC, confusion matrix, and ROC curve
- Best model saved with Joblib
- Flask web app for real-time churn prediction

## Folder Structure

- `data/` - dataset folder
- `notebooks/` - analysis notebooks
- `src/` - source code
  - `app/` - Flask web application
  - `models/` - model training and utilities

## Setup

1. Clone or download the repository.
2. Place `Churn_Modelling.csv` in the `data/` folder.
3. Create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

4. If you do not have the dataset locally, download it with the Kaggle CLI:

```bash
python download_data.py
```

> Ensure your Kaggle API token is configured in `~/.kaggle/kaggle.json` before running the download script.

## Usage

### Training and evaluation

Run the training script:

```bash
python src/models/train_model.py
```

The script will save the best trained model to `src/models/best_model.joblib`.

### Flask app

Run the web app from the project root:

```bash
python src/app/app.py
```

Open `http://127.0.0.1:5000` in your browser and submit customer inputs.

## Notes

- The dataset must be stored at `data/Churn_Modelling.csv`.
- For a portfolio, include screenshots of the EDA and model evaluation results.
