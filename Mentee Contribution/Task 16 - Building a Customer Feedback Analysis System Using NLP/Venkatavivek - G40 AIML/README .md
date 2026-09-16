# Customer Feedback NLP

An NLP-based customer feedback analysis system that automatically analyzes customer feedback and extracts useful information such as **sentiment, category, keywords, and semantic similarity**.

The project uses traditional Machine Learning techniques such as **TF-IDF and Logistic Regression**, along with modern **Transformer-based NLP models and Sentence Transformers**.

---

## Features

The system provides the following capabilities:

- Text preprocessing
- Sentiment classification
- Customer feedback category classification
- Keyword extraction
- Text embeddings
- Semantic similarity
- Transformer-based sentiment classification
- Model saving and loading
- Reusable Python modules

---

## Project Pipeline

```text
                    Customer Feedback
                           |
                           v
                  Text Preprocessing
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          Sentiment     Category      Keywords
             |             |             |
             v             v             v
       TF-IDF + LR    TF-IDF + LR    TF-IDF
             |
             v
        Classification


              Customer Feedback
                     |
                     v
            Sentence Transformer
                     |
                     v
               Embeddings
                     |
                     v
            Semantic Similarity
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Joblib
- Sentence Transformers
- Hugging Face Transformers
- Hugging Face Datasets
- PyTorch
- Jupyter Notebook

---

## Machine Learning Models

### 1. Sentiment Classification

The sentiment classifier predicts one of three classes:

```text
positive
negative
neutral
```

Pipeline:

```text
Feedback
   ↓
Preprocessing
   ↓
TF-IDF
   ↓
Logistic Regression
   ↓
Sentiment
```

---

### 2. Category Classification

The category classifier predicts one of seven customer-feedback categories:

```text
payment
login
performance
support
ui
bug
feature_request
```

Pipeline:

```text
Feedback
   ↓
Preprocessing
   ↓
TF-IDF
   ↓
Logistic Regression
   ↓
Category
```

---

### 3. Keyword Extraction

The keyword extractor identifies important words and phrases from customer feedback using TF-IDF scores.

Example:

```text
Input:
"The payment failed twice and the checkout page was extremely slow."

Output:
payment
failed
checkout
slow
```

---

### 4. Text Embeddings

The project uses Sentence Transformers to convert text into numerical vectors.

Example:

```text
"My payment failed"
        ↓
Sentence Transformer
        ↓
[0.123, -0.421, 0.762, ...]
```

These embeddings can be used for:

- Semantic similarity
- Similar feedback detection
- Duplicate feedback detection
- Feedback search
- Clustering
- Recommendation systems

---

### 5. Transformer-based Sentiment Analysis

The project also demonstrates Transformer-based NLP using:

```text
DistilBERT
```

Pipeline:

```text
Text
 ↓
Tokenizer
 ↓
DistilBERT
 ↓
Classification Layer
 ↓
negative / neutral / positive
```

This is implemented in:

```text
notebooks/05_transformers.ipynb
```

---

## Dataset

The project uses a customer-feedback dataset containing processed text and labels.

Important columns include:

```text
processed_text
sentiment
category
```

### Sentiment labels

```text
positive
negative
neutral
```

### Category labels

```text
payment
login
performance
support
ui
bug
feature_request
```

> Note: If synthetic data is used for experimentation, very high accuracy should not be interpreted as equivalent performance on real-world customer feedback.

---

## Project Structure

```text
customer-feedback-nlp/
│
├── data/
│   ├── raw_feedback.csv
│   └── processed_feedback.csv
│
├── models/
│   ├── sentiment_model.pkl
│   ├── sentiment_tfidf.pkl
│   ├── category_model.pkl
│   └── category_tfidf.pkl
│
├── notebooks/
│   ├── 01_text_preprocessing.ipynb
│   ├── 02_tfidf.ipynb
│   ├── 03_sentiment.ipynb
│   ├── 04_category_classification.ipynb
│   ├── 05_transformers.ipynb
│   └── 06_multilabel_classification.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── sentiment.py
│   ├── category_classifier.py
│   ├── keyword_extractor.py
│   └── embeddings.py
│
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd customer-feedback-nlp
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Preprocessing

Run the preprocessing module:

```bash
python src/preprocessing.py
```

This processes the raw customer feedback and creates:

```text
data/processed_feedback.csv
```

---

## Train Sentiment Model

Run:

```bash
python src/sentiment.py
```

The script:

1. Loads the processed dataset
2. Splits the data
3. Creates TF-IDF features
4. Trains Logistic Regression
5. Evaluates the model
6. Saves the trained model

The following files will be created:

```text
models/sentiment_model.pkl
models/sentiment_tfidf.pkl
```

---

## Train Category Model

Run:

```bash
python src/category_classifier.py
```

The following files will be created:

```text
models/category_model.pkl
models/category_tfidf.pkl
```

---

## Keyword Extraction

Run:

```bash
python src/keyword_extractor.py
```

Example:

```text
Feedback:
The payment page is extremely slow and the transaction keeps failing.

Important keywords:
- payment
- transaction
- failing
- slow
- page
```

---

## Embeddings

Run:

```bash
python src/embeddings.py
```

The module generates semantic embeddings using:

```text
all-MiniLM-L6-v2
```

It can also calculate similarity between two feedback messages.

Example:

```text
"My payment failed during checkout."

"The transaction did not work when I tried to buy something."
```

The two sentences should have relatively high semantic similarity even though they use different words.

---

# Using the Sentiment Model

After training the model, you can predict new feedback:

```python
from src.sentiment import predict_sentiment

feedback = "My application keeps crashing."

result = predict_sentiment(feedback)

print(result)
```

Example output:

```text
negative
```

---

# Using the Category Model

```python
from src.category_classifier import predict_category

feedback = "I cannot log into my account."

result = predict_category(feedback)

print(result)
```

Example output:

```text
login
```

---

# Example Predictions

| Customer Feedback | Sentiment | Category |
|---|---|---|
| My payment failed twice | negative | payment |
| I cannot log into my account | negative | login |
| The application takes too long to load | negative | performance |
| The support team solved my issue | positive | support |
| The new interface looks confusing | negative | ui |
| The application crashes when I open it | negative | bug |
| Please add dark mode | neutral | feature_request |

---

# TF-IDF

TF-IDF stands for:

**Term Frequency – Inverse Document Frequency**

It represents text numerically based on how important a word is within a document and across the dataset.

The project uses:

```python
TfidfVectorizer(
    ngram_range=(1, 2)
)
```

This means both unigrams and bigrams are considered.

Example:

```text
payment
payment failed
failed
failed transaction
```

This allows the model to learn useful word combinations.

---

# Logistic Regression

Logistic Regression is used as the primary classification algorithm for:

- Sentiment classification
- Category classification

For sentiment:

```text
TF-IDF
  ↓
Logistic Regression
  ↓
3 classes
```

For category:

```text
TF-IDF
  ↓
Logistic Regression
  ↓
7 classes
```

`class_weight="balanced"` is used to reduce the effect of class imbalance.

---

# Transformer Model

The project also introduces Transformer-based NLP using DistilBERT.

```text
Customer Feedback
       ↓
Tokenizer
       ↓
Token IDs
       ↓
DistilBERT
       ↓
Classification Layer
       ↓
Sentiment
```

Unlike traditional TF-IDF, Transformer models can capture contextual relationships between words.

The implementation is available in:

```text
notebooks/05_transformers.ipynb
```

---

# Embeddings

Sentence Transformers are used to create semantic representations of customer feedback.

The model used is:

```text
all-MiniLM-L6-v2
```

Embeddings can be used for:

```text
Feedback
   ↓
Embedding
   ↓
Similarity Search
   ↓
Find similar customer complaints
```

This can later be extended into a semantic search or recommendation system.

---

# Evaluation

The classification models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Classification Report

Example:

```text
Accuracy: 0.XXXX

              precision    recall    f1-score
negative         ...
neutral          ...
positive         ...
```

For real-world deployment, additional evaluation on an unseen real-world dataset is recommended.

---

# Future Improvements

Possible improvements include:

- Fine-tuning BERT/DistilBERT on a larger dataset
- Better handling of class imbalance
- Hyperparameter tuning
- Cross-validation
- Explainable AI
- Named Entity Recognition
- Semantic search
- Vector database integration
- Duplicate complaint detection
- Customer issue prioritization
- Streamlit web interface
- REST API using FastAPI or Django
- Real-time feedback analysis
- Multilingual sentiment analysis
- Telugu + English customer feedback support

---

# Learning Outcomes

This project demonstrates practical implementation of:

```text
Python
   ↓
Text Preprocessing
   ↓
NLP
   ↓
TF-IDF
   ↓
Machine Learning
   ↓
Classification
   ↓
Embeddings
   ↓
Semantic Similarity
   ↓
Transformers
```

It provides an end-to-end introduction to building an NLP-based customer feedback analysis system.

---

## Author

**Vivek**

B.Tech Computer Science and Engineering

---

## License

This project is intended for educational and research purposes.