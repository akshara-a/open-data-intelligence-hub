# Shop Sense AI - E-Commerce Recommendation System

## Project Overview

Shop Sense AI is a machine learning-based e-commerce recommendation system designed to analyze customer behavior, predict product ratings, estimate purchase likelihood, segment customers, and generate personalized product recommendations.

The project combines regression, classification, clustering, and hyperparameter optimization to solve multiple business problems in an e-commerce environment.

The final recommendation engine uses predicted product ratings, purchase probabilities, and customer behavioral segments to rank products for individual customers.

## Business Problem

E-commerce platforms collect large amounts of customer interaction data, including browsing activity, cart additions, purchase history, product ratings, and transaction information.

The objective of this project is to use machine learning to:

* Predict customer product ratings.
* Predict whether a customer is likely to purchase a product.
* Segment customers based on shopping behavior.
* Optimize machine learning models using hyperparameter tuning.
* Generate personalized Top-N product recommendations.
* Align model outputs with e-commerce business objectives.

## Machine Learning Tasks

| Machine Learning Task       | Algorithm                      | Purpose                                |
| --------------------------- | ------------------------------ | -------------------------------------- |
| Regression                  | Linear Regression              | Predict customer product ratings       |
| Regression                  | Ridge Regression               | Predict ratings using regularization   |
| Classification              | Logistic Regression            | Predict purchase likelihood            |
| Clustering                  | K-Means Clustering             | Segment customers based on behavior    |
| Hyperparameter Optimization | GridSearchCV                   | Optimize model parameters              |
| Recommendation              | Segment-Aware Weighted Ranking | Generate Top-N product recommendations |

## Dataset

The project uses an e-commerce customer behavior dataset containing 25,000 records and 29 original features.

Important dataset features include:

* `customer_id`
* `session_id`
* `product_id`
* `product_category`
* `unit_price`
* `quantity`
* `discount_percent`
* `revenue`
* `pages_viewed`
* `time_on_site_sec`
* `added_to_cart`
* `purchased`
* `cart_abandoned`
* `rating`
* `marketing_channel`
* `device_type`
* `user_type`
* `location`

Two additional features were created during preprocessing:

* `discount_applied`
* `engagement_score`

After feature engineering, the processed dataset contains 31 columns.

## Project Workflow

The project follows the machine learning workflow shown below:

```text
E-Commerce Dataset
        |
        v
Data Preprocessing
        |
        v
Exploratory Data Analysis
        |
        +-----------------------+
        |                       |
        v                       v
Rating Prediction        Purchase Prediction
Linear / Ridge           Logistic Regression
Regression                      |
        |                       |
        +-----------+-----------+
                    |
                    v
          Customer Segmentation
            K-Means Clustering
                    |
                    v
        Hyperparameter Optimization
                GridSearchCV
                    |
                    v
       Segment-Aware Recommendation
                    |
                    v
         Top-N Product Recommendations
```

## Data Preprocessing

The preprocessing phase performs the following operations:

* Duplicate record detection.
* Missing value analysis.
* Binary feature validation.
* Rating range validation.
* Negative numerical value validation.
* Identifier column identification.
* Feature engineering.
* Processed dataset generation.

The dataset contained:

* 0 duplicate records.
* 0 missing values.
* Valid binary purchase and cart features.
* Ratings ranging from 1 to 5.

### Feature Engineering

#### Discount Applied

A binary feature is created to identify whether a discount was applied to a product.

```text
discount_percent > 0
        |
        v
discount_applied = 1
```

#### Engagement Score

Customer browsing engagement is represented using:

```text
engagement_score = pages_viewed × time_on_site_sec
```

## Exploratory Data Analysis

Exploratory Data Analysis was performed to understand customer shopping behavior and dataset patterns.

The following analyses were performed:

* Rating distribution.
* Purchase distribution.
* Average rating by product category.
* Browsing time versus purchase behavior.
* Cart addition versus purchase behavior.
* Discount usage versus purchase behavior.
* Revenue distribution.
* Feature correlation analysis.

### Important EDA Findings

| Business Metric                     | Result |
| ----------------------------------- | -----: |
| Overall Purchase Rate               | 22.46% |
| Average Customer Rating             |   3.95 |
| Average Revenue per Session         | 404.65 |
| Purchase Rate After Cart Addition   | 34.85% |
| Purchase Rate Without Cart Addition |  0.00% |
| Purchase Rate With Discount         | 22.49% |
| Purchase Rate Without Discount      | 22.43% |

Cart addition was identified as an important indicator of purchase behavior.

Customers who did not add products to their carts had a 0% purchase rate in the dataset.

Discount usage showed very little difference in overall purchase rate.

## Regression - Rating Prediction

Regression models were developed to predict the rating a customer may give to a product.

### Models

* Linear Regression
* Ridge Regression

### Target Variable

`rating`

### Evaluation Metrics

* Mean Absolute Error
* Mean Squared Error
* Root Mean Squared Error
* R² Score

### Model Results

| Model                  |      MAE |      MSE |     RMSE | R² Score |
| ---------------------- | -------: | -------: | -------: | -------: |
| Linear Regression      | 0.232262 | 0.301130 | 0.548753 | 0.006290 |
| Ridge Regression       | 0.232261 | 0.301130 | 0.548753 | 0.006290 |
| Tuned Ridge Regression | 0.232168 | 0.301130 | 0.548753 | 0.006291 |

The tuned Ridge Regression model was selected for rating estimation.

The model achieved a low Mean Absolute Error. However, the low R² score indicates that the available features explain only a limited amount of rating variation.

The dataset contains a large concentration of ratings around 4, which limits rating variability and causes predictions to remain close to the average rating.

## Classification - Purchase Likelihood Prediction

Logistic Regression was used to predict whether a customer is likely to purchase a product.

### Target Variable

`purchased`

The target values are:

```text
0 = Not Purchased
1 = Purchased
```

### Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC

### Logistic Regression Results

| Metric    |   Result |
| --------- | -------: |
| Accuracy  | 0.572600 |
| Precision | 0.344479 |
| Recall    | 1.000000 |
| F1-Score  | 0.512434 |
| ROC-AUC   | 0.762440 |

The Logistic Regression model achieved 100% recall on the test data.

This means the model successfully identified all actual purchasing customers in the test set.

However, the lower precision indicates that the model also classified several non-purchasing customers as potential buyers.

The model is therefore suitable for broad customer targeting scenarios where missing a potential buyer is considered costly.

## Customer Segmentation

K-Means Clustering was used to segment customers based on shopping behavior.

Session-level data was aggregated into customer-level behavioral profiles.

### Customer Features

* Total sessions.
* Average pages viewed.
* Average time on site.
* Cart addition rate.
* Purchase rate.
* Total purchases.
* Average rating.
* Total revenue.
* Average discount.
* Average engagement.

### Optimal Number of Clusters

K values from 2 to 10 were evaluated using:

* Inertia.
* Elbow Method.
* Silhouette Score.

The highest Silhouette Score was obtained for:

```text
K = 2
Silhouette Score = 0.1959
```

Therefore, two customer segments were selected.

### Identified Customer Segments

#### Low-Conversion Browsers

These customers browse products and frequently interact with the e-commerce platform but rarely complete purchases.

Characteristics include:

* Lower purchase rate.
* Very low revenue contribution.
* Moderate cart activity.
* Lower number of sessions.

Possible business strategies include:

* Cart recovery campaigns.
* Personalized product suggestions.
* Purchase reminders.
* Limited promotional offers.

#### Active High-Value Buyers

These customers demonstrate stronger purchasing behavior and generate significantly greater revenue.

Characteristics include:

* Higher purchase rate.
* More completed purchases.
* Higher cart addition rate.
* Greater revenue contribution.
* More customer sessions.

Possible business strategies include:

* Loyalty rewards.
* Premium product recommendations.
* Cross-selling.
* Upselling.
* Personalized offers.

The Silhouette Score indicates that the customer segments have limited separation. Therefore, the clustering result should be interpreted as broad behavioral segmentation rather than strongly isolated customer groups.

## Hyperparameter Optimization

GridSearchCV was used to optimize the regression and classification models.

### Ridge Regression

The following `alpha` values were evaluated:

```text
0.01
0.1
1.0
10.0
100.0
```

The best parameter was:

```text
alpha = 100.0
```

The tuned Ridge Regression model achieved:

```text
MAE      = 0.232168
RMSE     = 0.548753
R² Score = 0.006291
```

### Logistic Regression

The following parameters were optimized:

* `C`
* `l1_ratio`
* `max_iter`

The best parameters were:

```text
C = 0.01
l1_ratio = 1.0
max_iter = 500
```

The tuned Logistic Regression achieved a ROC-AUC score of 0.761092.

The original Logistic Regression achieved a slightly higher ROC-AUC score of 0.762440.

Therefore, the original Logistic Regression model was selected for the final recommendation engine.

Model selection was based on held-out evaluation performance rather than assuming that the tuned model would always perform better.

## Shop Sense AI Recommendation Engine

The recommendation engine combines the outputs of multiple machine learning tasks.

The system uses:

```text
Tuned Ridge Regression
        |
        v
Predicted Product Rating

Original Logistic Regression
        |
        v
Purchase Probability

K-Means Clustering
        |
        v
Customer Segment
```

The customer segment determines the recommendation ranking strategy.

### Low-Conversion Browsers

For Low-Conversion Browsers, purchase probability receives greater importance.

```text
Recommendation Score
=
70% Purchase Probability
+
30% Normalized Predicted Rating
```

The objective is to prioritize products with greater purchase conversion potential.

### Active High-Value Buyers

For Active High-Value Buyers, predicted rating receives greater importance.

```text
Recommendation Score
=
40% Purchase Probability
+
60% Normalized Predicted Rating
```

The objective is to prioritize products that active buyers may prefer and rate highly.

## Recommendation Process

The recommendation engine performs the following steps:

1. Identifies the customer.
2. Retrieves the customer's behavioral segment.
3. Creates a customer behavioral profile.
4. Identifies products the customer has not previously purchased.
5. Creates candidate customer-product records.
6. Predicts product ratings using Tuned Ridge Regression.
7. Estimates purchase probability using Logistic Regression.
8. Applies segment-specific recommendation weights.
9. Calculates the recommendation score.
10. Ranks candidate products.
11. Returns the Top-N product recommendations.

## Model Comparison

| Model                     | ML Task               | Main Metric      | Business Value                        |
| ------------------------- | --------------------- | ---------------- | ------------------------------------- |
| Linear Regression         | Rating Prediction     | RMSE             | Predict product ratings               |
| Ridge Regression          | Rating Prediction     | RMSE             | Rating prediction with regularization |
| Tuned Ridge Regression    | Rating Prediction     | RMSE             | Estimate product preference           |
| Logistic Regression       | Purchase Prediction   | ROC-AUC          | Identify potential buyers             |
| Tuned Logistic Regression | Purchase Prediction   | ROC-AUC          | Optimized purchase prediction         |
| K-Means Clustering        | Customer Segmentation | Silhouette Score | Group customers by shopping behavior  |

## Business Value

Shop Sense AI can support the following e-commerce business activities:

* Personalized product recommendations.
* Purchase likelihood prediction.
* Customer segmentation.
* Cart recovery campaigns.
* Targeted marketing.
* Loyalty strategies.
* Product ranking.
* Cross-selling and upselling.
* Customer conversion analysis.

## Project Structure

```text
Building a Recommendation System for E-Commerce
|
|-- main.py
|-- README.md
|-- requirements.txt
|
|-- data
|   |-- Ecommerce.csv
|   |-- processed_ecommerce_data.csv
|
|-- outputs
|   |-- plots
|   |-- results
|
|-- src
    |-- preprocessing.py
    |-- eda.py
    |-- regression.py
    |-- classification.py
    |-- clustering.py
    |-- hyperparameter_tuning.py
    |-- recommendation.py
    |-- evaluation.py
```

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Project

Run the complete machine learning pipeline using:

```bash
python main.py
```

The program performs:

```text
Data Loading
    |
Data Preprocessing
    |
Exploratory Data Analysis
    |
Regression
    |
Classification
    |
Customer Segmentation
    |
Hyperparameter Optimization
    |
Recommendation Generation
    |
Final Model Evaluation
```

Generated plots are stored in:

```text
outputs/plots/
```

Generated model results and recommendations are stored in:

```text
outputs/results/
```

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn

## Final Conclusion

Shop Sense AI demonstrates how regression, classification, and clustering can be combined to solve multiple e-commerce business problems.

Tuned Ridge Regression is used to estimate customer product ratings. Logistic Regression estimates purchase likelihood, while K-Means Clustering identifies customer behavioral segments.

The final segment-aware recommendation engine combines predicted rating and purchase probability using different ranking weights for each customer segment.

This approach enables the e-commerce platform to generate personalized Top-N product recommendations while aligning recommendation ranking with customer behavior and business objectives.

The project also demonstrates that hyperparameter tuning does not always guarantee better test-set performance. Final model selection was therefore based on evaluation metrics and business relevance.

Overall, the system can support personalized recommendations, customer targeting, purchase conversion strategies, and improved e-commerce decision-making.
