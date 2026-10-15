# ❤️ Heart Disease Dataset

## Overview

This repository contains the **Heart Disease Dataset**, which is commonly used for machine learning classification tasks to predict whether a patient has heart disease based on various medical attributes.

The dataset is suitable for:
- Data Analysis
- Data Visualization
- Machine Learning
- Classification Algorithms
- Healthcare Analytics

---

## Dataset Information

- **File:** `heart.csv`
- **Rows:** 1,025
- **Columns:** 14
- **Target Variable:** `target`

### Features

| Column | Description |
|---------|-------------|
| age | Age of the patient |
| sex | Gender (1 = Male, 0 = Female) |
| cp | Chest pain type |
| trestbps | Resting blood pressure |
| chol | Serum cholesterol (mg/dl) |
| fbs | Fasting blood sugar (>120 mg/dl) |
| restecg | Resting electrocardiographic results |
| thalach | Maximum heart rate achieved |
| exang | Exercise-induced angina |
| oldpeak | ST depression induced by exercise |
| slope | Slope of the peak exercise ST segment |
| ca | Number of major vessels colored by fluoroscopy |
| thal | Thalassemia |
| target | Heart disease (1 = Present, 0 = Absent) |

---

## Objective

The goal of this dataset is to build a machine learning model capable of predicting whether a patient has heart disease using their medical information.

---

## Possible Machine Learning Models

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Naive Bayes
- XGBoost
- Neural Networks

---

## Example Workflow

1. Load the dataset.
2. Perform data cleaning and preprocessing.
3. Explore the data using visualization.
4. Split data into training and testing sets.
5. Train machine learning models.
6. Evaluate model performance.
7. Predict heart disease for new patients.

---

## Requirements

Install the required Python libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

---

## Loading the Dataset

```python
import pandas as pd

df = pd.read_csv("heart.csv")

print(df.head())
```

---

## Target Classes

| Value | Meaning |
|-------|---------|
| 0 | No Heart Disease |
| 1 | Heart Disease |

---

## Project Structure

```
.
├── heart.csv
└── README.md
```

---

## License

This dataset is intended for educational and research purposes.

---

## Acknowledgements

This dataset is widely used in machine learning and healthcare analytics for heart disease prediction and educational demonstrations.