# Customer Feedback Analysis System Using NLP

## 1. Project Title
Customer Feedback Analysis System Using NLP

## 2. Project Description
This project is a beginner-friendly Natural Language Processing (NLP) mini project that analyzes customer feedback and predicts:

- Sentiment: Positive, Negative, or Neutral
- Feedback categories: Payment, Login, Performance, Support, UI, Bug, Feature Request
- Important keywords and phrases

The solution uses common NLP and machine learning techniques such as text cleaning, tokenization, TF-IDF vectorization, n-grams, and logistic regression models.

## 3. Objective
The main goal is to classify customer feedback automatically and help teams understand the most common issues and positive experiences from user reviews.

## 4. Features
- Clean and normalize raw text feedback
- Remove unnecessary punctuation and extra spaces
- Preserve important negation words like `not`, `no`, and `never`
- Train sentiment classification model
- Train multi-label category classification model
- Extract top keywords and phrases using TF-IDF
- Build an interactive end-to-end app via `main.py`
- Visualize exploratory data analysis with Matplotlib and Seaborn

## 5. NLP Concepts Used
- Text preprocessing
- Lowercasing
- Tokenization
- Stop-word removal
- Lemmatization
- TF-IDF vectorization
- N-grams (unigrams and bigrams)
- Multi-label classification
- Keyword extraction
- Sentiment analysis

## 6. Technologies Used
- Python
- Pandas
- NumPy
- NLTK
- scikit-learn
- Matplotlib
- Seaborn
- Joblib
- Jupyter Notebook

## 7. Project Folder Structure
```text
customer-feedback-analysis/
├── data/
│   └── feedback.csv
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_tfidf_model.ipynb
│   ├── 03_sentiment_analysis.ipynb
│   ├── 04_category_classification.ipynb
│   └── 05_model_evaluation.ipynb
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── sentiment_model.py
│   ├── category_model.py
│   └── keyword_extractor.py
├── models/
│   ├── sentiment_model.pkl
│   ├── category_model.pkl
│   └── multilabel_binarizer.pkl
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 8. Installation Steps
1. Open a terminal in the project folder.
2. Create a virtual environment if needed:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 9. How to Run the Project
### Train the models
```bash
python src/sentiment_model.py
python src/category_model.py
```

### Run the interactive feedback analysis app
```bash
python main.py
```

### Example input
```text
The application is very slow and payment failed twice.
```

### Example output
```text
====================================
CUSTOMER FEEDBACK ANALYSIS
====================================

Feedback:
The application is very slow and payment failed twice.

Sentiment:
Negative

Categories:
- Performance
- Payment

Important Keywords:
- application slow
- payment failed
- payment
- slow
====================================
```

## 10. Model Evaluation
The project evaluates:

- Accuracy
- Precision
- Recall
- F1 Score
- Classification report
- Confusion matrix for sentiment
- Micro and macro metrics for category classification

## 11. Future Improvements
- Add more customer feedback samples
- Add a bigger custom vocabulary
- Try other models such as Naive Bayes or SVM
- Add a manual review dashboard
- Include confidence scores for predictions
- Use a more advanced real-world dataset

## 12. Project Summary
This project demonstrates how machine learning and NLP can be applied to real business problems. It is suitable for student projects, classroom demonstrations, and simple portfolio work.
