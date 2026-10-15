# Building a Customer Feedback Analysis System Using NLP

A comprehensive, modular Natural Language Processing (NLP) system for analyzing customer feedback in real-time. The system automatically processes noisy customer reviews and extracts **Sentiment**, **Multi-Topic Categories**, **Important Keywords/Keyphrases**, and **Semantically Similar Past Feedback**.

---

## 🚀 Key Features & NLP Capabilities

1. **Text Preprocessing & Linguistic Normalization**
   - Lowercasing, URL/email normalization, repeated character & punctuation compression.
   - Word tokenization.
   - **Negation-Preserving Stopword Filtering**: Crucial retention of negation words (`not`, `no`, `never`, `barely`, `without`) to prevent inverting customer sentiment (e.g. ensuring *"This app is not good"* does not collapse into *"This app is good"*).
   - **Stemming vs Lemmatization**: Suffix stemmer vs grammatical dictionary base-form lemmatizer.

2. **Sentiment Analysis**
   - N-gram (Unigram + Bigram) TF-IDF Vectorization with sublinear term frequency.
   - Balanced Logistic Regression classification (`positive`, `negative`, `neutral`).
   - Output probability distribution and model explainability (top informative n-grams).

3. **Multi-Label Category Classification**
   - Supports feedback spanning multiple topics simultaneously (e.g., *"The app is very slow and payment keeps failing"* $\rightarrow$ `['payment', 'performance']`).
   - Uses `MultiLabelBinarizer` and `OneVsRestClassifier` with probability thresholding.
   - Covers 8 real-world customer categories: `payment`, `performance`, `ui`, `support`, `login`, `bug`, `feature_request`, and `general`.

4. **Keyword & Keyphrase Extraction**
   - Salient phrase ranking using n-gram document-frequency scoring.
   - Filters out non-informative boundary stopwords for clean extracted phrases (e.g., *"payment gateway"*, *"support team"*, *"login otp"*).

5. **Semantic Similarity & Historical Retrieval**
   - Vector space embedding and Cosine Similarity engine.
   - Matches incoming feedback with historical complaints in the database to detect recurring issues and patterns.

6. **Modern Transformer Comparison (DistilBERT)**
   - Side-by-side comparison between classical TF-IDF Bag-of-Words and deep Transformer attention on tricky linguistic structures (negations, double negatives, sarcasm).

7. **Interactive Streamlit Web Dashboard & CLI**
   - Sleek interactive UI with live feedback testing, step-by-step NLP stage inspector, batch CSV processing with analytics charts, and model diagnostic explorer.
   - Production CLI for headless operations (`train`, `evaluate`, `analyze`, `compare`).

---

## 📂 Project Structure

```text
customer-feedback-nlp/
├── data/
│   └── feedback.csv                    # 80+ varied customer feedback samples with multi-labels
├── models/                             # Serialized trained models (.joblib)
│   ├── sentiment_model.joblib
│   └── category_model.joblib
├── notebooks/                          # 5 Step-by-step educational Jupyter notebooks
│   ├── 01_text_preprocessing.ipynb     # Cleaning, tokenization, stemming vs lemmatization
│   ├── 02_tfidf_and_ngrams.ipynb       # Bag of Words, TF-IDF calculation, unigram/bigrams
│   ├── 03_sentiment_analysis.ipynb     # Logistic Regression modeling & classification reports
│   ├── 04_category_classification.ipynb# Multi-label classification (One-vs-Rest)
│   └── 05_transformers.ipynb           # Sentence similarity & Transformer comparison
├── src/
│   ├── __init__.py
│   ├── preprocessing.py                # Text cleaning, tokenization, stemming & lemmatization
│   ├── sentiment.py                    # TF-IDF + Logistic Regression sentiment classifier
│   ├── category_classifier.py          # MultiLabelBinarizer + OneVsRestClassifier
│   ├── keyword_extractor.py            # TF-IDF N-gram keyphrase extractor
│   ├── embeddings.py                   # Sentence vectorization & Cosine Similarity search
│   ├── transformer_model.py            # DistilBERT transformer analyzer & comparison
│   └── pipeline.py                     # Unified CustomerFeedbackAnalyzer pipeline
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py                # Automated pytest test suite (10 test cases)
├── frontend/                           # Swiss Editorial Web Studio (HTML5/CSS3/JS)
│   ├── index.html                      # 4-Quadrant architectural studio interface
│   ├── style.css                       # Swiss grid design system & crosshairs
│   └── app.js                          # Client NLP controller & REST API client
├── server.py                           # High-performance REST API & static web server
├── app.py                              # Streamlit web dashboard
├── main.py                             # Command-line interface
├── requirements.txt                    # Project dependencies
└── README.md                           # Documentation & guide
```

---

## 🏗️ Architecture & NLP Workflow

```text
                  CUSTOMER FEEDBACK TEXT
                            │
                            ▼
                     TEXT CLEANING
             (Lowercase, Normalization, Stripping)
                            │
                            ▼
                      TOKENIZATION
                            │
                            ▼
              NEGATION-PRESERVING FILTERING
               (Preserves 'not', 'no', 'never')
                            │
                            ▼
                      LEMMATIZATION
               (Dictionary Base Form Conversion)
                            │
                            ▼
                    TF-IDF + N-GRAMS
               (Unigram & Bigram Vector Space)
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    SENTIMENT CLASSIFIER          MULTI-LABEL CATEGORIES
(Logistic Regression Pipeline)      (OneVsRestClassifier)
            │                               │
            ▼                               ▼
  Positive / Negative / Neutral     Payment, Performance, UI...
            │                               │
            └───────────────┬───────────────┘
                            │
                            ▼
                 KEYWORD & PHRASE EXTRACTOR
                (TF-IDF High-Salience Terms)
                            │
                            ▼
                SEMANTIC SIMILARITY SEARCH
              (Cosine Similarity over Corpus)
```

---

## ⚡ Quickstart

### 1. Installation

Clone or open the repository in your terminal and install dependencies:

```powershell
pip install -r requirements.txt
```

### 2. Train the Models via CLI

Train both the Sentiment Classifier and the Multi-Label Category Classifier:

```powershell
python main.py train
```

### 3. Evaluate Models

Generate accuracy, precision, recall, F1, confusion matrix, and multi-label metrics:

```powershell
python main.py evaluate
```

### 4. Analyze Single Feedback

Analyze any custom customer feedback text directly from the terminal:

```powershell
python main.py analyze "The application is very slow and payment keeps failing."
```

Example Output:
```text
======================================================================
CUSTOMER FEEDBACK NLP ANALYSIS REPORT
======================================================================
Input Text:       "The application is very slow and payment keeps failing."
Cleaned Text:     "the application is very slow and payment keeps failing"
Lemmatized:       ['application', 'slow', 'payment', 'keep', 'fail']
----------------------------------------------------------------------
Sentiment:        NEGATIVE (Confidence: 65.7%)
Sentiment Scores:
  - Negative  :  65.7%  #############
  - Neutral   :  15.9%  ###
  - Positive  :  18.4%  ###
----------------------------------------------------------------------
Categories:       payment, performance
Category Scores (active if >= 35%):
  [*] payment         :  70.1%
  [*] performance     :  65.3%
  [ ] general         :  24.1%
  [ ] bug             :  24.4%
  [ ] support         :  23.5%
  [ ] login           :  21.0%
----------------------------------------------------------------------
Important Keywords / Keyphrases:
  * slow payment             (TF-IDF: 0.343)
  * application slow         (TF-IDF: 0.343)
  * payment keeps failing    (TF-IDF: 0.314)
----------------------------------------------------------------------
Semantically Similar Past Customer Feedback:
  1. [67.4%] "The app is extremely slow and payment keeps failing"
     -> Sentiment: negative, Categories: performance,payment
  2. [42.4%] "Payment keeps failing during checkout with credit card"
     -> Sentiment: negative, Categories: payment
======================================================================
```

### 5. Compare Classical TF-IDF vs Transformer (DistilBERT)

```powershell
python main.py compare
```

---

## 🌐 Web Interfaces

### Option 1: Swiss Editorial Web Studio (Custom 4-Quadrant Architecture)

Run the dedicated REST API and modern Swiss editorial frontend:

```powershell
python server.py
```

Then navigate to **`http://localhost:8000`** (or port 8080) in your browser:
- **01 Intake & Linguistic Stream**: Live feedback input, preset selectors, real-time counters, hotkey execution (`Cmd/Ctrl + Enter`).
- **02 Sentiment Decoder**: Probabilistic emotional polarity banner, confidence score gauge, softmax distribution bars, negation detection guard.
- **03 Taxonomy & Keyphrase Engine**: Multi-label category matrix, salience-ranked TF-IDF keyphrases, in-context highlight map.
- **04 Semantic Twins & Historical Retrieval**: Cosine similarity search against 80+ customer incident database.
- **05 Pipeline X-Ray Drawer**: Step-by-step tokenization, negation filtering, Porter stemmer vs. WordNet lemmatizer table, TF-IDF weights.
- **06 Batch Analytics Lab**: Multi-review processor, sentiment distribution breakdown (% positive / % negative), CSV export.
- **07 Transformer Benchmark**: DistilBERT vs TF-IDF comparison on complex linguistic inversions.

*Note: The frontend can also be opened directly via `frontend/index.html` in any modern web browser.*

---

### Option 2: Streamlit Dashboard

```powershell
streamlit run app.py
```

Open `http://localhost:8501` in your browser.
- **🔍 Live Feedback Tester**: Instant sentiment gauge, category chips, keyword tags, similar complaints drawer.
- **🔬 Step-by-Step NLP Inspector**: Interactive view of raw text $\rightarrow$ tokens $\rightarrow$ lemmatization $\rightarrow$ TF-IDF weights.
- **📊 Batch Feedback Analytics**: Upload feedback CSV files, generate interactive sentiment & category charts, and download enriched CSV files.
- **🤖 Classical NLP vs Transformer**: Side-by-side linguistic comparison on negations and complex sentences.
- **📈 Model Evaluation**: Confusion matrix heatmap, precision/recall/F1 metrics, and top keywords per category.

---

## 🧪 Running Automated Tests

Run the complete test suite:

```powershell
pytest tests/test_pipeline.py -v
```

All 10 test suites verify:
- Clean text and normalization
- Regex tokenization
- Negation preservation
- Stemming vs lemmatization
- Sentiment model fitting & probability calibration
- Multi-label category prediction
- Keyword extraction
- Cosine similarity matching
- End-to-end pipeline execution

---

## 📚 Educational Jupyter Notebooks

Located in `notebooks/`:
- `01_text_preprocessing.ipynb`: Cleaning, tokenization, stop-words, stemming vs lemmatization table.
- `02_tfidf_and_ngrams.ipynb`: Bag of Words, TF-IDF calculation, unigram vs bigram representations.
- `03_sentiment_analysis.ipynb`: Logistic regression training, cross-validation, confusion matrix, precision/recall/F1.
- `04_category_classification.ipynb`: MultiLabelBinarizer, OneVsRestClassifier, multi-label evaluation (Micro/Macro F1).
- `05_transformers.ipynb`: Sentence embeddings, cosine similarity, DistilBERT comparison.
