# Task 17 — Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP

## Objective
Build a multi-class (positive/neutral/negative) sentiment classifier using basic NLP
techniques, and perform detailed error analysis to understand why misclassifications occur.

## Dataset
[Twitter US Airline Sentiment](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment)
(Kaggle, CC-BY-NC-SA-4.0) — 14,640 tweets, already labeled positive/neutral/negative.
Downloaded via the Kaggle API directly inside the notebook (not committed to the repo —
see "How to Run").

## Pipeline

Raw Tweets
|
v
Text Cleaning (lowercase, remove URLs, remove @mentions, remove special chars/numbers)
|
v
Train/Test Split (80/20, stratified)
|
v
TF-IDF (unigram + bigram, max 5000 features)
|
v
Logistic Regression
|
v
Evaluation (accuracy, precision, recall, F1, confusion matrix)
|
v
Error Analysis


## Results
- Accuracy: 79.4%
- Negative F1: 0.87 | Neutral F1: 0.61 | Positive F1: 0.66
- Dataset is imbalanced (63% negative, 21% neutral, 16% positive), which biases the
  model toward predicting negative on ambiguous inputs

## Error Analysis Findings
1. **Class imbalance bias** — most neutral/positive errors are misclassified as negative
2. **Negation** — e.g. "not bad" misread as negative due to the word "bad"
3. **Sarcasm** — e.g. "Great, another delayed flight" misread as positive
4. **Short/low-signal tweets** — very short neutral tweets carry little sentiment vocabulary

## Possible Improvements
Class-weighted Logistic Regression or oversampling minority classes, bigram-aware
negation handling, transformer-based models (BERT) for better context understanding.

## How to Run
1. Get a free Kaggle account and generate an API token (Settings → API Tokens)
2. In Colab, add it as a Secret named `KAGGLE_API_TOKEN`
3. Run all cells top to bottom (`Runtime → Run all`) — CPU runtime, no GPU needed
4. The notebook downloads the dataset automatically via the Kaggle API

## Files
- `Sentiment_Analyzer_Error_Analysis.ipynb` — full notebook
- `requirements.txt` — dependencies
- `README.md` — this file