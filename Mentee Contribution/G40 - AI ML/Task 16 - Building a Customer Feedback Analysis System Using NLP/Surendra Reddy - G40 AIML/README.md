# Task 16 - Customer Feedback Analysis System using NLP

## Overview
This project implements a Customer Feedback Analysis System using classical Natural Language Processing (NLP) techniques. The system processes raw customer feedback text and produces three outputs for each entry:
1. **Sentiment classification** (positive / negative / neutral)
2. **Multi-label category classification** (e.g. payment, performance, support, login, ui, general)
3. **Keyword extraction** (top TF-IDF terms per feedback)

## Approach
- **Text Cleaning**: Lowercasing, whitespace normalization, and basic text standardization.
- **Feature Extraction**: TF-IDF vectorization with unigrams and bigrams (`ngram_range=(1,2)`).
- **Sentiment Model**: Logistic Regression trained on TF-IDF features via an `sklearn.Pipeline`.
- **Category Model**: Multi-label classification using `OneVsRestClassifier(LogisticRegression)` with labels binarized via `MultiLabelBinarizer`.
- **Keyword Extraction**: Top-N highest TF-IDF scoring terms per feedback entry.

## Files
| File | Description |
|------|--------------|
| `Task16_Customer_Feedback_NLP.ipynb` | Main Colab notebook with the full pipeline |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

## How to Run
1. Open `Task16_Customer_Feedback_NLP.ipynb` in Google Colab or Jupyter.
2. Run all cells top to bottom (no GPU required — this is a classical scikit-learn pipeline).
3. Use `analyze_feedback("your feedback text")` at the end of the notebook to test on new input.

## Example Output

Feedback: The app is very slow and payment keeps failing.
Sentiment: negative
Categories: ['performance', 'payment']
Keywords: ['slow', 'payment', 'failing']


## Notes
- The current dataset is a small illustrative sample. For production use, this pipeline should be retrained on a larger, labeled feedback dataset for better generalization (the sample run showed 0.0 F1 on the category model due to insufficient training data — noted as a known limitation).
- Model classes: `general`, `login`, `payment`, `performance`, `support`, `ui`.

## Author
Surendra Reddy — G40 AIML