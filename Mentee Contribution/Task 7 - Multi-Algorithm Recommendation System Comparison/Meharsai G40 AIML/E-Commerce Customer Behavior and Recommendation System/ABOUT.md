# E-Commerce Customer Behavior and Recommendation System

## Overview

This project presents a machine learning-based e-commerce customer intelligence system designed to analyze customer behavior, predict purchase intent, segment customers, and generate personalized product recommendations.

The system combines supervised learning, unsupervised learning, and recommendation algorithms to study different aspects of customer activity in an e-commerce environment.

The project uses a dataset containing 25,000 customer sessions, 8,442 unique customers, and 899 unique products.

## Objectives

The main objectives of the project are:

- Analyze e-commerce customer and session behavior.
- Predict whether a customer session will result in a purchase.
- Identify customer segments based on behavioral and purchasing characteristics.
- Generate personalized product recommendations.
- Compare multiple recommendation algorithms using ranking-based evaluation metrics.
- Provide an interactive Streamlit interface for exploring the machine learning system.

## Dataset Overview

The dataset contains 25,000 e-commerce session records and 29 features.

### Dataset Statistics

| Attribute | Value |
|---|---:|
| Total Sessions | 25,000 |
| Unique Customers | 8,442 |
| Unique Products | 899 |
| Product Categories | 8 |
| Purchase Rate | 22.46% |
| Non-Purchase Sessions | 77.54% |

The dataset contains customer, product, browsing, cart, purchase, and temporal information.

Important attributes include:

- `customer_id`
- `session_id`
- `device_type`
- `user_type`
- `marketing_channel`
- `product_id`
- `product_category`
- `unit_price`
- `quantity`
- `discount_percent`
- `pages_viewed`
- `time_on_site_sec`
- `added_to_cart`
- `purchased`
- `cart_abandoned`
- `revenue`
- `rating`
- `visit_month`
- `visit_weekday`
- `visit_season`
- `location`

## Exploratory Data Analysis

Exploratory Data Analysis was performed to understand customer purchase behavior and feature relationships.

The target variable is imbalanced:

- Not Purchased: 19,384 sessions
- Purchased: 5,616 sessions

This corresponds to a purchase rate of 22.46%.

### Key EDA Observations

Registered or returning user behavior showed a higher purchase rate than the alternate user group.

Very short sessions had a lower purchase rate compared with longer sessions.

Browsing variables such as pages viewed and time on site showed limited direct separation between purchased and non-purchased sessions.

Several post-purchase variables had strong relationships with the target variable.

Examples include:

- `revenue`
- `revenue_normalized`
- `review_text`
- `review_helpful_votes`
- `rating`

These features were identified as potential target leakage or post-purchase information.

## Leakage Prevention

The objective of the purchase prediction model is to estimate purchase intent using information available before the final purchase outcome.

Therefore, post-purchase and outcome-derived variables were excluded from model training.

The following types of features were excluded:

- Revenue generated after purchase
- Normalized revenue
- Review information
- Review helpful votes
- Rating information
- Payment-related information
- Direct cart outcome indicators

The purchase prediction model uses 15 leakage-safe features:

- `device_type`
- `user_type`
- `marketing_channel`
- `product_category`
- `unit_price`
- `quantity`
- `discount_percent`
- `discount_amount`
- `pages_viewed`
- `time_on_site_sec`
- `visit_day`
- `visit_month`
- `visit_weekday`
- `visit_season`
- `location`

## Purchase Prediction

A Random Forest Classifier was used to predict whether a session would result in a purchase.

### Data Splitting

The dataset was divided using a stratified train-test split.

- Training records: 20,000
- Testing records: 5,000

The original class distribution was preserved in the untouched test set.

Only the training data was balanced before model training.

### Training Distribution After Balancing

| Purchase Class | Records |
|---|---:|
| Not Purchased | 4,493 |
| Purchased | 4,493 |

This prevents information from the test dataset from affecting the balancing process.

### Hyperparameter Tuning

RandomizedSearchCV with 5-fold cross-validation was used for model optimization.

The best Random Forest parameters were:

```python
{
    "n_estimators": 400,
    "min_samples_split": 10,
    "min_samples_leaf": 1,
    "max_features": "log2",
    "max_depth": 5
}
```

### Purchase Prediction Performance

| Metric | Score |
|---|---:|
| Accuracy | 0.4956 |
| Precision | 0.2536 |
| Recall | 0.6411 |
| F1 Score | 0.3635 |
| ROC-AUC | 0.5611 |

The model achieved a purchase-class recall of approximately 64.11%.

The ROC-AUC score indicates limited separation between purchasing and non-purchasing sessions. The EDA also showed that many leakage-safe behavioral variables have weak relationships with the purchase outcome.

Therefore, the model results are reported without artificially introducing post-purchase features to increase accuracy.

## Customer Segmentation

K-Means clustering was used to identify behavioral customer segments.

Customer-level profiles were created by aggregating session records.

The clustering features include:

- Total sessions
- Purchase rate
- Total purchases
- Total revenue
- Average order value
- Average pages viewed
- Average time on site
- Average discount
- Cart addition rate
- Cart abandonment rate

The customer features were standardized before clustering.

### Cluster Selection

K-Means models were evaluated from `K = 2` to `K = 8`.

The Silhouette Score and inertia were used for evaluation.

| K | Silhouette Score |
|---:|---:|
| 2 | 0.2399 |
| 3 | 0.1911 |
| 4 | 0.1868 |
| 5 | 0.1866 |
| 6 | 0.1729 |
| 7 | 0.1770 |
| 8 | 0.1692 |

The best configuration was:

```text
K = 2
Silhouette Score = 0.2399
```

### Identified Customer Segments

#### Cluster 0: Low-Engagement / Low-Value Customers

Characteristics include:

- Very low purchase rate
- Low total purchases
- Low generated revenue
- Higher cart abandonment rate

Possible business strategies include retargeting campaigns, cart recovery campaigns, and targeted purchase incentives.

#### Cluster 1: High-Value / Purchasing Customers

Characteristics include:

- Higher purchase rate
- More purchases
- Higher total revenue
- Higher cart addition rate
- Lower cart abandonment rate

Possible business strategies include personalized recommendations, loyalty programs, cross-selling, and retention campaigns.

## Product Recommendation System

The recommendation system uses implicit customer-product interactions.

Interaction scores were created using customer behavior.

| Customer Behavior | Interaction Score |
|---|---:|
| Product interaction | 1 |
| Added to cart | 3 |
| Purchased | 7 |

Higher scores represent stronger customer interest.

A customer-product interaction matrix was created with:

```text
8,442 customers × 899 products
```

## Recommendation Algorithms

Three recommendation approaches were compared.

### Popularity-Based Recommendation

Products are ranked using their overall interaction popularity.

This approach does not provide strong personalization but acts as a simple recommendation strategy.

### Item-Based Collaborative Filtering

Item-Based Collaborative Filtering calculates cosine similarity between product interaction vectors.

Products similar to those previously interacted with by a customer are ranked using weighted interaction scores.

### Truncated SVD

Truncated Singular Value Decomposition was used as a latent-factor recommendation approach.

The interaction matrix was projected into a lower-dimensional latent space using 50 components.

## Recommendation Evaluation

A leave-one-out evaluation strategy was used.

Customers with at least two unique purchased products were selected.

For each eligible customer:

1. One purchased product was held out as the test item.
2. Remaining interactions were used for recommendation.
3. Top-5 products were generated.
4. The system checked whether the held-out product appeared in the recommendation list.

A total of 1,159 customers were eligible for evaluation.

### Evaluation Metrics

The recommendation algorithms were evaluated using:

- Hit Rate@5
- Precision@5
- Recall@5
- Mean Reciprocal Rank@5
- Catalog Coverage@5

### Algorithm Comparison

| Algorithm | Hit Rate@5 | Precision@5 | Recall@5 | MRR@5 | Coverage@5 |
|---|---:|---:|---:|---:|---:|
| Popularity-Based | 0.003451 | 0.000690 | 0.003451 | 0.001582 | 0.006674 |
| Item-Based CF | 0.005177 | 0.001035 | 0.005177 | 0.001898 | 0.964405 |
| Truncated SVD | 0.002588 | 0.000518 | 0.002588 | 0.001898 | 0.294772 |

Item-Based Collaborative Filtering achieved the highest Hit Rate@5 and approximately 96.44% catalog coverage.

Therefore, Item-Based Collaborative Filtering was selected as the recommendation algorithm used in the interactive application.

## Recommendation System Limitations

The recommendation accuracy is limited by the characteristics of the dataset.

The dataset contains:

- 8,442 customers
- 899 products
- 25,000 interactions

This results in sparse customer-product interaction history.

Many customers have only a small number of sessions or purchases.

The dataset also does not maintain a fixed relationship between product IDs and product categories. A single product ID may appear under multiple categories.

Because of this dataset inconsistency, product-category-based recommendation filtering was not used.

The evaluation results are reported transparently rather than modifying the dataset to artificially increase recommendation performance.

## Streamlit Application

An interactive Streamlit application was developed to demonstrate the machine learning system.

The application contains four modules:

### Dashboard Overview

Displays:

- Dataset statistics
- Machine learning module summaries
- Recommendation algorithm comparison
- Evaluation metrics

### Purchase Prediction

Allows users to enter session information and estimate purchase probability using the trained Random Forest model.

### Customer Segmentation

Allows users to select a customer and inspect:

- Customer segment
- Purchase behavior
- Revenue
- Browsing activity
- Cart behavior

### Product Recommendation

Generates Top-5 personalized product recommendations using Item-Based Collaborative Filtering.

## Project Structure

```text
E-Commerce Customer Behavior and Recommendation System/
│
├── data/
│   └── Ecommerce.csv
│
├── models/
│   ├── customer_pca.pkl
│   ├── customer_scaler.pkl
│   ├── interaction_matrix.pkl
│   ├── item_similarity.pkl
│   ├── kmeans_model.pkl
│   ├── popular_products.pkl
│   ├── rf_model.pkl
│   └── svd_model.pkl
│
├── outputs/
│   ├── figures/
│   └── results/
│
├── src/
│   ├── compare_recommenders.py
│   ├── customer_segmentation.py
│   ├── data_understanding.py
│   ├── eda.py
│   ├── product_recommendation.py
│   └── purchase_prediction.py
│
├── app.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Machine Learning Pipeline

Run the project scripts in the following order:

```bash
python src/data_understanding.py
python src/eda.py
python src/purchase_prediction.py
python src/customer_segmentation.py
python src/product_recommendation.py
python src/compare_recommenders.py
```

## Running the Streamlit Application

Run:

```bash
streamlit run app.py
```

The application will start locally and can be accessed through the URL displayed by Streamlit.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Joblib
- Streamlit

## Conclusion

This project demonstrates an end-to-end e-commerce machine learning workflow combining customer behavior analysis, purchase prediction, customer segmentation, and product recommendation.

Random Forest was used for purchase intent prediction, K-Means clustering was used for behavioral customer segmentation, and three recommendation algorithms were evaluated.

Item-Based Collaborative Filtering achieved the best Hit Rate@5 among the evaluated recommenders and provided broad catalog coverage.

The project also highlights the importance of preventing target leakage, preserving an untouched test set, evaluating recommendation algorithms using held-out interactions, and transparently reporting limitations caused by sparse or inconsistent datasets.