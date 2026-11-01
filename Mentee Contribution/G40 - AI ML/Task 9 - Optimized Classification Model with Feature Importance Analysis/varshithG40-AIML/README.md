# 🛒 E-Commerce Purchase Prediction System

## Complete ML Pipeline + Modern Web Interface

A production-ready machine learning system that predicts whether an e-commerce customer will make a purchase, featuring a beautiful interactive web dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

---

## 📁 Project Structure

```
optimization/
├── data/
│   ├── ecommerce_customer_data.csv      # Synthetic dataset (5,000 customers)
│   └── generate_data.py                 # Data generation script
├── notebooks/
│   ├── purchase_prediction_analysis.ipynb  # Main analysis notebook
│   ├── purchase_prediction_analysis.py     # Python script version
│   └── figures/                            # Generated visualizations
├── models/
│   ├── purchase_prediction_model.pkl       # Saved model pipeline
│   └── model_metadata.json                 # Model metadata
├── reports/
│   ├── feature_importance_report.md        # Feature analysis report
│   └── business_recommendations.md         # Business recommendations
├── .streamlit/
│   └── config.toml                         # Streamlit configuration
├── app.py                                  # 🌐 Web interface (Streamlit)
├── requirements.txt                        # Python dependencies
└── README.md                               # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Generate the Dataset (optional - data is already included)

```bash
python data/generate_data.py
```

### 3. Run the Web Interface 🌐

```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**

### 4. Run the Analysis Notebook 📓

```bash
jupyter notebook notebooks/purchase_prediction_analysis.ipynb
```

---

## 🌐 Web Interface Features

The modern web dashboard includes 5 sections:

| Page | Description |
|------|-------------|
| **🏠 Dashboard** | Live metrics, dataset overview, purchase distribution charts |
| **🎯 Predict** | Interactive form to predict purchase probability for any customer |
| **📊 Model Performance** | Accuracy, F1, ROC-AUC, model comparison charts |
| **🔍 Feature Analysis** | Top 10 features, importance breakdown, correlations |
| **💡 Business Insights** | 8 actionable recommendations with roadmap |

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **F1-Score** | 0.6502 |
| **ROC-AUC** | 0.8296 |
| **Precision** | 0.5866 |
| **Recall** | 0.7292 |
| **Accuracy** | 0.7450 |

**Best Model:** Logistic Regression (Optimized) with `class_weight='balanced'`

---

## 🔑 Key Features

- ✅ **5,000 customer records** with 18 features
- ✅ **Moderate class imbalance** (32% purchasers, 68% non-purchasers)
- ✅ **Full ML pipeline**: EDA → Preprocessing → Training → Tuning → Evaluation
- ✅ **No data leakage**: Pipeline-based preprocessing with stratified splitting
- ✅ **3 baseline models** + hyperparameter optimization via GridSearchCV
- ✅ **Class imbalance handling**: `class_weight='balanced'` vs SMOTE comparison
- ✅ **Permutation importance** + coefficient analysis
- ✅ **Threshold optimization** for best F1-score
- ✅ **Customer segmentation**: Low / Medium / High likelihood
- ✅ **8 business recommendations** with expected impact

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **scikit-learn** — ML models and preprocessing
- **pandas / numpy** — Data manipulation
- **matplotlib / seaborn** — Static visualizations
- **imbalanced-learn** — SMOTE oversampling
- **Streamlit** — Web interface
- **Plotly** — Interactive charts

---

## 📝 Usage Examples

### Predict a New Customer

1. Open the web app at http://localhost:8501
2. Go to **"🎯 Predict Purchase"**
3. Enter customer details (age, cart items, time on site, etc.)
4. Click **"🔮 Predict Purchase Likelihood"**
5. View probability, customer segment, and key influencing factors

### Use the Model Programmatically

```python
import joblib
import pandas as pd

# Load the model
model = joblib.load('models/purchase_prediction_model.pkl')

# Create customer data
customer = pd.DataFrame({
    'Age': [35],
    'Gender': ['Female'],
    'Location': ['Urban'],
    'DeviceType': ['Mobile'],
    'TrafficSource': ['Organic Search'],
    'PagesViewed': [10],
    'TimeOnSite': [25.0],
    'ProductsViewed': [12],
    'CartItems': [2],
    'PreviousPurchases': [5],
    'AverageOrderValue': [150.0],
    'DiscountUsed': [1],
    'EmailClicked': [1],
    'AdClicked': [0],
    'ReviewScoreViewed': [4.5],
    'DaysSinceLastVisit': [10],
    'SessionCount': [8]
})

# Predict
probability = model.predict_proba(customer)[0][1]
print(f"Purchase probability: {probability:.1%}")
```

---

## 📋 Dataset Description

| Feature | Type | Description |
|---------|------|-------------|
| CustomerID | ID | Unique customer identifier |
| Age | Numeric | Customer age (18-75) |
| Gender | Categorical | Male / Female |
| Location | Categorical | Urban / Suburban / Rural |
| DeviceType | Categorical | Desktop / Mobile / Tablet |
| TrafficSource | Categorical | How customer arrived |
| PagesViewed | Numeric | Pages viewed in session |
| TimeOnSite | Numeric | Minutes spent on site |
| ProductsViewed | Numeric | Number of products viewed |
| CartItems | Numeric | Items added to cart |
| PreviousPurchases | Numeric | Historical purchase count |
| AverageOrderValue | Numeric | Average past order value ($) |
| DiscountUsed | Binary | Used a discount (0/1) |
| EmailClicked | Binary | Clicked email campaign (0/1) |
| AdClicked | Binary | Clicked an ad (0/1) |
| ReviewScoreViewed | Numeric | Avg review score of viewed products |
| DaysSinceLastVisit | Numeric | Days since previous visit |
| SessionCount | Numeric | Total sessions |
| **Purchase** | **Target** | **Made a purchase (0/1)** |

---

## 📊 Verification Checklist

- [x] Script runs end-to-end without errors
- [x] F1 > 0.65 on test set
- [x] ROC-AUC > 0.80 on test set
- [x] No data leakage (preprocessing inside pipeline)
- [x] Stratified train/test split preserves class distribution
- [x] Feature importance aligns with data generation logic
- [x] Web interface loads and predicts correctly

---

## 📄 License

This project is for educational and demonstration purposes.
