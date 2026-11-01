# Customer Feedback Analysis System

## Overview

This project is a **Customer Feedback Analysis System** that analyzes customer reviews and provides:

* Sentiment classification as **Positive** or **Negative**
* Rule-based **Hybrid Sentiment Analysis** using VADER and keywords
* Feedback **categorization** such as Payment, Performance, Login, and Support
* Extraction of important **keywords**
* Model evaluation using **Accuracy, Classification Report, and Confusion Matrix**

The project combines a machine learning approach using **TF-IDF + Logistic Regression** with a rule-based approach for detailed customer feedback analysis.

---

## Dataset

The project uses two datasets from the Hugging Face `AnkitAI/product-reviews-sentiment` dataset:

* `categorized_text_reviews.csv`
* `synthetic_reviews.csv`

The two datasets are combined into a single dataset.

The final dataset contains **9,000 reviews** with the following columns:

* `review`
* `category`

Example categories include:

* Product Feedback
* Customer Service
* Fraud and Scam
* Operational Issues

---

## Technologies Used

* Python
* Pandas
* Scikit-learn
* VADER Sentiment Analysis
* TF-IDF Vectorization
* Logistic Regression
* Regular Expressions

---

## Project Workflow

```text
Customer Reviews
       |
       v
Load and Combine Datasets
       |
       v
Map Categories to Sentiment
       |
       v
Train/Test Split
       |
       v
TF-IDF Vectorization
       |
       v
Logistic Regression
       |
       v
Sentiment Prediction
       |
       +----------------------+
       |                      |
       v                      v
Model Evaluation       Hybrid Analysis
                              |
                              v
                    VADER + Keywords
                              |
                              v
                    Sentiment + Category
                              |
                              v
                          Keywords
```

---

## 1. Data Loading

The two CSV files are loaded using Pandas and combined using `pd.concat()`.

```python
v1 = pd.read_csv("hf://datasets/AnkitAI/product-reviews-sentiment/categorized_text_reviews.csv")
v2 = pd.read_csv("hf://datasets/AnkitAI/product-reviews-sentiment/synthetic_reviews.csv")

data = pd.concat([v1, v2], ignore_index=True)
```

The resulting dataset contains 9,000 reviews.

---

## 2. Sentiment Label Creation

The original categories are mapped into two sentiment classes.

The following categories are treated as negative:

* Operational Issues
* Fraud and Scam

All other categories are treated as positive.

```python
def get_sentiment(category):
    if category in ['Operational Issues', 'Fraud and Scam']:
        return 'negative'
    else:
        return 'positive'

data['sentiment'] = data['category'].apply(get_sentiment)
```

### Sentiment Distribution

| Sentiment |     Count |
| --------- | --------: |
| Negative  |     4,555 |
| Positive  |     4,445 |
| **Total** | **9,000** |

The classes are relatively balanced.

---

## 3. Train-Test Split

The review text is used as the input and the generated sentiment label is used as the target.

```python
X = data['review']
y = data['sentiment']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
```

The dataset is divided into:

* **7,200 training samples**
* **1,800 testing samples**

---

## 4. TF-IDF + Logistic Regression

A Scikit-learn Pipeline is used to combine TF-IDF vectorization and Logistic Regression.

```python
model = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000
    )),
    ('classifier', LogisticRegression(max_iter=1000))
])
```

### TF-IDF

TF-IDF converts text into numerical features that can be processed by the machine learning model.

The project uses:

* Unigrams and bigrams with `ngram_range=(1, 2)`
* Maximum of 5,000 features

### Logistic Regression

Logistic Regression is used as the classification algorithm to predict:

```text
positive
negative
```

The model is trained using:

```python
model.fit(X_train, y_train)
```

The Pipeline automatically handles the TF-IDF transformation before training the classifier.

---

## 5. Model Evaluation

The trained model is evaluated on the test dataset.

```python
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
```

### Model Accuracy

**Accuracy: 98.44%**

The model correctly classified approximately 98.44% of the test reviews.

---

## Classification Report

The classification report produced by the notebook shows approximately:

| Class    | Precision | Recall | F1-Score |
| -------- | --------: | -----: | -------: |
| Negative |      0.98 |   0.98 |     0.98 |
| Positive |      0.98 |   0.98 |     0.98 |

The overall accuracy in the classification report is approximately **98%**.

---

## Confusion Matrix

The notebook produced the following confusion matrix:

```text
[[910  14]
 [ 14 862]]
```

This indicates that most test samples were classified correctly, with relatively few incorrect predictions.

---

## 6. Prediction on New Feedback

The trained model is also tested on new customer feedback.

Example:

```text
Payment gateway is not working
The application is very slow
I love this app, it's amazing
Customer support was very helpful
App crashes every time I try to login
```

The trained TF-IDF + Logistic Regression pipeline predicts the sentiment of these new reviews.

---

## 7. Hybrid Sentiment Analysis

A separate rule-based hybrid sentiment analysis system is implemented using:

* VADER Sentiment Analyzer
* Negative keywords
* Positive keywords

### Negative Keywords

Examples include:

```text
not working
slow
laggy
crash
failed
terrible
awful
horrible
useless
scam
fraud
```

### Positive Keywords

Examples include:

```text
love
amazing
excellent
awesome
great
perfect
wonderful
fantastic
helpful
quickly
solved
```

The system first counts positive and negative keywords.

If one type of keyword has a higher count, that sentiment is selected.

If the counts are equal, the VADER compound score is used as a tie-breaker.

---

## 8. Complete Feedback Analysis

The `analyze_feedback()` function provides three types of information:

### Sentiment

The review is classified as:

* Positive
* Negative
* Neutral

### Category

The system identifies relevant categories using keywords:

* Payment
* Performance
* Login
* Support
* General

A single review can belong to multiple categories.

For example:

```text
"App crashes every time I try to login"
```

is classified into:

```text
Performance
Login
```

### Keywords

Important words are extracted from the review by:

* Converting text to lowercase
* Splitting the text into words
* Removing short words
* Removing selected common words
* Keeping up to four keywords

---

## Example Final Analysis

For:

```text
Payment failed and app is slow
```

the system produces:

```text
Sentiment: NEGATIVE
Categories: Payment, Performance
Keywords: payment, failed, slow
```

For:

```text
Customer support was very helpful
```

the system produces:

```text
Sentiment: POSITIVE
Categories: Support
Keywords: customer, support, very, helpful
```

---

## Sample Results

The final analysis system was tested with several customer feedback examples.

| Feedback                              | Sentiment | Categories           |
| ------------------------------------- | --------- | -------------------- |
| Payment gateway is not working        | Negative  | Payment              |
| I love this app, it's amazing         | Positive  | General              |
| App crashes every time I try to login | Negative  | Performance, Login   |
| Customer support was very helpful     | Positive  | Support              |
| Payment failed and app is slow        | Negative  | Payment, Performance |

---

## Key Features

* Loads and combines customer review datasets
* Creates sentiment labels from review categories
* Uses TF-IDF for text feature extraction
* Uses Logistic Regression for sentiment classification
* Achieves approximately **98.44% accuracy**
* Uses VADER for rule-based sentiment analysis
* Uses positive and negative keyword matching
* Identifies multiple feedback categories
* Extracts important keywords
* Supports analysis of new customer feedback

---

## Conclusion

This project demonstrates a complete customer feedback analysis workflow combining **machine learning and rule-based NLP techniques**.

The TF-IDF + Logistic Regression model provides high-accuracy sentiment classification, while the hybrid VADER and keyword-based system provides additional interpretability and detailed feedback information such as categories and keywords.

Together, these approaches can help identify customer sentiment and understand the main issues or positive aspects mentioned in customer feedback.
