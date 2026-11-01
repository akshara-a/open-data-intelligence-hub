---
title: "Multi-Class Sentiment Analyzer with Error Analysis"
author: "Nidhi Sandbhor"
output: html_document
---

# 1. Introduction

Sentiment Analysis is an NLP task used to identify the emotion or opinion present in text.

In this project, we classify text into three sentiment classes:

- Positive
- Neutral
- Negative

The main steps are:

1. Load Dataset
2. Understand Dataset
3. Clean Text
4. TF-IDF Feature Extraction
5. Train Logistic Regression Model
6. Predict Sentiment
7. Evaluate Model
8. Create Confusion Matrix
9. Perform Error Analysis

# 2. Import Required Libraries

```{python}
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay