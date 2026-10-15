# ❤️ Optimized Classification Model with Feature Importance Analysis

## 📌 Project Overview

This project focuses on developing an optimized machine learning classification model to predict heart disease using patient medical information.

The system uses a **Random Forest Classification algorithm** with data preprocessing and feature importance analysis to identify the major factors affecting heart disease prediction.

The project includes:
- Data preprocessing
- Machine learning model training
- Model evaluation
- Feature importance analysis
- Streamlit web application deployment


## 🎯 Objectives

- Build an accurate heart disease prediction system.
- Apply machine learning techniques for classification.
- Analyze important features influencing predictions.
- Create an interactive Streamlit application.
- Improve understanding of medical risk factors using feature importance.


## 📂 Project Structure

```
Optimized Classification Model with Feature Importance Analysis
│
├── app.py
├── train_model.py
├── README.md
├── requirements.txt
│
├── data
│   └── heart.csv
│
├── models
│   ├── heart_model.pkl
│   └── scaler.pkl
│
└── notebooks
    └── EDA.ipynb
```


## 📊 Dataset Description

The project uses the **Heart Disease Dataset** containing medical attributes of patients.

### Features:

| Feature | Description |
|--------|-------------|
| age | Age of patient |
| sex | Gender |
| cp | Chest pain type |
| trestbps | Resting blood pressure |
| chol | Cholesterol level |
| fbs | Fasting blood sugar |
| restecg | Resting ECG results |
| thalach | Maximum heart rate |
| exang | Exercise induced angina |
| oldpeak | ST depression |
| slope | Slope of peak exercise ST segment |
| ca | Number of major vessels |
| thal | Thalassemia |

### Target Variable:

```
target
```

Values:

- 0 → No Heart Disease
- 1 → Heart Disease


## 🛠️ Technologies Used

### Programming Language
- Python

### Libraries

- Pandas
- NumPy
- Scikit-learn
- Joblib
- Matplotlib
- Seaborn
- Streamlit


## 🤖 Machine Learning Model

### Random Forest Classifier

Random Forest is used because it:

- Provides high accuracy
- Handles complex patterns
- Reduces overfitting
- Provides feature importance scores


## ⚙️ Machine Learning Workflow

```
Dataset
   |
   ↓
Data Preprocessing
   |
   ↓
Feature Scaling
   |
   ↓
Train-Test Split
   |
   ↓
Random Forest Classification
   |
   ↓
Model Evaluation
   |
   ↓
Feature Importance Analysis
   |
   ↓
Streamlit Deployment
```


## 📈 Model Evaluation

The model performance is evaluated using:

- Accuracy Score
- Precision
- Recall
- F1 Score
- Classification Report


Evaluation Example:

```
Accuracy: 90%+
```


## 🔍 Feature Importance Analysis

Feature importance analysis helps identify which medical factors contribute most to heart disease prediction.

Important features include:

- Chest pain type
- Maximum heart rate
- ST depression
- Age
- Cholesterol
- Exercise induced angina


## 🚀 Installation and Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
```

### Step 2: Navigate to Project Folder

```bash
cd Optimized-Classification-Model-with-Feature-Importance-Analysis
```

### Step 3: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```


## 🏋️ Train the Model

Run:

```bash
python train_model.py
```

After training, the following files will be created:

```
models/
│
├── heart_model.pkl
└── scaler.pkl
```


## ▶️ Run Streamlit Application

Run:

```bash
streamlit run app.py
```

Application URL:

```
http://localhost:8501
```


## 🖥️ Application Features

✅ Heart disease prediction  
✅ Patient health input interface  
✅ Machine learning based classification  
✅ Feature importance visualization  
✅ Interactive Streamlit dashboard  


## 🔮 Future Enhancements

- Add XGBoost and compare multiple algorithms
- Implement hyperparameter optimization
- Add SHAP explainability
- Deploy using Streamlit Cloud
- Add patient prediction history
- Improve dashboard visualization


## 👩‍💻 Author

**Shaik Aiesha**

B.Tech Computer Science Engineering  
Artificial Intelligence & Machine Learning


## ⭐ Acknowledgement

This project is developed for educational purposes to demonstrate machine learning classification, model optimization, and feature importance analysis.