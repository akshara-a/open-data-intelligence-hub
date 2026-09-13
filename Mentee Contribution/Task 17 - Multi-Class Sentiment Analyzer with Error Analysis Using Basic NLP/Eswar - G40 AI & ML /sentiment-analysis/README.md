# Multi-Class Sentiment Analyzer with Error Analysis

A beginner-level NLP project that classifies text into **Positive**, **Neutral**, or **Negative** sentiment using basic NLP techniques (TF-IDF + Logistic Regression), with a full error-analysis section.

## Project Structure

```text
sentiment-analysis/
│
├── sentiment_data.csv        # Dataset (text, sentiment)
├── sentiment_analysis.py     # Full pipeline script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Pipeline

1. Load the dataset
2. Understand the dataset (shape, columns, missing values, class balance)
3. Clean the text (lowercase, remove URLs/punctuation/numbers/extra spaces)
4. Convert text into numerical features using TF-IDF (unigrams + bigrams)
5. Train a Logistic Regression model
6. Predict sentiment on held-out test data (80/20 stratified split)
7. Evaluate the model (accuracy, precision, recall, F1-score)
8. Create a confusion matrix
9. Perform error analysis on misclassified examples

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python sentiment_analysis.py
```

This will print dataset info, accuracy, and the classification report to the console, and will save:

- `sentiment_distribution.png` — bar chart of class distribution
- `confusion_matrix.png` — confusion matrix plot
- `error_analysis.csv` — table of misclassified test examples

## Results (on the included dataset)

- **Accuracy:** ~0.94 (will vary slightly if the dataset is changed)
- Evaluated with precision, recall, F1-score per class, plus a confusion matrix.

## Error Analysis Findings

Common causes of misclassification identified during error analysis:

- **Negation** — e.g. "not bad" being read as negative because of the word "bad"
- **Mixed opinions** — sentences containing both positive and negative cues
- **Neutral sentiment** — neutral text lacks strong emotional words, making it easy to confuse with positive/negative
- **Sarcasm** — basic TF-IDF models cannot detect sarcastic tone
- **Rare vocabulary** — words seen rarely (or never) in training are hard to weigh correctly

## Limitations

- TF-IDF is a bag-of-words style representation and does not capture full sentence meaning
- Limited understanding of context (e.g. "I thought it would be bad, but it was excellent")
- Cannot detect sarcasm
- Performance depends on dataset size and class balance

## Possible Improvements

- Increase and balance the dataset
- Use word embeddings or transformer-based models (e.g. BERT) for better context understanding
- Try alternative basic models (Naive Bayes, SVM) for comparison

## Tech Stack

- Python
- pandas, numpy
- scikit-learn (TF-IDF, Logistic Regression, metrics)
- matplotlib (visualizations)
