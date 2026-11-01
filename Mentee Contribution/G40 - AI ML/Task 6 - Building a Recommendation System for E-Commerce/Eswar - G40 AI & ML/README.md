# E-Commerce Recommendation System — ML Model Comparison

Implementing and comparing regression, classification, and clustering algorithms
to support product recommendations, purchase-likelihood prediction, and customer
segmentation for an e-commerce business.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── ecommerce_customer_data.csv     # dataset
└── ecommerce_recommendation_system.ipynb   # main notebook (or paste cells into Colab)
```

## Dataset

**Source:** *Customer Shopping Trends Dataset* — a real, publicly available dataset
(3,900 customer transactions), originally published on Kaggle
(`iamsouravbanerjee/customer-shopping-trends-dataset`).

| Column | Description |
|---|---|
| Customer ID | Unique customer identifier |
| Age | Customer age |
| Gender | Male / Female |
| Item Purchased | Specific product bought |
| Category | Product category |
| Purchase Amount (USD) | Transaction value (used as `Price`) |
| Location | Customer's US state |
| Size, Color, Season | Product attributes |
| Review Rating | Customer's rating for the item (used as `Rating`) |
| Subscription Status | Yes/No — used as the classification target (proxy for purchase/conversion likelihood) |
| Shipping Type | Delivery method chosen |
| Discount Applied | Yes/No |
| Promo Code Used | Yes/No |
| Previous Purchases | Count of prior purchases by the customer |
| Payment Method | Payment type used |
| Frequency of Purchases | How often the customer shops |

### Note on schema mapping

The original task brief describes a generic schema (`User_ID`, `Browsing_Time`,
`Cart_Addition`, a binary `Purchase_Status`, etc.). No public dataset exposes
session-level browsing/cart data (that requires private clickstream logs), so
this project maps the brief's business concepts onto the closest real columns
available — most notably, **`Subscription Status` is used as the classification
target** in place of `Purchase_Status`, since every row in this dataset is
already a completed purchase and there's no "did not buy" class to predict.
This mapping is documented again inside the notebook.

## What's Implemented

| Part | Task | Algorithm | Target | Metrics |
|---|---|---|---|---|
| A | Regression | Ridge Regression | `Rating` | MAE, MSE, RMSE, R² |
| B | Classification | Logistic Regression | `Subscription_Status_flag` | Accuracy, Precision, Recall, F1, ROC-AUC |
| C | Clustering | K-Means | — (unsupervised) | Inertia, Silhouette Score, Elbow Method |
| D | Hyperparameter Tuning | GridSearchCV | Ridge `alpha`; Logistic `C`/`penalty`/`solver`; K-Means `n_clusters` | — |
| E | Model Comparison | — | — | Summary table + business interpretation |

## How to Run

### Option 1 — Google Colab
1. Open a new notebook at [colab.research.google.com](https://colab.research.google.com)
2. Upload `ecommerce_customer_data.csv` via the file browser (folder icon, left sidebar)
3. Paste the code cells in order (see project files) and run all
4. Colab already has all required libraries pre-installed — `requirements.txt`
   is included for reference / local use

### Option 2 — Local / Jupyter
```bash
pip install -r requirements.txt
jupyter notebook ecommerce_recommendation_system.ipynb
```
Make sure `ecommerce_customer_data.csv` is in the same folder as the notebook
(or update the path in the `pd.read_csv(...)` cell).

## Key Findings

- **Regression:** Ridge Regression shows ratings barely vary with price,
  discounts, or purchase history in this dataset (low R²) — most ratings sit
  in a narrow 3.0–3.8 band. Richer signals (per-product reviews, real browsing
  data) would be needed to meaningfully improve rating prediction.
- **Classification:** Logistic Regression separates likely subscribers/
  converters with a moderate ROC-AUC. `Previous_Purchases` and
  `Discount_Applied` are typically the strongest drivers — directly usable for
  targeting loyalty offers and discount campaigns.
- **Clustering:** K-Means (k chosen via Elbow + Silhouette analysis) reveals
  distinct customer segments (e.g. high-value spenders, discount-sensitive
  shoppers, low-engagement browsers), each suited to a different marketing
  strategy.
- **Business takeaway:** regression flags *what* to recommend, classification
  flags *who* is ready to convert, and clustering flags *how* to group
  customers for targeted campaigns.

## Author's Notes

This is an academic exercise mapping a course-style ML task brief onto a real
public dataset. See the notebook's introductory markdown cells for the full
column-mapping rationale.
