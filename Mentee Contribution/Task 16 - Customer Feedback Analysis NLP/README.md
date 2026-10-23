# Customer Feedback Analysis System Using NLP

## Overview

This project analyzes customer feedback using Natural Language Processing and Machine Learning.

The system predicts:

- Customer sentiment
- Feedback category
- Important keywords

## Features

- Text cleaning
- Lowercase conversion
- Punctuation removal
- Stop-word removal
- TF-IDF vectorization
- Unigram and bigram extraction
- Sentiment classification
- Category classification
- Keyword extraction
- Model evaluation
- Streamlit web application

## Technologies Used

- Python
- Pandas
- Scikit-learn
- TF-IDF
- Logistic Regression
- Streamlit
- Joblib

## Project Structure

```text
Task 16 - Customer Feedback Analysis NLP
│
├── data
│   └── feedback.csv
├── models
│   ├── sentiment_model.pkl
│   └── category_model.pkl
├── notebooks
├── outputs
├── src
│   ├── preprocessing.py
│   ├── train_models.py
│   ├── predict.py
│   └── keyword_extractor.py
├── app.py
├── requirements.txt
└── README.md