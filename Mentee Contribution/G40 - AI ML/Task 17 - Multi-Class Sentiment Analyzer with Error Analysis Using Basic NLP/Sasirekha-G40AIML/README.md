# 💬 Sentiment Intelligence — Multi-Class Sentiment Analyzer

A realistic, end-to-end NLP machine-learning project built from the **supplied `Tweets.csv` dataset**.

## Project objective

Classify short text into:

- `positive`
- `neutral`
- `negative`

The project follows the assignment methodology: data validation → cleaning → train/test split → TF-IDF → Logistic Regression → evaluation → confusion matrix → error analysis.

## Dataset used

The supplied archive contained `Tweets.csv` with 27,481 rows and these columns:

- `textID`
- `text`
- `selected_text`
- `sentiment`

The model uses `text` as the input and `sentiment` as the target. `textID` and `selected_text` are retained in the raw dataset for traceability but are not used as model features.

## Real-world project structure

```text
sentiment-analyzer-real-world/
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   └── raw/
│       └── Tweets.csv
├── models/
│   └── sentiment_pipeline.joblib
├── notebooks/
│   └── sentiment_analysis.ipynb
├── reports/
│   ├── metrics.json
│   ├── error_analysis.csv
│   └── figures/
│       ├── confusion_matrix.png
│       └── sentiment_distribution.png
├── src/
│   ├── model.py
│   ├── text_utils.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
└── tests/
    ├── test_model.py
    └── test_text_utils.py
```

## Quick start in VS Code

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the web app

```bash
streamlit run app.py
```

### 4. Retrain from the supplied dataset

```bash
python -m src.train
python -m src.evaluate
```

### 5. Run tests

```bash
pytest -q
```

### 6. Command-line prediction

```bash
python -m src.predict "I absolutely loved this movie"
```

## Model design

```text
Raw tweet
   ↓
Text normalization
   ↓
TF-IDF word + bigram features
   ↓
Logistic Regression
   ↓
Sentiment + class probabilities
```

The TF-IDF vectorizer is fit only on the training split, avoiding test-set vocabulary leakage.

## Evaluation

The included `reports/metrics.json` contains the metrics from the packaged trained model. The exact score is dataset- and split-dependent, so the README does not hard-code an assumed accuracy.

## Error analysis

`reports/error_analysis.csv` contains held-out examples for which the model's prediction differs from the actual label. This supports manual investigation of:

- negation
- mixed sentiment
- sarcasm
- neutral language
- rare vocabulary
- context-dependent expressions

## Deployment

The project includes a `Dockerfile`:

```bash
docker build -t sentiment-intelligence .
docker run -p 8501:8501 sentiment-intelligence
```

Then open `http://localhost:8501`.

## Important limitation

This is intentionally a **basic NLP** solution using TF-IDF and Logistic Regression. It does not understand language like a transformer model and can struggle with sarcasm, long-range context and subtle negation.
