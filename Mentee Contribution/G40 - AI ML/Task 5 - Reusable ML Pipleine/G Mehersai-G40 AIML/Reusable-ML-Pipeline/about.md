# Reusable ML Pipeline using Random Forest Classifier

## Overview

This project demonstrates how to build a **Reusable Machine Learning Pipeline** using the Titanic dataset. The pipeline automates the complete machine learning workflow, including data preprocessing, model training, evaluation, and prediction.

Instead of writing separate code for each task, all preprocessing and modeling steps are combined into a single reusable pipeline using Scikit-learn's `Pipeline` and `ColumnTransformer`.

---

## Objective

The objective of this project is to build a reusable and maintainable machine learning workflow that can be applied to new data without rewriting preprocessing and training code.

---

## Dataset

**Dataset:** Titanic Survival Prediction

The dataset contains passenger information such as:

* Passenger Class (Pclass)
* Sex
* Age
* Number of Siblings/Spouses (SibSp)
* Number of Parents/Children (Parch)
* Fare
* Embarked Port
* Survival Status (Target Variable)

Target Variable:

* **Survived**

  * 0 → Did Not Survive
  * 1 → Survived

---

## Machine Learning Workflow

```
Load Dataset
      ↓
Data Validation
      ↓
Handle Missing Values
      ↓
Encode Categorical Features
      ↓
Scale Numerical Features
      ↓
Train Random Forest Classifier
      ↓
Evaluate Model
      ↓
Predict New Passenger
```

---

## Features Implemented

* Data Loading
* Data Validation
* Missing Value Handling using `SimpleImputer`
* Categorical Encoding using `OneHotEncoder`
* Numerical Feature Scaling using `StandardScaler`
* Reusable ML Pipeline using `Pipeline`
* Feature Transformation using `ColumnTransformer`
* Random Forest Classification
* Model Evaluation
* Prediction on New Data

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn

---

## Project Structure

```
Reusable-ML-Pipeline/
│
├── data/
│   └── titanic.csv
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd Reusable-ML-Pipeline
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Execute:

```bash
python main.py
```

The program will:

* Load the Titanic dataset
* Validate required columns
* Build the preprocessing pipeline
* Train the Random Forest model
* Evaluate model performance
* Predict the survival of a sample passenger

---

## Libraries Used

* pandas
* numpy
* scikit-learn

---

## Learning Outcomes

Through this project, I learned:

* How reusable ML pipelines simplify machine learning workflows.
* How to automate preprocessing using `Pipeline`.
* How to process numerical and categorical features using `ColumnTransformer`.
* How to handle missing values with `SimpleImputer`.
* How to encode categorical variables using `OneHotEncoder`.
* How to train and evaluate a `RandomForestClassifier`.
* How to build machine learning projects that are organized, reusable, and suitable for real-world applications.

---

## Future Improvements

* Add feature engineering (e.g., Family Size, Title extraction)
* Perform hyperparameter tuning using GridSearchCV
* Save the trained model using Joblib
* Deploy the pipeline using Flask or FastAPI
* Add cross-validation for better model evaluation

---

## Conclusion

This project demonstrates the importance of reusable machine learning pipelines in building maintainable and production-ready ML applications. By combining preprocessing and model training into a single workflow, the pipeline reduces manual effort, improves consistency, and can be reused with new datasets without modifying the code.
