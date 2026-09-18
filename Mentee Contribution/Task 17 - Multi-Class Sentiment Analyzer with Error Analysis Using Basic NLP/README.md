# Task 17 - Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP

## Project Overview

This project is a multi-class sentiment analysis system that classifies text into three categories:

- Positive
- Neutral
- Negative

The project uses basic Natural Language Processing techniques and Machine Learning.

## Objectives

- Clean and preprocess text data.
- Convert text into numerical features using TF-IDF.
- Train a Logistic Regression classifier.
- Predict positive, neutral, and negative sentiments.
- Evaluate model performance.
- Analyze incorrectly classified sentences.
- Build a Streamlit web application.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Joblib
- Streamlit
- TF-IDF
- Logistic Regression

## Project Structure

```text
Task 17 - Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP
│
├── app.py
├── README.md
├── requirements.txt
│
├── data
│   └── sentiment_data.csv
│
├── models
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── outputs
│   ├── classification_report.txt
│   ├── confusion_matrix.png
│   ├── error_analysis.csv
│   ├── error_counts.csv
│   └── sentiment_distribution.png
│
└── src
    ├── predict.py
    └── sentiment_analysis.py