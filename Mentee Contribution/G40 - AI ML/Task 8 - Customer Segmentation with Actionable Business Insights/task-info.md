# Customer Segmentation with Actionable Business Insights

## Project Overview

In this project, students will analyze customer data and create meaningful customer segments using machine learning. The objective is not only to group similar customers but also to interpret each segment and recommend practical business actions.

Students will use clustering as the primary technique while applying regression, classification, hyperparameter optimization, and business-focused evaluation where appropriate.

---

## Business Scenario

An e-commerce company has collected customer information such as:

* Customer demographics
* Purchase frequency
* Total spending
* Average order value
* Product preferences
* Website activity
* Days since the last purchase
* Discount usage
* Customer ratings
* Purchase history

The company wants to understand different types of customers so that it can improve marketing campaigns, customer retention, product recommendations, and promotional strategies.

---

## Project Objective

Build a customer segmentation solution that:

1. Groups customers with similar purchasing behaviour.
2. Identifies the characteristics of each customer segment.
3. Predicts customer ratings or spending using regression.
4. Predicts purchase likelihood using classification.
5. Optimizes the selected machine-learning models.
6. Converts model results into actionable business recommendations.

---

## Concepts Mapped to the Project

### 1. Regression for Predicting Customer Ratings or Spending

Students can build a regression model to predict one of the following:

* Customer rating
* Total customer spending
* Average order value
* Expected future revenue
* Customer lifetime value

Recommended algorithms:

* Linear Regression
* Ridge Regression

Possible input features:

* Number of purchases
* Average order value
* Recency
* Website visits
* Discount usage
* Product categories purchased
* Customer tenure

Suggested evaluation metrics:

* Mean Absolute Error
* Mean Squared Error
* Root Mean Squared Error
* R² Score

---

### 2. Classification for Purchase Likelihood

Students can create a classification model to predict whether a customer is likely to make another purchase.

Example target:

* `1`: Customer is likely to purchase
* `0`: Customer is unlikely to purchase

Recommended algorithm:

* Logistic Regression

Possible input features:

* Days since last purchase
* Number of previous purchases
* Total spending
* Average rating
* Website activity
* Email engagement
* Discount usage
* Customer segment

Suggested evaluation metrics:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix
* ROC-AUC Score

Business interpretation should focus on identifying high-potential customers without wasting marketing resources on customers who are unlikely to respond.

---

### 3. Clustering for Customer Segmentation

Clustering is the main component of this mini project.

Students should use K-Means clustering to group customers based on their similarities.

Possible clustering features:

* Recency: Days since the customer’s last purchase
* Frequency: Number of purchases made
* Monetary Value: Total amount spent
* Average order value
* Number of website visits
* Discount usage percentage
* Customer ratings
* Product diversity

Students may also use the RFM approach:

* **Recency:** How recently the customer purchased
* **Frequency:** How often the customer purchases
* **Monetary Value:** How much the customer spends

Before applying K-Means, students should:

1. Handle missing values.
2. Remove or treat extreme outliers.
3. Convert categorical values where required.
4. Scale numerical features using StandardScaler or MinMaxScaler.
5. Select relevant features for clustering.

---

## Selecting the Number of Clusters

Students should not choose the number of clusters randomly.

The following methods should be used:

### Elbow Method

Run K-Means with different values of `k` and plot the inertia.

The point where the reduction in inertia begins to slow down can be selected as the appropriate number of clusters.

### Silhouette Score

Calculate the silhouette score for multiple values of `k`.

A higher silhouette score indicates that customers are better separated into distinct clusters.

Students should compare both methods before selecting the final number of clusters.

---

## Example Customer Segments

The final segments may look similar to the following:

### Segment 1: High-Value Loyal Customers

Characteristics:

* High purchase frequency
* High total spending
* Recent purchases
* High average order value

Business actions:

* Offer loyalty rewards.
* Provide early access to new products.
* Introduce premium membership benefits.
* Avoid excessive discounts because these customers already demonstrate strong purchase intent.

### Segment 2: New and Promising Customers

Characteristics:

* Recently joined
* Low-to-medium purchase frequency
* Good recent engagement
* Moderate spending

Business actions:

* Provide onboarding offers.
* Recommend popular products.
* Send personalized welcome campaigns.
* Encourage a second purchase.

### Segment 3: Discount-Driven Customers

Characteristics:

* Purchase mainly during promotions
* High discount usage
* Moderate purchase frequency
* Low or medium profit contribution

Business actions:

* Send targeted promotional offers.
* Use limited-time discounts.
* Recommend bundled products.
* Avoid giving unnecessary discounts outside campaign periods.

### Segment 4: At-Risk Customers

Characteristics:

* Previously active
* Long time since the last purchase
* Declining engagement
* Moderate or high historical spending

Business actions:

* Run re-engagement campaigns.
* Offer personalized comeback incentives.
* Request feedback about previous experiences.
* Highlight recently launched products.

### Segment 5: Low-Engagement Customers

Characteristics:

* Low purchase frequency
* Low total spending
* Limited website activity
* Long purchase intervals

Business actions:

* Use low-cost email campaigns.
* Promote entry-level products.
* Avoid expensive advertising campaigns.
* Analyze whether these customers should remain a priority group.

---

## Hyperparameter Optimization

Students should improve model performance by tuning hyperparameters.

### K-Means Hyperparameters

Possible parameters:

* `n_clusters`
* `init`
* `n_init`
* `max_iter`
* `random_state`

For K-Means, students can compare different cluster counts using:

* Silhouette score
* Inertia
* Cluster size distribution

### Logistic Regression Hyperparameters

Possible parameters:

* `C`
* `penalty`
* `solver`
* `max_iter`

### Ridge Regression Hyperparameters

Possible parameter:

* `alpha`

Students can use:

* GridSearchCV
* RandomizedSearchCV

The optimized model should be compared with the initial baseline model.

---

## Suggested Dataset Columns

A dataset may contain the following columns:

| Column                | Description                                      |
| --------------------- | ------------------------------------------------ |
| CustomerID            | Unique customer identifier                       |
| Age                   | Customer age                                     |
| Gender                | Customer gender                                  |
| AnnualIncome          | Estimated annual income                          |
| TotalSpending         | Total amount spent                               |
| PurchaseFrequency     | Number of purchases                              |
| AverageOrderValue     | Average value per order                          |
| DaysSinceLastPurchase | Number of days since the previous purchase       |
| WebsiteVisits         | Number of website visits                         |
| DiscountUsage         | Percentage of purchases made using discounts     |
| CustomerRating        | Average rating provided by the customer          |
| ProductCategory       | Most frequently purchased category               |
| PurchaseLikelihood    | Whether the customer is likely to purchase again |

Students may use a public customer segmentation dataset or create a realistic synthetic dataset.

---

## Project Workflow

### Step 1: Understand the Business Problem

Clearly define:

* Why customer segmentation is required
* Who will use the results
* Which business decisions the segments will support

### Step 2: Perform Exploratory Data Analysis

Students should examine:

* Dataset shape
* Data types
* Missing values
* Duplicate records
* Feature distributions
* Correlations
* Outliers
* Customer spending patterns
* Purchase frequency patterns

Recommended visualizations:

* Histograms
* Box plots
* Scatter plots
* Correlation heatmap
* Spending distribution
* Recency versus frequency plot

### Step 3: Prepare the Data

Tasks include:

* Removing customer identifiers from model features
* Handling missing data
* Encoding categorical variables
* Scaling numerical columns
* Treating outliers
* Creating derived features such as RFM values

### Step 4: Build the Clustering Model

Students should:

1. Select clustering features.
2. Scale the features.
3. test different values of `k`.
4. Use the elbow method.
5. Calculate silhouette scores.
6. Fit the final K-Means model.
7. Assign a cluster label to every customer.

### Step 5: Profile the Segments

For every cluster, calculate:

* Number of customers
* Average spending
* Average purchase frequency
* Average recency
* Average order value
* Average rating
* Average discount usage
* Percentage contribution to total revenue

Students should assign a meaningful business name to each cluster.

### Step 6: Build the Regression Model

Predict customer rating, future spending, or customer lifetime value.

Students should compare:

* Linear Regression
* Ridge Regression

### Step 7: Build the Classification Model

Predict whether a customer is likely to make another purchase.

Students should:

* Create training and testing datasets.
* Train Logistic Regression.
* Generate a confusion matrix.
* Evaluate precision, recall, F1-score, and ROC-AUC.

### Step 8: Tune the Models

Use GridSearchCV or RandomizedSearchCV to optimize the selected models.

Compare model performance before and after tuning.

### Step 9: Generate Business Insights

Students must explain:

* Which customer segment generates the highest revenue
* Which segment has the highest churn or inactivity risk
* Which customers should receive loyalty rewards
* Which segment is most responsive to discounts
* Which customers require re-engagement
* Which segment should receive premium product recommendations

### Step 10: Present the Results

The final presentation should communicate technical results in business-friendly language.

---

## Business-Focused Evaluation

Model evaluation should go beyond technical scores.

Students should answer questions such as:

* Can the segments be clearly distinguished?
* Are the segment sizes meaningful?
* Can the marketing team take different actions for each segment?
* Does the purchase prediction model identify high-potential customers?
* Does the regression model provide useful spending or rating estimates?
* Can the recommendations improve revenue or retention?
* Is the cost of the campaign justified by the expected business value?

---

## Required Visualizations

Students should include:

1. Customer spending distribution
2. Recency, frequency, and monetary-value analysis
3. Elbow method graph
4. Silhouette score comparison
5. Two-dimensional cluster visualization
6. Cluster-wise customer count
7. Cluster-wise average spending
8. Cluster-wise purchase frequency
9. Confusion matrix for classification
10. Actual versus predicted values for regression

---

## Sample Python Libraries

Students may use:

```python
pandas
numpy
matplotlib
scikit-learn
```

Recommended scikit-learn components:

```python
StandardScaler
MinMaxScaler
KMeans
PCA
LinearRegression
Ridge
LogisticRegression
GridSearchCV
train_test_split
silhouette_score
mean_absolute_error
mean_squared_error
r2_score
classification_report
confusion_matrix
roc_auc_score
```

---

## Suggested Project Structure

```text
customer-segmentation-project/
│
├── data/
│   └── customer_data.csv
│
├── notebooks/
│   └── customer_segmentation.ipynb
│
├── src/
│   ├── data_preprocessing.py
│   ├── clustering.py
│   ├── regression.py
│   ├── classification.py
│   └── model_evaluation.py
│
├── reports/
│   ├── customer_segments.csv
│   ├── business_insights.md
│   └── visualizations/
│
├── README.md
└── requirements.txt
```

---

## Expected Deliverables

### 1. Jupyter Notebook

The notebook should contain:

* Data loading
* Exploratory data analysis
* Data preprocessing
* Clustering
* Regression
* Classification
* Hyperparameter optimization
* Model evaluation
* Business interpretation

### 2. Customer Segment Report

A report containing:

* Segment names
* Segment characteristics
* Segment size
* Revenue contribution
* Recommended business action

### 3. Model Comparison Table

| Model               | Objective                   | Baseline Performance | Tuned Performance | Selected Model |
| ------------------- | --------------------------- | -------------------: | ----------------: | -------------- |
| K-Means             | Customer segmentation       |     Silhouette score |  Silhouette score | Yes/No         |
| Linear Regression   | Predict customer value      |          RMSE and R² |       RMSE and R² | Yes/No         |
| Ridge Regression    | Predict customer value      |          RMSE and R² |       RMSE and R² | Yes/No         |
| Logistic Regression | Predict purchase likelihood |       F1 and ROC-AUC |    F1 and ROC-AUC | Yes/No         |

### 4. Business Recommendation Document

The document should contain at least one actionable recommendation for every customer segment.

### 5. Presentation

A presentation of approximately 8 to 12 slides covering:

* Business problem
* Dataset
* Data analysis
* Model selection
* Customer segments
* Model performance
* Business insights
* Final recommendations

---

## Mentor Validation Criteria

The project will be evaluated based on:

| Evaluation Area       | Expected Outcome                                            |
| --------------------- | ----------------------------------------------------------- |
| Data Preparation      | Data is cleaned, transformed, and scaled correctly          |
| Exploratory Analysis  | Important customer behaviour patterns are identified        |
| Clustering            | Appropriate features and cluster count are selected         |
| Segment Profiling     | Every segment is clearly described and named                |
| Regression            | Customer rating or value is predicted and evaluated         |
| Classification        | Purchase likelihood is predicted using suitable metrics     |
| Hyperparameter Tuning | At least one model is optimized                             |
| Business Insights     | Model findings are converted into practical recommendations |
| Visualization         | Results are communicated through meaningful charts          |
| Code Quality          | Code is readable, reusable, and properly organized          |

---

## AI-Augmented Activities

Students may use AI tools to:

* Understand suitable features for segmentation
* Explore alternative cluster interpretations
* Debug preprocessing and model-training issues
* Compare model evaluation metrics
* Analyze hyperparameter sensitivity
* Improve visualization explanations
* Convert technical results into business recommendations

Students must validate AI-generated suggestions using dataset evidence and model results.

---

## Final Project Outcome

At the end of the project, students should be able to:

* Prepare customer data for machine learning
* Apply K-Means clustering
* Identify an appropriate number of customer segments
* Interpret customer behaviour within each segment
* Build regression and classification models
* Optimize model performance
* Evaluate models using technical and business metrics
* Present actionable recommendations to marketing and business teams
