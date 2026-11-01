# 📊 Customer Segmentation with Actionable Business Insights

> **Task 8 — Machine Learning Project**  
> An end-to-end customer segmentation solution using K-Means Clustering, Logistic Regression, Ridge Regression, and hyperparameter optimisation.

---

## 🎯 Project Overview

An e-commerce company collected customer data covering demographics, purchase behaviour, and website activity. This project builds a complete ML pipeline to:

1. **Segment** customers into meaningful groups using K-Means clustering (RFM approach).
2. **Predict** purchase likelihood using Logistic Regression.
3. **Predict** total spending using Linear Regression and Ridge Regression.
4. **Optimise** models with GridSearchCV hyperparameter tuning.
5. **Recommend** business actions for each customer segment.

---

## 📁 Project Structure

```
Task-8-Customer-Segmentation/
│
├── data/
│   ├── customer_data.csv            ← Raw dataset (1,001 rows × 13 columns)
│   └── cleaned_customer_data.csv    ← Preprocessed dataset (auto-generated)
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py        ← Data loading, cleaning, encoding, scaling
│   ├── exploratory_analysis.py      ← EDA visualisations
│   ├── clustering.py                ← K-Means, Elbow, Silhouette, PCA
│   ├── classification.py            ← Logistic Regression for purchase likelihood
│   ├── regression.py                ← Linear + Ridge Regression for spending
│   ├── hyperparameter_tuning.py     ← GridSearchCV for classifier & regressor
│   ├── model_evaluation.py          ← Shared evaluation metrics utilities
│   └── business_insights.py        ← Segment recommendations & markdown report
│
├── notebooks/
│   └── Task8_Customer_Segmentation.ipynb   ← Complete walkthrough notebook
│
├── images/                          ← Auto-generated visualisations
│   ├── spending_distribution.png
│   ├── correlation_heatmap.png
│   ├── boxplot_outliers.png
│   ├── purchase_frequency.png
│   ├── average_spending.png
│   ├── elbow_method.png
│   ├── silhouette_scores.png
│   ├── customer_clusters.png
│   ├── cluster_counts.png
│   ├── confusion_matrix.png
│   └── regression_results.png
│
├── outputs/                         ← Auto-generated results
│   ├── clustered_customers.csv      ← All customers with assigned Cluster label
│   ├── customer_segments.csv        ← Cluster-level statistics & names
│   ├── classification_predictions.csv
│   ├── regression_predictions.csv
│   └── business_recommendations.md  ← Actionable business report
│
├── app.py                           ← Streamlit dashboard + pipeline runner
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

| Column | Description |
|--------|-------------|
| CustomerID | Unique customer identifier |
| Age | Customer age |
| Gender | Male / Female |
| AnnualIncome | Estimated annual income ($) |
| TotalSpending | Total amount spent ($) |
| PurchaseFrequency | Number of purchases |
| AverageOrderValue | Average value per order ($) |
| DaysSinceLastPurchase | Days since the last purchase (Recency) |
| WebsiteVisits | Number of website visits |
| DiscountUsage | Fraction of purchases made using discounts |
| CustomerRating | Average rating (1–5) |
| ProductCategory | Most frequently purchased category |
| PurchaseLikelihood | Target: 1 = likely to purchase, 0 = unlikely |

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Full ML Pipeline

```bash
python app.py
```

This generates all outputs, images, and predictions automatically.

### 3. Launch the Interactive Dashboard

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧠 ML Models Used

| Model | Task | Evaluation Metrics |
|-------|------|--------------------|
| K-Means Clustering | Customer Segmentation | Silhouette Score, Inertia |
| Logistic Regression | Purchase Likelihood | Accuracy, F1, ROC-AUC |
| Linear Regression | Spending Prediction | MAE, RMSE, R² |
| Ridge Regression | Spending Prediction | MAE, RMSE, R² |

---

## 🏷️ Customer Segments

| Segment | Profile | Business Action |
|---------|---------|-----------------|
| 👑 High-Value Loyal | High frequency, high spending, recent | Loyalty rewards, VIP access |
| 🌱 New & Promising | Recently acquired, moderate engagement | Onboarding offers, 2nd-purchase push |
| 🏷️ Discount-Driven | Purchase mainly on promotion | Targeted flash sales, bundling |
| ⚠️ At-Risk | Previously active, declining | Re-engagement campaigns |
| 💤 Low-Engagement | Low frequency, low spending | Low-cost email, entry-level products |

---

## 📈 Required Visualisations (All Generated)

1. ✅ Customer spending distribution
2. ✅ Recency, frequency, and monetary-value analysis
3. ✅ Elbow method graph
4. ✅ Silhouette score comparison
5. ✅ 2D cluster visualisation (PCA)
6. ✅ Cluster-wise customer count
7. ✅ Cluster-wise average spending (segment profiles)
8. ✅ Cluster-wise purchase frequency (segment profiles)
9. ✅ Confusion matrix for classification
10. ✅ Actual vs Predicted values for regression

---

## 🛠️ Libraries Used

```python
pandas        # Data manipulation
numpy         # Numerical computation
matplotlib    # Plotting
seaborn       # Statistical visualisation
scikit-learn  # ML models, preprocessing, evaluation
streamlit     # Interactive dashboard
```

---

## 📝 Results Summary

- **Clustering:** K-Means identifies 4–5 distinct customer segments using RFM features.
- **Classification:** Logistic Regression predicts purchase likelihood (F1 ≥ 0.70 after tuning).
- **Regression:** Ridge Regression predicts total spending (R² ≥ 0.50).
- **Business Report:** `outputs/business_recommendations.md` contains segment profiles and actionable strategies.

---

*Developed as part of the ML project series — Task 8.*
