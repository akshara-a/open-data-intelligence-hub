# Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP

A complete, end-to-end Natural Language Processing (NLP) project that classifies text into three sentiment classes (**Positive**, **Neutral**, and **Negative**) using classic machine learning techniques, followed by an in-depth **Error Analysis** to diagnose and understand the model's linguistic failure modes.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Project Directory Structure](#project-directory-structure)
4. [Installation & Requirements](#installation--requirements)
5. [How to Run](#how-to-run)
6. [NLP Methodology Pipeline](#nlp-methodology-pipeline)
7. [Experimental Results & Evaluation](#experimental-results--evaluation)
8. [In-Depth Error Analysis](#in-depth-error-analysis)
9. [Project Limitations](#project-limitations)
10. [Future Improvements](#future-improvements)
11. [Viva Questions & Answers (20 Questions)](#viva-questions--answers)
12. [Assignment Summary](#assignment-summary)

---

## 1. Project Overview

Sentiment analysis is a subfield of Natural Language Processing (NLP) that aims to determine the underlying emotional tone or opinion expressed in human language.

In this assignment, we implement a **multi-class sentiment classifier** without complex or opaque deep learning frameworks. We focus on transparent, interpretable, classical NLP methods:
- **Text Normalization**: Regex-based lowercasing, URL removal, punctuation cleaning, and whitespace trimming.
- **Feature Extraction**: TF-IDF (Term Frequency - Inverse Document Frequency) with unigrams and bigrams (`ngram_range=(1, 2)`).
- **Classification Algorithm**: Multi-class Logistic Regression with L-BFGS optimization.
- **Error Analysis**: Systematic auditing of misclassified samples across linguistic edge cases.

---

## 2. Objectives

1. **Build a 3-Class Sentiment Classifier**: Accurately predict whether a given sentence or review is `positive`, `neutral`, or `negative`.
2. **Implement Good NLP Practices**: Prevent data leakage by fitting TF-IDF only on training data, applying stratified train-test splits, and reporting precision, recall, and F1-score.
3. **Conduct In-Depth Error Analysis**: Go beyond aggregate accuracy to inspect specific misclassified sentences and classify their causes (negation, mixed sentiment, sarcasm, neutral ambiguity, rare words, and context shortage).

---

## 3. Project Directory Structure

```text
Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP/
│
├── sentiment_data.csv             # Balanced 500-sample dataset (167 pos, 167 neu, 166 neg)
├── sentiment_analysis.py          # Complete standalone Python execution script
├── sentiment_analysis.ipynb       # Interactive Jupyter Notebook with step-by-step documentation
├── sentiment_distribution.png     # Class balance visualization plot
├── confusion_matrix.png           # Confusion matrix evaluation heatmap
└── README.md                      # Comprehensive assignment documentation and Viva Q&A
```

---

## 4. Installation & Requirements

Ensure you have Python 3.8+ installed. Install the necessary dependencies via `pip`:

```bash
pip install pandas numpy matplotlib scikit-learn
```

Optional (for running the Jupyter notebook):
```bash
pip install jupyter notebook
```

---

## 5. How to Run

### Option A: Run via Terminal / Command Line
Execute the full automated pipeline from your shell:

```bash
python sentiment_analysis.py
```

This will:
1. Load and validate `sentiment_data.csv` (500 samples).
2. Clean and preprocess all text.
3. Split the data into 80% training (400 samples) and 20% testing (100 samples) sets using stratified sampling.
4. Extract unigram and bigram TF-IDF features (`max_features=5000`).
5. Train the Logistic Regression model.
6. Evaluate accuracy, classification report, and confusion matrix.
7. Save visualization artifacts: `sentiment_distribution.png` and `confusion_matrix.png`.
8. Perform detailed error analysis and print misclassification tables.
9. Run real-time test inferences across sample sentences.

### Option B: Interactive Execution via Jupyter Notebook
Launch Jupyter Notebook or Jupyter Lab:

```bash
jupyter notebook sentiment_analysis.ipynb
```
Step through the individual code cells sequentially to inspect intermediate outputs, charts, and error breakdowns interactively.

---

## 6. NLP Methodology Pipeline

The complete end-to-end workflow follows an established industry-standard NLP architecture:

```text
Raw Text Dataset (sentiment_data.csv, 500 samples)
   │
   ▼
1. Text Preprocessing & Cleaning (Regex URL/Symbol Removal, Lowercasing)
   │
   ▼
2. Stratified Train-Test Split (80% Train [400], 20% Test [100], stratify=y)
   │
   ▼
3. TF-IDF Feature Extraction (Unigrams + Bigrams, max_features=5000)
   │  [fit_transform on Train; transform only on Test]
   ▼
4. Model Training (Logistic Regression, max_iter=1000)
   │
   ▼
5. Model Evaluation (Accuracy, Precision, Recall, F1-Score, Confusion Matrix)
   │
   ▼
6. Error Analysis & Diagnostics
   ├── Error Rates & Confusion Cross-tabulation
   ├── Neutral Misclassification Drill-down
   └── Linguistic Taxonomy Analysis (Negation, Sarcasm, Mixed Opinions, Rare Words)
```

---

## 7. Experimental Results & Evaluation

The model was evaluated on an unseen, stratified test set of 100 reviews (34 Neutral, 33 Positive, 33 Negative).

### 7.1 Key Performance Metrics

| Metric | Result |
| :--- | :--- |
| **Total Test Samples** | 100 (from 500 total dataset) |
| **Overall Accuracy** | **93.00%** |
| **Macro Avg F1-Score** | **0.9300** |
| **Weighted Avg F1-Score** | **0.9299** |
| **Total Misclassifications** | 7 / 100 (Error Rate: **7.00%**) |

### 7.2 Detailed Classification Report

```text
              precision    recall  f1-score   support

    negative     0.9412    0.9697    0.9552        33
     neutral     0.8889    0.9412    0.9143        34
    positive     0.9667    0.8788    0.9206        33

    accuracy                         0.9300       100
   macro avg     0.9322    0.9299    0.9300       100
weighted avg     0.9318    0.9300    0.9299       100
```

### 7.3 Confusion Matrix

| Actual \ Predicted | Predicted Negative | Predicted Neutral | Predicted Positive |
| :--- | :---: | :---: | :---: |
| **Actual Negative** | **32** | 1 | 0 |
| **Actual Neutral** | 1 | **32** | 1 |
| **Actual Positive** | 1 | 3 | **29** |

#### Observations:
- **Strong Recognition**: The model correctly predicts 93 out of 100 test samples.
- **Neutral Boundary Confusion**: Consistent with real-world NLP observations, the Neutral class exhibits the most boundary cross-over (1 misclassified as negative, 1 misclassified as positive, and 3 positives misclassified as neutral).

---

## 8. In-Depth Error Analysis

Error analysis inspects *why* incorrect predictions occur to reveal fundamental limitations of bag-of-words / TF-IDF representations.

### Error Taxonomy & Real Test Cases (from the 7 Test Misclassifications)

#### 1. Negation Inversion
- **Example 1**: *"i didnt hate this film in fact it was entertaining"*
  - **Actual**: `positive` | **Predicted**: `neutral`
  - **Reason**: The negation phrase `"didnt hate"` conveys positive enjoyment, but bag-of-words separates `"didnt"` and `"hate"`, pulling the prediction toward the neutral boundary.
- **Example 2**: *"i cannot say anything good about this film"*
  - **Actual**: `negative` | **Predicted**: `neutral`
  - **Reason**: The positive token `"good"` conflicts with the negative prefix `"cannot say"`.

#### 2. Mixed Opinions / Contrastive Clauses
- **Example 1**: *"superb cinematography though the characters were poorly written"*
  - **Actual**: `neutral` | **Predicted**: `negative`
  - **Reason**: The positive word `"superb"` is countered by `"poorly written"`. The negative clause carries slightly higher TF-IDF weight in this test sample.
- **Example 2**: *"enjoyable action despite the terrible writing"*
  - **Actual**: `positive` | **Predicted**: `neutral`
  - **Reason**: The phrase balances `"enjoyable"` with `"terrible"`, resulting in a neutralized prediction vector.
- **Example 3**: *"remarkable effects couldnt disguise the boring screenplay"*
  - **Actual**: `neutral` | **Predicted**: `positive`
  - **Reason**: The strong term `"remarkable"` pulled the prediction positive despite `"boring"`.

#### 3. Rare / Advanced Vocabulary
- **Example**: *"a propitious and magnificent tour de force of dramatic art"*
  - **Actual**: `positive` | **Predicted**: `negative`
  - **Reason**: Rare literary words like `"propitious"` had zero occurrences in the training set vocabulary, depriving the model of its strongest sentiment signal.

#### 4. Short Sentences & Brevity
- **Example**: *"loved it"*
  - **Actual**: `positive` | **Predicted**: `neutral`
  - **Reason**: Ultra-short two-word inputs contain sparse feature vectors, allowing small intercept biases to tip the prediction away from the intended class.

---

## 9. Project Limitations

1. **Bag-of-Words Limitation**: TF-IDF models word occurrences and bigrams, but lacks syntactic parsing, dependency tracking, or deep compositional semantics.
2. **Inability to Resolve Sarcasm**: Sarcastic statements (e.g., *"Great, another boring 3-hour movie"*) rely on ironic contrast between positive vocabulary and cynical intent, which linear classifiers cannot detect without context.
3. **No Sequence Modeling**: The model treats words essentially as an unordered collection of n-grams, discarding long-range semantic dependencies.
4. **Vocabulary Bottleneck**: Words not present in the training vocabulary cannot contribute to sentiment prediction (Out-of-Vocabulary issue).

---

## 10. Future Improvements

1. **Negation Tagging**: Prepend a `NOT_` prefix to all words following a negation token until the next punctuation mark (e.g., `"not bad"` → `"not NOT_bad"`).
2. **Lexicon Integration**: Incorporate sentiment lexicons (e.g., VADER or SentiWordNet) as engineered numerical features alongside TF-IDF.
3. **Model Exploration**: Compare performance against Naive Bayes (MultinomialNB) and Support Vector Machines (LinearSVC).
4. **Contextual Embeddings**: Transition to dense transformer-based architectures (such as DistilBERT or RoBERTa) for deep semantic and contextual comprehension.

---

## 11. Viva Questions & Answers

### Q1. What is sentiment analysis?
**Ans:** Sentiment analysis is a Natural Language Processing (NLP) technique used to computationally identify, extract, and quantify emotional states, attitudes, and opinions expressed in text.

### Q2. What are the classes used in this project?
**Ans:** Three sentiment classes are used:
1. `Positive`
2. `Neutral`
3. `Negative`

### Q3. Why is it called multi-class classification?
**Ans:** Because the target variable contains more than two distinct categorical outcomes. A problem with two classes is binary classification; problems with three or more classes are multi-class classification.

### Q4. What is NLP?
**Ans:** NLP stands for **Natural Language Processing**. It is an interdisciplinary field of Artificial Intelligence and Computational Linguistics focused on enabling computers to understand, interpret, and generate human languages.

### Q5. Why do we preprocess text?
**Ans:** Raw text contains noise (varying cases, punctuation, HTML links, and numbers) that increases vocabulary size without providing useful sentiment signal. Preprocessing standardizes the text, reduces sparsity, and improves model generalization.

### Q6. What is TF-IDF?
**Ans:** TF-IDF stands for **Term Frequency - Inverse Document Frequency**. It is a statistical numerical feature extraction metric:
- **TF (Term Frequency)**: Measures how frequently a term occurs in a document.
- **IDF (Inverse Document Frequency)**: Measures how rare or common a word is across all documents in the corpus.
Words that are frequent in a specific document but rare overall receive high weights.

### Q7. Why can't we directly give sentences to Logistic Regression?
**Ans:** Machine learning algorithms perform mathematical computations (vector dot products, matrix multiplications) and require numerical feature vectors, not raw strings.

### Q8. Which classifier is used?
**Ans:** Multi-class **Logistic Regression** (using one-vs-rest or multinomial cross-entropy with L-BFGS solver).

### Q9. What is a training dataset?
**Ans:** The portion of labeled data used to fit the model parameters (weights and biases) during the learning phase.

### Q10. What is a testing dataset?
**Ans:** A separate, unseen dataset reserved strictly for evaluating the trained model's generalization ability on real-world inputs.

### Q11. Why do we use an 80-20 split?
**Ans:** An 80/20 split offers a balanced tradeoff, allocating sufficient data (80%) for the model to learn representative patterns while retaining an adequate sample (20%) for statistically valid testing.

### Q12. What is accuracy?
**Ans:** Accuracy is the proportion of total correct predictions out of all predictions made:
$$\text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Predictions}}$$

### Q13. What is precision?
**Ans:** Precision measures the reliability of positive predictions for a given class:
$$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}$$
It answers: *When the model predicts class $C$, how often is it right?*

### Q14. What is recall?
**Ans:** Recall (sensitivity) measures the model's coverage of actual instances:
$$\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}$$
It answers: *Out of all actual examples of class $C$, how many did the model identify?*

### Q15. What is F1-score?
**Ans:** F1-score is the harmonic mean of precision and recall:
$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
It provides a balanced single metric when precision and recall need to be evaluated jointly.

### Q16. What is a confusion matrix?
**Ans:** A confusion matrix is an $N \times N$ table where rows represent true labels and columns represent predicted labels. The main diagonal shows correct predictions; off-diagonal elements show errors.

### Q17. What is error analysis?
**Ans:** Error analysis is the systematic process of manually or programmatically inspecting misclassified examples to diagnose systemic failure modes, data bugs, and model weaknesses.

### Q18. Why is error analysis important?
**Ans:** Accuracy alone gives a high-level summary score but hides specific failure patterns. Error analysis identifies *why* errors occur (e.g., negation failure, sarcasm, neutral ambiguity), guiding targeted improvements.

### Q19. Why can neutral sentiment be difficult?
**Ans:** Neutral statements lack strong emotional keywords. They often express mild opinions, mixed sentiments, or purely objective facts, placing them near the decision boundary between positive and negative classes.

### Q20. Can this model understand sarcasm?
**Ans:** No. Sarcasm relies on pragmatic context, world knowledge, and irony where positive words are used with negative intent. Basic TF-IDF and linear models only see the individual words, leading to misclassification.

---

## 12. Assignment Summary

- **Project:** Multi-Class Sentiment Analyzer with Error Analysis
- **Dataset:** 500 Samples (167 Positive, 167 Neutral, 166 Negative)
- **Split:** 80% Train (400 samples), 20% Test (100 samples)
- **Task:** 3-Class Text Classification (`positive`, `neutral`, `negative`)
- **Techniques Used:** Regex Preprocessing, TF-IDF Vectorization (`ngram_range=(1, 2)`), Multi-Class Logistic Regression
- **Evaluation:** Accuracy (93.00%), Precision, Recall, F1-Score (0.9300), Confusion Matrix
- **Error Analysis:** Empirical taxonomy covering Negations, Mixed Sentiment, Neutral Ambiguity, Rare Words, and Short Sentences.
