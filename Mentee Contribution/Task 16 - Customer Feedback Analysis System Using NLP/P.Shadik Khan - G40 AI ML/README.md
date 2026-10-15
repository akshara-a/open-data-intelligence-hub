# Customer Feedback Analysis System Using NLP

## 1. Project Overview

The Customer Feedback Analysis System is an NLP-based application that analyzes customer feedback automatically.

The system identifies:

- Sentiment
- Main complaint category
- Important keywords and phrases
- Text similarity
- Overall meaning of feedback

## 2. Objective

The objective of this project is to apply Natural Language Processing techniques to customer feedback.

The system processes customer comments and classifies them into meaningful categories.

## 3. Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- NLTK
- TF-IDF
- Logistic Regression
- Jupyter Notebook

## 4. Dataset

The dataset contains customer feedback with the following fields:

- ID
- Feedback
- Sentiment
- Category

### Sentiment Labels

- Positive
- Negative
- Neutral

### Category Labels

- Payment
- Login
- Performance
- Support
- UI
- Bug
- Feature Request

## 5. NLP Preprocessing

The following preprocessing techniques are used:

1. Convert text to lowercase
2. Remove URLs
3. Remove numbers
4. Remove punctuation
5. Remove extra spaces

## 6. TF-IDF

TF-IDF is used to convert customer feedback into numerical feature vectors.

The vector representation is used by machine learning models for classification.

## 7. Sentiment Analysis

Logistic Regression is used to classify feedback into:

- Positive
- Negative
- Neutral

## 8. Category Classification

Customer feedback is classified into categories such as:

- Payment
- Login
- Performance
- Support
- UI
- Bug
- Feature Request

## 9. Keyword Extraction

TF-IDF scores are used to identify important words and phrases from customer feedback.

## 10. Text Similarity

Cosine similarity is used to compare the semantic similarity between two feedback messages.

## 11. Model Evaluation

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

## 12. Example

### Input

"The application is very slow and payment failed twice."

### Expected Analysis

Sentiment:
Negative

Categories:
- Performance
- Payment

Important Keywords:
- application
- slow
- payment
- failed

## 13. Project Workflow

Customer Feedback
        |
        v
Text Preprocessing
        |
        v
TF-IDF Vectorization
        |
        +-------------------+
        |                   |
        v                   v
Sentiment Model      Category Model
        |                   |
        +---------+---------+
                  |
                  v
          Keyword Extraction
                  |
                  v
            Final Analysis

## 14. Conclusion

The project demonstrates how NLP and machine learning can be used to automatically analyze customer feedback.

The system provides useful information about customer sentiment, complaints, keywords, and feedback similarity.