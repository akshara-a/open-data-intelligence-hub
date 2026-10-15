# BUILDING A CUSTOMER FEEDBACK ANALYSIS SYSTEM USING NLP

## PROJECT REPORT

### Submitted in partial fulfillment of the requirements for the award of the degree of

**BACHELOR OF TECHNOLOGY**
**IN COMPUTER SCIENCE AND ENGINEERING**

---

# ABSTRACT

Customer feedback contains valuable information about customer satisfaction, complaints, problems, and expectations. However, manually analyzing a large number of customer reviews is time-consuming and difficult. Natural Language Processing (NLP) provides techniques that allow computers to process and analyze human language automatically.

This project presents a **Customer Feedback Analysis System using Natural Language Processing**. The system accepts customer feedback in textual form and analyzes it to identify sentiment, complaint categories, important words or phrases, and the overall meaning of the feedback. The project follows an NLP pipeline consisting of text preprocessing, text vectorization using Term Frequency-Inverse Document Frequency (TF-IDF), sentiment classification using Logistic Regression, category detection, keyword extraction, and meaning generation.

The dataset used in this project contains **25,000 customer feedback records** with information such as review text and sentiment labels. The sentiment classes are **positive, negative, and neutral**. The dataset contains 9,937 negative reviews, 5,085 neutral reviews, and 9,978 positive reviews.

For sentiment classification, the dataset was divided into **80% training data and 20% testing data**, resulting in 20,000 training samples and 5,000 testing samples. TF-IDF with unigrams and bigrams was used for feature extraction, followed by Logistic Regression for classification.

The trained sentiment model achieved **100% accuracy, 100% precision, 100% recall, and 100% F1-score on the held-out 5,000-sample test split**. The confusion matrix contained no off-diagonal errors, and error analysis found zero incorrect predictions in that test split.

The final system also performs complaint category detection, keyword extraction, and generation of a simple overall interpretation of customer feedback. The project demonstrates how classical NLP and machine learning techniques can be combined to build an effective customer feedback analysis system.

**Keywords:** Natural Language Processing, Customer Feedback, Sentiment Analysis, TF-IDF, Logistic Regression, Text Classification, Keyword Extraction, NLP.

---

# 1. INTRODUCTION

Customer feedback is an important source of information for organizations because it reflects customer opinions about products, services, applications, delivery, support, and overall user experience. Feedback may be available in the form of product reviews, survey responses, support tickets, application reviews, feedback forms, and chat messages. The project specification identifies these as common sources of customer feedback.

When the number of reviews becomes large, manually reading every review becomes difficult. A system that automatically understands customer feedback can help organizations identify positive experiences, detect complaints, recognize frequently occurring problems, and understand customer requirements.

Natural Language Processing is a branch of Artificial Intelligence that enables computers to work with human language. In this project, NLP techniques are used to transform raw customer feedback into useful information.

The overall NLP process can be represented as:

```text
Raw Customer Feedback
          |
          v
   Text Preprocessing
          |
          v
      Tokenization
          |
          v
        TF-IDF
          |
          v
 Machine Learning Model
          |
          +----------------+
          |                |
          v                v
      Sentiment        Categories
          |
          v
   Keywords / Meaning
```

This flow follows the recommended basic NLP workflow in the project specification.

---

# 2. PROBLEM STATEMENT

Organizations receive a large amount of customer feedback through different channels. Manually analyzing this feedback requires considerable time and effort.

The main problems are:

1. Large volumes of feedback are difficult to analyze manually.
2. Identifying customer sentiment manually is time-consuming.
3. Important complaint categories may be difficult to identify.
4. Important words and phrases may be overlooked.
5. Different types of complaints may occur in the same feedback.
6. Organizations need a simple way to understand the overall meaning of customer feedback.

Therefore, there is a need for an automated NLP-based system that can analyze customer feedback and provide useful information such as sentiment, categories, keywords, and an overall interpretation.

The project specification defines the main objective as building a simple Customer Feedback Analysis System that understands customer sentiment, main complaint categories, important words or phrases, and overall meaning.

---

# 3. OBJECTIVES

The main objectives of the project are:

1. To develop an NLP-based customer feedback analysis system.
2. To preprocess raw customer feedback text.
3. To convert text into numerical features using TF-IDF.
4. To classify customer feedback into positive, negative, or neutral sentiment.
5. To identify important complaint categories.
6. To extract important words and phrases from feedback.
7. To generate a simple interpretation of the overall meaning.
8. To evaluate the performance of the sentiment classification model.
9. To visualize the classification performance using a confusion matrix.
10. To perform error analysis on the test data.

The specification identifies sentiment, complaint categories, important words/phrases, and overall meaning as the key outputs of the system.

---

# 4. SCOPE OF THE PROJECT

The project focuses mainly on Natural Language Processing rather than database systems, APIs, deployment, or complex infrastructure.

The system accepts customer feedback as text and performs the following operations:

* Text cleaning
* Tokenization through the text vectorization process
* TF-IDF feature extraction
* Sentiment classification
* Complaint category detection
* Keyword extraction
* Overall meaning generation
* Model evaluation

The minimum NLP scope described in the specification includes customer feedback input, preprocessing, TF-IDF, sentiment classification, feedback category classification, and sentiment/category output.

---

# 5. EXISTING SYSTEM

In a traditional customer feedback analysis process, organizations may depend on:

* Manual review of customer comments
* Manual classification of complaints
* Manual identification of positive and negative feedback
* Manual extraction of important issues
* Spreadsheet-based analysis

### Disadvantages of the Existing System

1. It requires significant human effort.
2. It is time-consuming for large datasets.
3. Results may differ between different people.
4. Important keywords may be missed.
5. Large numbers of customer comments are difficult to analyze consistently.
6. Manual analysis is difficult to scale.

---

# 6. PROPOSED SYSTEM

The proposed system automatically analyzes customer feedback using NLP and machine learning.

The system performs the following operations:

```text
Customer Feedback
       |
       v
Text Cleaning
       |
       v
TF-IDF Feature Extraction
       |
       v
Logistic Regression
       |
       v
Sentiment Prediction
       |
       +-------------------+
       |                   |
       v                   v
Category Detection    Keyword Extraction
       |                   |
       +---------+---------+
                 |
                 v
        Overall Meaning
```

The proposed system reduces manual effort and provides structured information from unstructured customer feedback.

The specification recommends Python, pandas, and scikit-learn for the first implementation and identifies text cleaning, TF-IDF, sentiment classification, feedback category classification, and evaluation as the core components.

---

# 7. SYSTEM REQUIREMENTS

## 7.1 Hardware Requirements

Recommended hardware:

* Computer/Laptop
* Minimum 4 GB RAM
* Recommended 8 GB or more RAM
* Intel/AMD processor
* Sufficient storage for dataset and model files

The project was developed and tested on a Windows-based computer.

## 7.2 Software Requirements

* Operating System: Windows
* Programming Language: Python
* Python Libraries:

  * pandas
  * scikit-learn
  * joblib
  * matplotlib
  * re

---

# 8. TECHNOLOGIES USED

## 8.1 Python

Python is used as the primary programming language because it provides extensive libraries for data processing, machine learning, and NLP.

## 8.2 Pandas

Pandas is used for:

* Reading the CSV dataset
* Inspecting the dataset
* Cleaning and manipulating data
* Saving processed datasets

## 8.3 Scikit-learn

Scikit-learn is used for:

* Train-test splitting
* TF-IDF feature extraction
* Logistic Regression
* Accuracy calculation
* Precision calculation
* Recall calculation
* F1-score calculation
* Confusion matrix generation

Scikit-learn provides classification reports containing precision, recall, F1-score, and support for classification models.

## 8.4 Joblib

Joblib is used to save and load the trained sentiment model and TF-IDF vectorizer.

## 8.5 Matplotlib

Matplotlib is used to generate the confusion matrix visualization.

---

# 9. DATASET DESCRIPTION

The project uses a customer sentiment dataset named:

```text
Customer_Sentiment.csv
```

The dataset contains:

```text
25,000 records
13 original columns
```

After preprocessing, an additional `cleaned_text` column is added.

Therefore, the processed dataset contains:

```text
25,000 records
14 columns
```

## 9.1 Dataset Columns

The original dataset contains the following columns:

| Column               | Description                   |
| -------------------- | ----------------------------- |
| customer_id          | Unique customer identifier    |
| gender               | Customer gender               |
| age_group            | Customer age group            |
| region               | Customer region               |
| product_category     | Product category              |
| purchase_channel     | Purchase channel              |
| platform             | Platform used                 |
| customer_rating      | Customer rating               |
| review_text          | Customer feedback text        |
| sentiment            | Sentiment label               |
| response_time_hours  | Response time                 |
| issue_resolved       | Whether issue was resolved    |
| complaint_registered | Complaint registration status |

The main columns used by the NLP system are:

```text
review_text
sentiment
cleaned_text
```

---

# 10. SENTIMENT DISTRIBUTION

The dataset contains three sentiment classes:

| Sentiment | Number of Records |
| --------- | ----------------: |
| Negative  |             9,937 |
| Neutral   |             5,085 |
| Positive  |             9,978 |
| **Total** |        **25,000** |

The sentiment labels used in the project are:

```text
positive
negative
neutral
```

These three sentiment classes are also the standard classes suggested in the project specification.

---

# 11. DATA PREPROCESSING

Raw customer feedback often contains unnecessary characters, different capitalization, URLs, punctuation, and extra spaces.

For example:

```text
"The APP is VERY slow!!!"
```

needs to be transformed into a cleaner representation before further processing.

The project performs the following preprocessing operations:

1. Convert text to lowercase.
2. Remove URLs.
3. Remove special characters and numbers.
4. Remove unnecessary whitespace.
5. Remove empty text records.

The preprocessing process can be represented as:

```text
Raw Text
   |
   v
Convert to Lowercase
   |
   v
Remove URLs
   |
   v
Remove Special Characters
   |
   v
Normalize Spaces
   |
   v
Cleaned Text
```

The project specification identifies text cleaning as an important first stage of the NLP workflow.

### Example

Input:

```text
Very disappointed with the quality!!!
```

Cleaned text:

```text
very disappointed with the quality
```

---

# 12. TOKENIZATION

Tokenization is the process of breaking text into smaller units called tokens, generally words or phrases.

For example:

```text
Payment failed and money was deducted
```

can be represented as:

```text
Payment
failed
and
money
was
deducted
```

In this implementation, tokenization is handled internally as part of the TF-IDF vectorization process rather than through a separate tokenization program.

The project specification describes the NLP flow as raw text → preprocessing → tokenization → TF-IDF → machine learning model.

---

# 13. STOP WORDS

Stop words are common words that may provide limited information for classification.

Examples include:

```text
the
is
and
a
an
to
of
with
```

The sentiment model uses:

```python
stop_words="english"
```

during TF-IDF feature extraction.

A custom stop-word list is also used for keyword extraction so that more meaningful words and phrases can be identified.

The project specification also notes that stop-word removal should be used carefully because some common words can carry meaning depending on the task.

---

# 14. TF-IDF FEATURE EXTRACTION

Machine learning algorithms cannot directly process raw text. Therefore, customer feedback must be converted into numerical features.

TF-IDF stands for:

**Term Frequency-Inverse Document Frequency.**

It assigns importance to words based on their occurrence in a document and their frequency across the collection of documents.

A commonly represented formula is:

```text
TF-IDF(t,d) = TF(t,d) × IDF(t)
```

The project specification explains that words occurring in almost every document are less useful for distinguishing documents, while words such as "refund" may be more informative for particular feedback.

The implementation uses:

```python
TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    max_features=5000,
    sublinear_tf=True
)
```

The model uses:

```text
Unigrams + Bigrams
```

### Unigram

A unigram contains one word:

```text
payment
failed
```

### Bigram

A bigram contains two words:

```text
payment failed
```

Using unigrams and bigrams allows the model to use both individual words and short phrases. The project specification specifically explains that bigrams can capture relationships such as "not good" more effectively than considering the individual words separately.

---

# 15. TF-IDF FEATURE DIMENSIONS

After preprocessing and TF-IDF transformation, the dataset was divided into training and testing data.

The resulting feature dimensions were:

```text
Training TF-IDF shape:
(20000, 68)

Testing TF-IDF shape:
(5000, 68)
```

This means the trained vectorizer generated 68 TF-IDF features for the final dataset configuration.

---

# 16. SENTIMENT ANALYSIS

Sentiment analysis determines whether customer feedback expresses a positive, negative, or neutral opinion.

The project uses three sentiment classes:

```text
Positive
Negative
Neutral
```

Examples:

```text
"I am very happy with the product"
        → Positive

"The product is terrible"
        → Negative

"The product is okay, nothing special"
        → Neutral
```

Sentiment analysis is treated as a text classification problem in the project.

---

# 17. LOGISTIC REGRESSION CLASSIFIER

Logistic Regression is used as the machine learning classifier.

Although its name contains "regression", Logistic Regression is commonly used for classification problems.

The project uses:

```python
LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    C=1.0,
    random_state=42
)
```

The classifier receives the numerical TF-IDF representation and learns the relationship between text features and sentiment labels.

The basic process is:

```text
Cleaned Feedback
       |
       v
      TF-IDF
       |
       v
Logistic Regression
       |
       v
Positive / Negative / Neutral
```

TF-IDF combined with a linear classifier such as Logistic Regression is a common approach for text classification with sparse features.

---

# 18. TRAIN-TEST SPLIT

The dataset is divided into:

```text
80% Training
20% Testing
```

Therefore:

```text
Total records = 25,000

Training records = 20,000

Testing records = 5,000
```

Stratified splitting was used so that the distribution of sentiment classes is maintained between training and testing data.

---

# 19. MODEL TRAINING

The model training process is:

```text
Customer Dataset
       |
       v
Text Preprocessing
       |
       v
Train-Test Split
       |
       v
TF-IDF Vectorization
       |
       v
Logistic Regression Training
       |
       v
Trained Sentiment Model
```

The trained files are stored as:

```text
models/sentiment_model.pkl
models/tfidf_vectorizer.pkl
```

This allows the trained model to be reused for new customer feedback without retraining every time.

---

# 20. COMPLAINT CATEGORY DETECTION

In addition to sentiment, the system identifies the main category or categories associated with customer feedback.

The implemented category detector uses keyword-based rules.

The categories currently implemented are:

| Category        | Example Keywords                          |
| --------------- | ----------------------------------------- |
| Payment         | payment, card, transaction, UPI, billing  |
| Delivery        | delivery, shipping, courier, late, delay  |
| Quality         | quality, damaged, broken, defective       |
| Performance     | slow, lag, loading, freezing, crashing    |
| Support         | support, customer service, response, help |
| Login           | login, password, OTP, verification        |
| Refund          | refund, return, money back                |
| Feature Request | add, feature, option, dark mode           |

For example:

```text
"The application is very slow and keeps freezing."
```

Output:

```text
Category:
Performance
```

Another example:

```text
"Payment failed and customer support did not respond."
```

Output:

```text
Categories:
Payment
Support
```

The project specification recommends category labels such as payment, login, performance, support, UI, bug, and feature request.

**Implementation note:** In the final code, category detection is implemented as a keyword/rule-based component rather than as a separately trained machine-learning category classifier. This accurately reflects the current project implementation.

---

# 21. KEYWORD EXTRACTION

The system extracts important words and phrases from customer feedback.

Keyword extraction uses TF-IDF-based ranking with:

```text
Unigrams
+
Bigrams
```

A custom stop-word list is used to remove common words.

For example:

```text
Payment failed and customer support did not respond
```

may produce keywords such as:

```text
payment failed
payment
support
respond
```

Another example:

```text
The application is very slow and keeps freezing
```

may produce:

```text
slow freezing
slow
freezing
application
```

The project specification identifies keyword extraction as a useful extension to the basic sentiment/category system.

---

# 22. OVERALL MEANING GENERATION

The system generates a simple textual interpretation based on the predicted sentiment and detected categories.

Examples:

### Positive Feedback

```text
The customer has a generally positive experience.
```

### Negative Feedback

```text
The customer is dissatisfied with the experience.
```

### Negative Feedback with Category

```text
The customer is dissatisfied and is experiencing an issue related to payment.
```

This provides a simple human-readable interpretation of the analysis.

---

# 23. SENTIMENT RULE OVERRIDES

During manual testing, some short or unfamiliar sentences produced weak machine-learning predictions.

For example, phrases such as:

```text
Payment failed
I want a refund
I am very happy
```

may contain wording that is not strongly represented by the learned TF-IDF vocabulary.

Therefore, the final analyzer includes strong phrase rules for clearly identifiable expressions such as:

```text
payment failed
money deducted
want a refund
very disappointed
terrible
very poor
not working
keeps crashing
very slow
very happy
absolutely love
excellent
highly recommend
```

These rules improve the final analyzer's handling of obvious customer feedback expressions.

The machine-learning confidence is still reported separately from these rule-based overrides.

---

# 24. COMPLETE SYSTEM WORKFLOW

The complete system operates as follows:

```text
                 CUSTOMER FEEDBACK
                         |
                         v
                  TEXT CLEANING
                         |
                         v
                    TOKENIZATION
                         |
                         v
                       TF-IDF
                         |
                         v
                LOGISTIC REGRESSION
                         |
                         v
                 SENTIMENT RESULT
                         |
             +-----------+-----------+
             |                       |
             v                       v
      CATEGORY DETECTION       KEYWORD EXTRACTION
             |                       |
             +-----------+-----------+
                         |
                         v
                 OVERALL MEANING
```

This combines the main stages recommended in the project specification.

---

# 25. PROJECT MODULES

The project contains the following main Python modules.

## 25.1 preprocessing.py

Responsible for:

* Reading the dataset
* Cleaning review text
* Removing unnecessary characters
* Creating the `cleaned_text` column
* Saving the processed dataset

Output:

```text
data/processed_feedback.csv
```

---

## 25.2 sentiment.py

Responsible for:

* Splitting data into training/testing sets
* TF-IDF feature extraction
* Training Logistic Regression
* Evaluating the model
* Saving the trained model
* Saving the vectorizer

Output:

```text
models/sentiment_model.pkl
models/tfidf_vectorizer.pkl
```

---

## 25.3 category_classifier.py

Responsible for:

* Detecting complaint categories
* Applying category keywords
* Supporting multiple categories
* Saving category results

Output:

```text
data/feedback_with_categories.csv
```

---

## 25.4 keyword_extractor.py

Responsible for:

* Cleaning feedback
* Extracting TF-IDF keywords
* Identifying unigrams and bigrams
* Saving keyword results

Output:

```text
data/feedback_with_keywords.csv
```

---

## 25.5 feedback_analyzer.py

This is the main analysis module.

It combines:

* Sentiment prediction
* Sentiment rule overrides
* Category detection
* Keyword extraction
* Meaning generation

It can analyze new customer feedback.

---

## 25.6 evaluate_model.py

Responsible for calculating:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix

---

## 25.7 plot_confusion_matrix.py

Responsible for generating the visual confusion matrix.

Output:

```text
confusion_matrix.png
```

---

## 25.8 results_summary.py

Displays:

* Dataset size
* Training/test size
* Sentiment distribution
* Model information
* Evaluation results
* Confusion matrix
* NLP components

---

## 25.9 error_analysis.py

Checks whether the sentiment model incorrectly classified any test samples.

Output:

```text
data/error_analysis.csv
```

---

# 26. PROJECT FOLDER STRUCTURE

The final project structure is:

```text
customer-feedback-nlp/
│
├── data/
│   ├── Customer_Sentiment.csv
│   ├── processed_feedback.csv
│   ├── feedback_with_categories.csv
│   ├── feedback_with_keywords.csv
│   └── error_analysis.csv
│
├── models/
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── sentiment.py
│   ├── category_classifier.py
│   ├── keyword_extractor.py
│   ├── feedback_analyzer.py
│   ├── evaluate_model.py
│   ├── plot_confusion_matrix.py
│   ├── results_summary.py
│   └── error_analysis.py
│
└── confusion_matrix.png
```

The specification also recommends keeping the project structure simple and separating data, source code, models, and supporting files.

---

# 27. SAMPLE INPUT AND OUTPUT

## Example 1

### Input

```text
Payment failed and my money was deducted
```

### Output

```text
Sentiment:
Negative

Category:
Payment

Important Keywords:
payment failed
payment
money deducted

Overall Meaning:
The customer is dissatisfied and is experiencing an issue related to payment.
```

---

## Example 2

### Input

```text
The delivery was very late
```

### Output

```text
Sentiment:
Negative

Category:
Delivery

Overall Meaning:
The customer is dissatisfied and is experiencing an issue related to delivery.
```

---

## Example 3

### Input

```text
The product quality is very poor
```

### Output

```text
Sentiment:
Negative

Category:
Quality

Overall Meaning:
The customer is dissatisfied and is experiencing an issue related to quality.
```

---

## Example 4

### Input

```text
Customer support did not respond to my complaint
```

### Output

```text
Sentiment:
Negative

Category:
Support

Overall Meaning:
The customer is dissatisfied and is experiencing an issue related to support.
```

---

## Example 5

### Input

```text
Please add dark mode to the application
```

### Output

```text
Category:
Feature Request
```

---

## Example 6

### Input

```text
I am extremely happy with my purchase
```

### Output

```text
Sentiment:
Positive

Overall Meaning:
The customer has a generally positive experience.
```

---

# 28. MODEL EVALUATION

The sentiment model was evaluated using an 80/20 train-test split.

### Dataset

```text
Total records: 25,000
Training records: 20,000
Testing records: 5,000
```

### Evaluation Metrics

The following metrics were used:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

A classification report is commonly used to summarize precision, recall, F1-score, and support for each class.

---

# 29. EVALUATION RESULTS

The final model achieved the following results:

| Metric    |      Result |
| --------- | ----------: |
| Accuracy  | **100.00%** |
| Precision | **100.00%** |
| Recall    | **100.00%** |
| F1-score  | **100.00%** |

These results were obtained on the **5,000-sample held-out test split**.

The model used:

```text
Feature Extraction:
TF-IDF

N-gram Range:
(1, 2)

Classifier:
Logistic Regression
```

---

# 30. CONFUSION MATRIX

The final confusion matrix was:

```text
                 Predicted

              Negative  Neutral  Positive

Actual
Negative        1987       0        0

Neutral            0      1017      0

Positive           0       0       1996
```

Matrix representation:

```text
[[1987    0    0]
 [   0 1017    0]
 [   0    0 1996]]
```

The diagonal values represent correctly classified samples.

Therefore:

```text
Negative correctly classified = 1,987
Neutral correctly classified  = 1,017
Positive correctly classified = 1,996
```

Total:

```text
1987 + 1017 + 1996 = 5000
```

Thus, all 5,000 test samples were correctly classified in this evaluation split.

A confusion matrix is used to compare actual and predicted classes and identify classification errors.

---

# 31. ERROR ANALYSIS

Error analysis was performed using the test dataset.

Results:

```text
Total test samples:
5000

Correct predictions:
5000

Incorrect predictions:
0
```

Therefore:

```text
Error rate = 0%
```

No incorrect predictions were found in the held-out test split.

The generated error analysis file is:

```text
data/error_analysis.csv
```

The project specification emphasizes that model evaluation should not rely only on accuracy and recommends examining incorrect predictions to understand possible weaknesses.

Although no test-set errors were found, manual testing of new sentences showed that unseen wording can sometimes produce weaker predictions. Therefore, the 100% result should be interpreted as performance on this particular held-out dataset rather than a guarantee of perfect real-world performance.

---

# 32. ADVANTAGES

The proposed system provides several advantages:

1. Automates customer feedback analysis.
2. Reduces manual analysis effort.
3. Processes textual feedback quickly.
4. Identifies positive, negative, and neutral sentiment.
5. Detects important complaint categories.
6. Extracts important words and phrases.
7. Generates a simple interpretation of feedback.
8. Uses a lightweight machine-learning approach.
9. Can analyze new feedback after training.
10. Provides measurable model evaluation.
11. Supports multiple complaint categories for a single feedback sentence.
12. Uses reusable saved model and vectorizer files.

---

# 33. LIMITATIONS

Despite the strong test-set results, the system has some limitations.

### 33.1 Dataset Dependence

The model learns patterns from the available dataset. New types of customer feedback may contain vocabulary that was not present during training.

### 33.2 Category Detection

The current category component is keyword/rule-based rather than a separately trained machine-learning category classifier.

### 33.3 Context Understanding

TF-IDF does not provide the deep contextual understanding of modern transformer-based NLP models.

### 33.4 Sarcasm

The system may have difficulty identifying sarcasm.

For example:

```text
"Great, another payment failure!"
```

may require contextual understanding.

### 33.5 Mixed Sentiment

A sentence may contain both positive and negative opinions.

Example:

```text
"The application looks great but it is extremely slow."
```

A simple three-class sentiment model may not fully represent this mixed opinion.

### 33.6 Confidence Interpretation

The confidence shown by the Logistic Regression model is its model probability output. It should not automatically be interpreted as a perfectly calibrated real-world probability.

### 33.7 100% Test Accuracy

The reported 100% accuracy is specific to the selected held-out test split. It should not be interpreted as a guarantee that every future real-world customer review will be classified correctly.

---

# 34. FUTURE ENHANCEMENTS

The project can be extended in several ways.

## 34.1 Multi-label Machine Learning

Instead of only using keyword rules, a multi-label classification model can be trained so that one feedback sentence can receive multiple complaint labels.

For example:

```text
"The application is slow and payment keeps failing."

Categories:
Performance
Payment
```

The project specification specifically identifies multi-label classification as a useful extension.

## 34.2 Stemming and Lemmatization

Future versions can apply stemming or lemmatization to reduce variations of words.

Example:

```text
running
runs
ran
```

could be mapped toward a common representation.

## 34.3 Sentence Embeddings

Sentence embeddings can be used to represent the semantic meaning of complete feedback sentences.

## 34.4 Semantic Similarity

The system could identify feedback that has similar meaning even when different words are used.

## 34.5 Transformer Models

A future version could use:

* BERT
* DistilBERT
* Other transformer-based models

The project specification recommends transformers as a later-stage enhancement after understanding the classical NLP implementation.

## 34.6 Real-Time Feedback Analysis

A future version could accept feedback continuously and analyze it automatically.

## 34.7 Visualization Dashboard

A future implementation could display:

* Positive feedback percentage
* Negative feedback percentage
* Most common complaint categories
* Most important keywords
* Sentiment trends

This is a possible extension and is not part of the current required NLP implementation.

---

# 35. RESULT DISCUSSION

The project successfully demonstrates a complete classical NLP pipeline for customer feedback analysis.

The dataset contains 25,000 customer feedback records. After preprocessing, the feedback was converted into numerical TF-IDF representations.

The TF-IDF vectorizer used both unigrams and bigrams, allowing the model to consider individual words as well as short phrases.

Logistic Regression was then trained using 20,000 training records.

The model was evaluated using 5,000 unseen test records and achieved:

```text
Accuracy  = 100%
Precision = 100%
Recall    = 100%
F1-score  = 100%
```

The confusion matrix also showed no misclassification:

```text
[[1987    0    0]
 [   0 1017    0]
 [   0    0 1996]]
```

The additional category detection and keyword extraction components provide information beyond sentiment alone.

Therefore, the final system can transform unstructured customer feedback into structured information:

```text
Feedback
   ↓
Sentiment
   ↓
Complaint Category
   ↓
Important Keywords
   ↓
Overall Meaning
```

---

# 36. CONCLUSION

The **Customer Feedback Analysis System Using NLP** was successfully developed and tested.

The project demonstrates how Natural Language Processing and machine learning can be applied to automatically analyze customer feedback.

The system performs text preprocessing, TF-IDF feature extraction, sentiment classification using Logistic Regression, complaint category detection, keyword extraction, and overall meaning generation.

A dataset containing 25,000 customer feedback records was used. The dataset was divided into 20,000 training samples and 5,000 testing samples.

The final sentiment classification model achieved:

```text
Accuracy  : 100.00%
Precision : 100.00%
Recall    : 100.00%
F1-score  : 100.00%
```

The confusion matrix showed that all 5,000 test samples were correctly classified, and the error analysis found zero incorrect predictions in the held-out test set.

The project successfully demonstrates the fundamental NLP concepts required for customer feedback analysis while maintaining a simple architecture without unnecessary backend or infrastructure components. This matches the recommended classical NLP development path in the project specification.

The system can be further improved in the future through multi-label machine learning, sentence embeddings, semantic similarity, and transformer-based models such as BERT or DistilBERT.

---

# 37. REFERENCES

1. Scikit-learn documentation – Classification Report and classification evaluation metrics.

2. Scikit-learn documentation – Text classification using sparse TF-IDF features.

3. Project specification – **Building a Customer Feedback Analysis System Using NLP**.

4. Project specification – TF-IDF and N-gram concepts.

5. Project specification – Sentiment analysis and Logistic Regression.

6. Project specification – Category classification, multi-label classification, and recommended implementation.

---

# 38. APPENDIX A – IMPORTANT PROJECT RESULTS

## Dataset

```text
Dataset:
Customer_Sentiment.csv

Records:
25,000

Processed records:
25,000
```

## Sentiment Distribution

```text
Negative: 9,937
Neutral:  5,085
Positive: 9,978
```

## Training and Testing

```text
Training:
20,000

Testing:
5,000
```

## TF-IDF

```text
N-gram range:
(1, 2)

Training features:
(20000, 68)

Testing features:
(5000, 68)
```

## Model

```text
Logistic Regression
```

## Results

```text
Accuracy:
100.00%

Precision:
100.00%

Recall:
100.00%

F1-score:
100.00%
```

## Confusion Matrix

```text
[[1987    0    0]
 [   0 1017    0]
 [   0    0 1996]]
```

## Error Analysis

```text
Test samples:
5000

Correct:
5000

Incorrect:
0
```

---

# 39. APPENDIX B – PROJECT EXECUTION COMMANDS

The main project modules can be executed from the project root using:

```text
python src/preprocessing.py

python src/sentiment.py

python src/category_classifier.py

python src/keyword_extractor.py

python src/feedback_analyzer.py

python src/evaluate_model.py

python src/plot_confusion_matrix.py

python src/results_summary.py

python src/error_analysis.py
```

---

# 40. APPENDIX C – FINAL PROJECT PIPELINE

```text
                    ┌───────────────────────┐
                    │   Customer Feedback   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Text Preprocessing  │
                    │ Lowercase              │
                    │ URL Removal            │
                    │ Special Character     │
                    │ Removal                │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      Tokenization     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │        TF-IDF         │
                    │ Unigrams + Bigrams    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Logistic Regression  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Sentiment Analysis   │
                    │ Positive / Negative   │
                    │ Neutral               │
                    └───────────┬───────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
        ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
        │   Category   │ │  Keywords   │ │   Overall    │
        │   Detection  │ │ Extraction  │ │   Meaning    │
        └──────────────┘ └─────────────┘ └──────────────┘
                 │              │              │
                 └──────────────┼──────────────┘
                                ▼
                    ┌───────────────────────┐
                    │   Final Analysis      │
                    └───────────────────────┘
```

# END OF REPORT
