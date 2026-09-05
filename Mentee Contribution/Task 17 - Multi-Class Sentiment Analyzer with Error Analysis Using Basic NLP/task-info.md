# NLP Assignment: Multi-Class Sentiment Analyzer with Error Analysis

## 1. Title

**Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP**

---

## 2. Introduction

Sentiment analysis is a Natural Language Processing (NLP) task used to identify the emotion or opinion present in text.

For example:

* `"The movie was amazing."` → **Positive**
* `"The movie was okay."` → **Neutral**
* `"The movie was terrible."` → **Negative**

In this assignment, we will build a **multi-class sentiment analyzer** that classifies text into three sentiment classes:

1. **Positive**
2. **Neutral**
3. **Negative**

We will use basic NLP techniques only.

The main steps are:

1. Load the dataset
2. Understand the dataset
3. Clean the text
4. Convert text into numerical features using TF-IDF
5. Train a machine learning model
6. Predict sentiment
7. Evaluate the model
8. Create a confusion matrix
9. Perform error analysis

---

# 3. Objective

The objective of this assignment is to build a simple NLP-based machine learning model that can classify a sentence or review into one of three sentiment categories:

* Positive
* Neutral
* Negative

Another important objective is to perform **error analysis** to understand why the model gives incorrect predictions.

---

# 4. Tools and Libraries

We will use Python and the following libraries:

```python
pandas
numpy
matplotlib
scikit-learn
```

Install the required libraries using:

```bash
pip install pandas numpy matplotlib scikit-learn
```

---

# 5. Dataset

The dataset should contain at least two columns:

| text                           | sentiment |
| ------------------------------ | --------- |
| I really enjoyed this movie    | positive  |
| The movie was average          | neutral   |
| I hated this movie             | negative  |
| Excellent acting and story     | positive  |
| Nothing special about the film | neutral   |
| The film was very boring       | negative  |

The dataset can be saved as:

```text
sentiment_data.csv
```

Example CSV:

```csv
text,sentiment
"I really enjoyed this movie",positive
"The movie was average",neutral
"I hated this movie",negative
"Excellent acting and story",positive
"Nothing special about the film",neutral
"The film was very boring",negative
```

For a real assignment, a larger dataset should be used because six examples are not enough to train a good machine learning model.

---

# 6. Import Required Libraries

```python
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
```

### Explanation

* `pandas` is used to load and manage the dataset.
* `numpy` is used for numerical operations.
* `re` is used for text cleaning.
* `matplotlib` is used for graphs.
* `train_test_split` divides the dataset into training and testing data.
* `TfidfVectorizer` converts text into numerical values.
* `LogisticRegression` is used for classification.
* `accuracy_score` calculates model accuracy.
* `classification_report` gives precision, recall and F1-score.
* `confusion_matrix` shows correct and incorrect predictions.

---

# 7. Load the Dataset

```python
df = pd.read_csv("sentiment_data.csv")
```

Display the first five rows:

```python
print(df.head())
```

Example output:

```text
                              text sentiment
0      I really enjoyed this movie  positive
1            The movie was average   neutral
2               I hated this movie  negative
3       Excellent acting and story  positive
4  Nothing special about the film   neutral
```

---

# 8. Check Dataset Information

Check the number of rows and columns:

```python
print(df.shape)
```

Check column names:

```python
print(df.columns)
```

Check basic information:

```python
print(df.info())
```

Check missing values:

```python
print(df.isnull().sum())
```

---

# 9. Remove Missing Values

If the dataset contains empty rows, remove them.

```python
df = df.dropna()
```

Check again:

```python
print(df.isnull().sum())
```

---

# 10. Check Sentiment Classes

We can check which sentiment classes exist in the dataset.

```python
print(df["sentiment"].unique())
```

Expected output:

```text
['positive' 'neutral' 'negative']
```

Count the number of examples in each class:

```python
print(df["sentiment"].value_counts())
```

Example:

```text
positive    1000
negative    950
neutral     900
```

This helps us understand whether the dataset is balanced.

---

# 11. Visualize Sentiment Distribution

```python
df["sentiment"].value_counts().plot(kind="bar")

plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Samples")
plt.show()
```

### Observation

If all three classes have a similar number of examples, the dataset is approximately balanced.

If one class has many more examples than the others, the dataset is imbalanced.

---

# 12. Text Preprocessing

Text data usually contains unnecessary information such as:

* Capital letters
* URLs
* Special characters
* Extra spaces
* Numbers
* Punctuation

We will create a simple function to clean the text.

```python
def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-z\s]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
```

Apply the function:

```python
df["clean_text"] = df["text"].apply(clean_text)
```

Display the original and cleaned text:

```python
print(df[["text", "clean_text"]].head())
```

---

# 13. Understanding the Cleaning Function

Suppose the original sentence is:

```text
"I REALLY loved this Movie!!! 10/10"
```

After converting to lowercase:

```text
i really loved this movie!!! 10/10
```

After removing special characters and numbers:

```text
i really loved this movie
```

Final cleaned text:

```text
i really loved this movie
```

---

# 14. Define Input and Output

The input variable is the cleaned text.

```python
X = df["clean_text"]
```

The target variable is sentiment.

```python
y = df["sentiment"]
```

So:

```python
X = df["clean_text"]
y = df["sentiment"]
```

---

# 15. Split the Dataset

We divide the dataset into:

* **80% training data**
* **20% testing data**

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

### Why do we split the dataset?

The training dataset is used to teach the model.

The testing dataset is used to check how well the model works on unseen text.

`stratify=y` helps maintain approximately the same percentage of positive, neutral and negative samples in both training and testing data.

---

# 16. TF-IDF Feature Extraction

Machine learning models cannot directly understand sentences.

For example:

```text
I love this movie
```

must first be converted into numbers.

We will use **TF-IDF**.

TF-IDF means:

**Term Frequency - Inverse Document Frequency**

It gives importance to useful words.

For example:

Words such as:

```text
excellent
amazing
terrible
boring
fantastic
bad
```

may receive useful weights because they help identify sentiment.

Create the TF-IDF vectorizer:

```python
tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)
```

Convert training data:

```python
X_train_tfidf = tfidf.fit_transform(X_train)
```

Convert testing data:

```python
X_test_tfidf = tfidf.transform(X_test)
```

---

# 17. Why Use `fit_transform()` and `transform()`?

For training data:

```python
tfidf.fit_transform(X_train)
```

TF-IDF first learns the vocabulary and then converts the training sentences into numbers.

For testing data:

```python
tfidf.transform(X_test)
```

We only transform the test data using the vocabulary learned from the training data.

We should **not fit the vectorizer on the testing data**, because that would allow information from the test set to influence training.

---

# 18. Train the Model

We will use **Logistic Regression**.

Although the name contains "regression", Logistic Regression is commonly used for classification.

```python
model = LogisticRegression(
    max_iter=1000
)
```

Train the model:

```python
model.fit(X_train_tfidf, y_train)
```

The model now learns relationships between words and sentiment classes.

---

# 19. Make Predictions

Predict sentiment for the testing dataset:

```python
y_pred = model.predict(X_test_tfidf)
```

Display some predictions:

```python
print(y_pred[:10])
```

Example output:

```text
['positive'
 'negative'
 'neutral'
 'positive'
 'negative']
```

---

# 20. Calculate Accuracy

```python
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
```

Example:

```text
Accuracy: 0.82
```

This means the model correctly classified approximately **82% of the test examples**.

The actual result will depend on the dataset.

---

# 21. Classification Report

Accuracy alone is not enough.

We should also calculate:

* Precision
* Recall
* F1-score

```python
print(classification_report(y_test, y_pred))
```

Example output:

```text
              precision    recall  f1-score   support

negative          0.84       0.82      0.83       200
neutral           0.75       0.72      0.73       190
positive          0.86       0.89      0.87       210

accuracy                               0.82       600
macro avg         0.82       0.81      0.81       600
weighted avg      0.82       0.82      0.82       600
```

---

# 22. Understanding Evaluation Metrics

## Accuracy

Accuracy tells us the percentage of total predictions that are correct.

Formula:

```text
Accuracy = Correct Predictions / Total Predictions
```

Example:

If the model predicts 80 sentences correctly out of 100:

```text
Accuracy = 80 / 100
         = 0.80
         = 80%
```

---

## Precision

Precision answers:

> When the model predicts a particular sentiment, how often is it correct?

For example, if the model predicts 100 reviews as positive and only 85 are actually positive:

```text
Precision = 85 / 100
          = 0.85
```

---

## Recall

Recall answers:

> Out of all actual examples of a sentiment, how many did the model correctly identify?

For example, there are 100 actual positive reviews.

If the model correctly identifies 80:

```text
Recall = 80 / 100
       = 0.80
```

---

## F1-Score

F1-score combines precision and recall.

A higher F1-score normally means better classification performance.

---

# 23. Confusion Matrix

A confusion matrix shows which classes are being confused with each other.

```python
cm = confusion_matrix(y_test, y_pred)
```

Display it:

```python
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

display.plot()
plt.title("Confusion Matrix")
plt.show()
```

Example:

| Actual / Predicted | Negative | Neutral | Positive |
| ------------------ | -------: | ------: | -------: |
| Negative           |      160 |      30 |       10 |
| Neutral            |       25 |     140 |       25 |
| Positive           |        5 |      20 |      185 |

The diagonal numbers represent correct predictions.

For example:

```text
Negative → Negative = Correct
Neutral → Neutral = Correct
Positive → Positive = Correct
```

Numbers outside the diagonal represent mistakes.

For example:

```text
Negative → Neutral = Error
Neutral → Positive = Error
Positive → Neutral = Error
```

---

# 24. Error Analysis

Error analysis means examining the incorrect predictions made by the model.

This is an important part of NLP because accuracy only tells us **how many predictions were correct**.

Error analysis helps us understand:

> Why did the model make mistakes?

---

# 25. Create an Error Analysis DataFrame

First, create a new DataFrame containing the test sentences, actual labels and predicted labels.

```python
results = pd.DataFrame({
    "text": X_test.values,
    "actual": y_test.values,
    "predicted": y_pred
})
```

Display some examples:

```python
print(results.head())
```

---

# 26. Find Incorrect Predictions

```python
errors = results[
    results["actual"] != results["predicted"]
]
```

Display incorrect predictions:

```python
print(errors.head(20))
```

Example:

| Text                                 | Actual   | Predicted |
| ------------------------------------ | -------- | --------- |
| the movie was not bad                | positive | negative  |
| acting was good but story was boring | neutral  | positive  |
| it was okay nothing special          | neutral  | negative  |
| not the best movie                   | negative | positive  |

These examples help us understand the weaknesses of the model.

---

# 27. Count Incorrect Predictions

```python
print("Total test samples:", len(results))

print("Incorrect predictions:", len(errors))
```

We can also calculate the error percentage:

```python
error_rate = len(errors) / len(results)

print("Error Rate:", error_rate)
```

---

# 28. Analyze Common Error Types

We can manually study the errors.

Some common error types are explained below.

---

## Error Type 1: Negation

Example:

```text
The movie was not bad.
```

Actual:

```text
Positive
```

Predicted:

```text
Negative
```

### Reason

The model may give high importance to the word:

```text
bad
```

but fail to understand:

```text
not bad
```

which usually has a positive meaning.

---

## Error Type 2: Mixed Sentiment

Example:

```text
The acting was amazing but the story was boring.
```

The sentence contains:

Positive word:

```text
amazing
```

Negative word:

```text
boring
```

Therefore the model may have difficulty deciding whether the sentence is positive, neutral or negative.

---

## Error Type 3: Neutral Sentences

Example:

```text
The movie was okay.
```

Words such as:

```text
okay
average
fine
normal
```

may be difficult for the model because their sentiment is weaker than clearly positive or negative words.

As a result, neutral sentiment is often more difficult to classify.

---

## Error Type 4: Sarcasm

Example:

```text
Great, another boring three-hour movie.
```

The word:

```text
great
```

normally indicates positive sentiment.

However, the complete sentence may actually be negative or sarcastic.

A basic TF-IDF model cannot properly understand sarcasm.

---

## Error Type 5: Lack of Context

Example:

```text
That was something.
```

Without additional context, it is difficult to determine whether this statement is positive, negative or neutral.

Simple NLP models do not understand context like humans do.

---

## Error Type 6: Rare Words

Suppose the test sentence contains:

```text
The film was phenomenal.
```

If the word:

```text
phenomenal
```

appeared very few times or never appeared in the training dataset, the model may not understand its relationship with positive sentiment.

---

## Error Type 7: Short Sentences

Example:

```text
Not good.
```

Very short sentences contain very little information.

Therefore prediction can sometimes be difficult.

---

# 29. Analyze Which Classes Are Most Confused

We can create a table showing actual and predicted sentiment combinations.

```python
error_counts = errors.groupby(
    ["actual", "predicted"]
).size()

print(error_counts)
```

Example output:

```text
actual    predicted

negative  neutral      30
negative  positive      8

neutral   negative     25
neutral   positive     28

positive  negative      5
positive  neutral      22
```

### Observation

Suppose the largest errors are:

```text
neutral → positive
neutral → negative
```

This suggests that the model finds **neutral sentiment difficult to identify**.

---

# 30. Display Only Neutral Errors

```python
neutral_errors = errors[
    errors["actual"] == "neutral"
]

print(neutral_errors.head(10))
```

This allows us to study why neutral examples are being classified incorrectly.

---

# 31. Test the Model on New Sentences

We can create a small prediction function.

```python
def predict_sentiment(sentence):

    sentence = clean_text(sentence)

    sentence_tfidf = tfidf.transform([sentence])

    prediction = model.predict(sentence_tfidf)

    return prediction[0]
```

Now test it.

```python
print(
    predict_sentiment(
        "I absolutely loved this movie"
    )
)
```

Possible output:

```text
positive
```

Another example:

```python
print(
    predict_sentiment(
        "This movie was terrible and boring"
    )
)
```

Possible output:

```text
negative
```

Neutral example:

```python
print(
    predict_sentiment(
        "The movie was okay"
    )
)
```

Possible output:

```text
neutral
```

---

# 32. Test Multiple Sentences

```python
sentences = [
    "This movie was amazing",
    "The movie was average",
    "I hated the story",
    "The acting was excellent",
    "Nothing special about this movie"
]

for sentence in sentences:

    sentiment = predict_sentiment(sentence)

    print(sentence, "->", sentiment)
```

Possible output:

```text
This movie was amazing -> positive
The movie was average -> neutral
I hated the story -> negative
The acting was excellent -> positive
Nothing special about this movie -> neutral
```

---

# 33. Complete Program

The complete basic program is shown below.

```python
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


# -----------------------------------
# 1. Load Dataset
# -----------------------------------

df = pd.read_csv("sentiment_data.csv")


# -----------------------------------
# 2. Check Dataset
# -----------------------------------

print(df.head())

print(df.shape)

print(df.isnull().sum())

print(df["sentiment"].value_counts())


# -----------------------------------
# 3. Remove Missing Values
# -----------------------------------

df = df.dropna()


# -----------------------------------
# 4. Text Cleaning
# -----------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-z\s]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


df["clean_text"] = df["text"].apply(clean_text)


# -----------------------------------
# 5. Input and Target
# -----------------------------------

X = df["clean_text"]

y = df["sentiment"]


# -----------------------------------
# 6. Train-Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 7. TF-IDF
# -----------------------------------

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_tfidf = tfidf.fit_transform(X_train)

X_test_tfidf = tfidf.transform(X_test)


# -----------------------------------
# 8. Model Training
# -----------------------------------

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train_tfidf,
    y_train
)


# -----------------------------------
# 9. Prediction
# -----------------------------------

y_pred = model.predict(
    X_test_tfidf
)


# -----------------------------------
# 10. Accuracy
# -----------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print(
    "Accuracy:",
    accuracy
)


# -----------------------------------
# 11. Classification Report
# -----------------------------------

print(
    classification_report(
        y_test,
        y_pred
    )
)


# -----------------------------------
# 12. Confusion Matrix
# -----------------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

display.plot()

plt.title(
    "Confusion Matrix"
)

plt.show()


# -----------------------------------
# 13. Error Analysis
# -----------------------------------

results = pd.DataFrame({
    "text": X_test.values,
    "actual": y_test.values,
    "predicted": y_pred
})

errors = results[
    results["actual"]
    != results["predicted"]
]

print("\nIncorrect Predictions:")

print(
    errors.head(20)
)


# -----------------------------------
# 14. Error Counts
# -----------------------------------

print(
    errors.groupby(
        ["actual", "predicted"]
    ).size()
)


# -----------------------------------
# 15. Prediction Function
# -----------------------------------

def predict_sentiment(sentence):

    sentence = clean_text(sentence)

    sentence_tfidf = tfidf.transform(
        [sentence]
    )

    prediction = model.predict(
        sentence_tfidf
    )

    return prediction[0]


# -----------------------------------
# 16. Test New Sentences
# -----------------------------------

print(
    predict_sentiment(
        "I really loved this movie"
    )
)

print(
    predict_sentiment(
        "The movie was okay"
    )
)

print(
    predict_sentiment(
        "This was a terrible movie"
    )
)
```

---

# 34. Methodology

The complete methodology of this project can be written as:

```text
Dataset
   ↓
Text Cleaning
   ↓
Train-Test Split
   ↓
TF-IDF Vectorization
   ↓
Logistic Regression
   ↓
Sentiment Prediction
   ↓
Model Evaluation
   ↓
Confusion Matrix
   ↓
Error Analysis
```

---

# 35. Results

After training the Logistic Regression classifier using TF-IDF features, the model was evaluated using:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix

The model successfully learned common sentiment-related words and was able to classify many reviews correctly.

Positive and negative sentiments were generally easier to identify because they often contain clear words such as:

```text
amazing
excellent
love
terrible
bad
boring
hate
```

Neutral examples were more difficult because neutral sentences often contain less emotional language.

> Note: Add your actual accuracy and classification report values after running the program.

Example:

```text
Model Accuracy: 82%
```

Do not write `82%` unless your model actually produces approximately that result.

---

# 36. Error Analysis Findings

After examining incorrect predictions, several common problems were identified.

### 1. Negation

The model sometimes had difficulty with sentences containing words such as:

```text
not
never
no
```

Example:

```text
The movie was not bad.
```

The word `bad` is negative, but `not bad` can express a positive opinion.

---

### 2. Mixed Opinions

Sentences containing both positive and negative opinions were difficult.

Example:

```text
The acting was good but the story was boring.
```

---

### 3. Neutral Sentiment

Neutral examples were often confused with positive or negative examples.

Example:

```text
The movie was fine.
```

---

### 4. Sarcasm

The basic model could not properly identify sarcasm.

Example:

```text
Great, another boring movie.
```

---

### 5. Rare Vocabulary

Words that appeared rarely in the training dataset were difficult for the model.

---

# 37. Limitations

The project has several limitations.

### Limitation 1: Bag-of-Words Style Representation

TF-IDF mostly works using word occurrence and importance.

It does not completely understand the meaning of a sentence.

---

### Limitation 2: Context

The model has limited understanding of context.

For example:

```text
I thought it would be bad, but it was actually excellent.
```

The sentence contains both:

```text
bad
```

and

```text
excellent
```

A simple model may become confused.

---

### Limitation 3: Sarcasm

The model cannot properly identify sarcasm.

---

### Limitation 4: Dataset Size

If the training dataset is small, the model may not learn enough words and patterns.

---

### Limitation 5: Class Imbalance

If one sentiment class contains significantly more examples than other classes, the model may become biased toward the larger class.

---

# 38. Possible Improvements

The project can be improved in several simple ways.

### 1. Increase the Dataset Size

More training examples can help the model learn more vocabulary and sentiment patterns.

---

### 2. Balance the Dataset

Try to maintain similar numbers of:

```text
Positive
Neutral
Negative
```

examples.

---

### 3. Use Bigrams

We already used:

```python
ngram_range=(1, 2)
```

This allows TF-IDF to learn both single words and two-word combinations.

For example:

```text
not good
very bad
really amazing
not bad
```

This can help with sentiment classification.

---

### 4. Try Another Basic Model

We can compare Logistic Regression with models such as:

```text
Multinomial Naive Bayes
Support Vector Machine
```

However, Logistic Regression is sufficient for this basic assignment.

---

# 39. Conclusion

In this assignment, a **multi-class sentiment analyzer** was created using basic Natural Language Processing and machine learning techniques.

The model classified text into three sentiment classes:

* Positive
* Neutral
* Negative

Text preprocessing was performed to remove unnecessary characters and normalize the sentences.

TF-IDF was used to convert textual information into numerical features. Logistic Regression was then trained using these features.

The performance of the model was evaluated using accuracy, precision, recall, F1-score and a confusion matrix.

Error analysis showed that the model may have difficulty with:

* Negation
* Neutral statements
* Mixed sentiments
* Sarcasm
* Rare words
* Context-dependent sentences

Therefore, error analysis is useful because it not only shows that the model is making mistakes but also helps identify **why the mistakes occur**.

Overall, the project demonstrates how basic NLP techniques can be used to create a simple multi-class sentiment classification system.

---

# 40. Viva Questions and Answers

## Q1. What is sentiment analysis?

Sentiment analysis is an NLP technique used to identify the opinion or emotion expressed in text.

---

## Q2. What are the classes used in this project?

The three classes are:

```text
Positive
Neutral
Negative
```

---

## Q3. Why is it called multi-class classification?

Because the model predicts more than two possible classes.

Our project has three classes.

---

## Q4. What is NLP?

NLP stands for **Natural Language Processing**.

It is a field of artificial intelligence that helps computers process and understand human language.

---

## Q5. Why do we preprocess text?

Text preprocessing removes unnecessary information and converts the text into a cleaner form that is easier for the model to process.

---

## Q6. What is TF-IDF?

TF-IDF stands for:

```text
Term Frequency - Inverse Document Frequency
```

It converts text into numerical features based on the importance of words.

---

## Q7. Why can't we directly give sentences to Logistic Regression?

Machine learning algorithms work with numerical values.

Therefore, sentences must first be converted into numbers.

---

## Q8. Which classifier is used?

We used:

```text
Logistic Regression
```

---

## Q9. What is a training dataset?

The training dataset is the portion of data used to teach the machine learning model.

---

## Q10. What is a testing dataset?

The testing dataset contains unseen examples used to evaluate the trained model.

---

## Q11. Why do we use an 80-20 split?

80% of the dataset is used for training and 20% for testing.

This provides enough data for training while keeping some unseen examples for evaluation.

---

## Q12. What is accuracy?

Accuracy is the percentage of total predictions that are correct.

---

## Q13. What is precision?

Precision measures how many predicted examples of a class were actually correct.

---

## Q14. What is recall?

Recall measures how many actual examples of a class were correctly identified.

---

## Q15. What is F1-score?

F1-score combines precision and recall into one measurement.

---

## Q16. What is a confusion matrix?

A confusion matrix is a table showing correct and incorrect predictions for each class.

---

## Q17. What is error analysis?

Error analysis means manually examining incorrect model predictions to understand why the model made mistakes.

---

## Q18. Why is error analysis important?

It helps us:

```text
Understand model weaknesses
Find common mistakes
Identify difficult sentiment classes
Improve the model
```

---

## Q19. Why can neutral sentiment be difficult?

Neutral sentences normally contain fewer strong emotional words, which makes them harder to distinguish from positive and negative sentences.

---

## Q20. Can this model understand sarcasm?

Not very well.

TF-IDF with Logistic Regression is a basic approach and does not truly understand the contextual meaning of sentences.

---

# 41. Final Project Structure

A simple project folder can look like:

```text
sentiment-analysis/
│
├── sentiment_data.csv
│
├── sentiment_analysis.ipynb
│
└── README.md
```

If using a Python file:

```text
sentiment-analysis/
│
├── sentiment_data.csv
│
├── sentiment_analysis.py
│
└── README.md
```

---

# 42. Short Assignment Summary

**Project:** Multi-Class Sentiment Analyzer

**Task:** Text Classification

**Sentiment Classes:**

```text
Positive
Neutral
Negative
```

**NLP Technique:**

```text
Text Cleaning
TF-IDF
```

**Machine Learning Algorithm:**

```text
Logistic Regression
```

**Evaluation:**

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

**Error Analysis:**

```text
Incorrect Predictions
Negation Errors
Neutral Sentiment Errors
Mixed Sentiment Errors
Sarcasm
Rare Words
```

This is a simple and suitable beginner-level NLP assignment because it covers the complete NLP classification pipeline without using advanced deep learning models such as LSTM, BERT or Transformers.
