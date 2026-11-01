# Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP

## Overview
This project builds a simple NLP-based machine learning model that classifies a sentence or review into one of three sentiment categories: Positive, Neutral, or Negative. It also includes error analysis to understand why the model gives incorrect predictions.

## Tools and Libraries
- pandas
- numpy
- matplotlib
- scikit-learn

## Methodology
1. Load the dataset
2. Clean the text (lowercase, remove URLs, special characters)
3. Train-Test Split (80% training, 20% testing)
4. Convert text into numerical features using TF-IDF
5. Train a Logistic Regression model
6. Predict sentiment
## Model Evaluation Results
After running the script on our dataset, the model achieved the following performance metrics:

- **Model Accuracy**: 75.0%

**Classification Report**:
```
              precision    recall  f1-score   support

    negative       1.00      1.00      1.00         1
     neutral       0.67      1.00      0.80         2
    positive       0.00      0.00      0.00         1

    accuracy                           0.75         4
   macro avg       0.56      0.67      0.60         4
weighted avg       0.58      0.75      0.65         4
```

## Error Analysis Findings
The error analysis often reveals issues with:
- Negation
- Mixed opinions
- Neutral sentiment
- Sarcasm
- Rare vocabulary
