# Customer Feedback Analysis System Using NLP

This repository implements an NLP-based customer feedback analysis system. The sentiment component follows the supplied assignment specification for a **multi-class sentiment analyzer with error analysis**, while the rest of the repository extends the project to category classification, multi-label prediction, keywords, embeddings, and transformers.

## Sentiment Notebook

The generated notebook is:

```text
notebooks/03_sentiment.ipynb
```

It is adapted from the supplied assignment Markdown while using the project's customer-feedback dataset instead of movie-review examples. The assignment defines three sentiment classes—Positive, Neutral, and Negative—and specifies the following pipeline: text cleaning, TF-IDF, Logistic Regression, prediction, evaluation, confusion matrix, and error analysis.

## Dataset

The notebook expects:

```text
data/feedback.csv
```

Required columns:

| Column | Purpose |
|---|---|
| `feedback` | Input customer text |
| `sentiment` | Target: positive, neutral, negative |
| `category` | Used by separate category work; not used by this notebook |

## Notebook Workflow

### 1. Load and inspect data
Checks shape, columns, information, and missing values.

### 2. Sentiment distribution
Counts the three sentiment classes and creates a bar chart.

### 3. Text cleaning
The notebook follows the assignment's simple cleaning approach:

```python
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
```

### 4. Train-test split
Uses an 80/20 split with `random_state=42` and `stratify=y`.

### 5. TF-IDF
Uses:

```python
TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
```

The vectorizer is fitted only on training data and then used to transform test data.

### 6. Logistic Regression
Uses:

```python
LogisticRegression(max_iter=1000)
```

### 7. Evaluation
Reports:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

### 8. Error analysis
Creates a table containing the text, actual sentiment, and predicted sentiment, then isolates incorrect predictions. It also counts actual/predicted class combinations and inspects neutral-sentiment errors.

The assignment identifies common difficulties including negation, mixed opinions, neutral statements, sarcasm, rare vocabulary, and context-dependent sentences.

### 9. New-feedback prediction
The notebook exposes:

```python
predict_sentiment(sentence)
```

which cleans new feedback, transforms it with the trained TF-IDF vectorizer, and predicts one of the three sentiment classes.

## Installation

Install the dependencies used by this notebook:

```bash
pip install pandas numpy matplotlib scikit-learn
```

## Running

Open `notebooks/03_sentiment.ipynb` and run the cells from top to bottom. The relative dataset path is:

```text
../data/feedback.csv
```

Run the notebook from the notebook directory or adjust the path if your Jupyter working directory is different.



## Important Limitation

This is a basic TF-IDF + Logistic Regression sentiment model. TF-IDF represents word and phrase importance but does not deeply understand context. Therefore, negation, sarcasm, mixed sentiment, rare words, and context-dependent feedback can cause errors.

The dataset used for this project is synthetic, so its evaluation score should not be presented as real-world customer-support performance.

## Advanced Extensions

After the basic sentiment notebook, the project continues with:

1. category classification
2. multi-label category classification
3. keyword extraction
4. sentence embeddings
5. transformer-based sentiment classification
6. comparison of classical NLP with transformer models

## Source Alignment

The supplied assignment describes a beginner-level multi-class sentiment analyzer using text cleaning, TF-IDF, Logistic Regression, accuracy, precision, recall, F1-score, confusion matrix, and error analysis. This generated notebook preserves that methodology and adapts only the text domain and file paths to the customer-feedback project.
