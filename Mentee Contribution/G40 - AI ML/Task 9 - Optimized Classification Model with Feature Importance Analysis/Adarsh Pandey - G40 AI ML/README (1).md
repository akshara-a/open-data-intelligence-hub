# Customer Segmentation with Actionable Business Insights

An end-to-end machine learning project that segments customers using **RFM analysis
(Recency, Frequency, Monetary)** and **K-Means clustering**, then translates each
cluster into concrete business actions (retention, upsell, win-back campaigns, etc.).

---

## 📂 Project Files

| File | Description |
|---|---|
| `Customer_Segmentation.ipynb` | Full notebook: data cleaning → EDA → RFM → clustering → business insights. Runs directly in Google Colab or Jupyter. |
| `README.md` | This file. |

---

## 📊 Dataset

**Paste your dataset URL here:**

```
DATASET_URL = "PASTE_YOUR_DATASET_URL_HERE"
```

You'll paste this same link into **Step 2** of the notebook (`Customer_Segmentation.ipynb`).

### Recommended free datasets (transactional, works out of the box)
- **UCI Online Retail Dataset** — https://archive.ics.uci.edu/dataset/352/online+retail
- **Kaggle mirror (CSV)** — https://www.kaggle.com/datasets/carrie1/ecommerce-data
- **UCI Online Retail II (2009–2011)** — https://archive.ics.uci.edu/dataset/502/online+retail+ii

### Required columns
Your dataset should have (or be renamed to) these columns:

| Column | Meaning |
|---|---|
| `CustomerID` | Unique customer identifier |
| `InvoiceNo` | Order / transaction ID |
| `InvoiceDate` | Date of the transaction |
| `Quantity` | Units purchased |
| `UnitPrice` | Price per unit |

If your column names differ, edit the `COLUMN_MAP` dictionary in Step 2 of the notebook.

---

## 🚀 How to Run (Google Colab)

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Upload `Customer_Segmentation.ipynb` (**File → Upload notebook**)
3. In **Step 2 (Load Data)**, paste your dataset URL or upload the file manually
4. Click **Runtime → Run all**

## 🚀 How to Run (Local Jupyter)

```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
jupyter notebook Customer_Segmentation.ipynb
```

---

## 🧠 Methodology

1. **Data Cleaning** — remove cancelled orders, missing customer IDs, invalid quantities/prices
2. **RFM Feature Engineering**
   - Recency: days since last purchase
   - Frequency: number of distinct orders
   - Monetary: total amount spent
3. **Scaling** — log-transform + standardize (RFM is heavily skewed)
4. **Optimal k** — Elbow method + Silhouette score
5. **K-Means Clustering** — segment customers into groups
6. **PCA Visualization** — 2D view of segments
7. **Cluster Profiling** — average R/F/M per segment
8. **Business Insight Mapping** — label each cluster and assign an action

---

## 💡 Example Business Segments & Actions

| Segment | Signature | Action |
|---|---|---|
| Champions / VIPs | Recent, frequent, high spend | Loyalty rewards, early access, VIP treatment |
| Loyal Customers | Frequent, moderate spend | Upsell/cross-sell, referral requests |
| At-Risk Customers | Was active, now inactive | Win-back campaign with personalized discount |
| Lost / Dormant | Long inactive, low value | Low-cost reactivation email, then deprioritize |
| New Customers | Recent, low frequency | Onboarding nudge, second-purchase incentive |

Final output: `customer_segments.csv` — every customer with their RFM values, cluster, and segment label, ready to hand to marketing/CRM teams.

---

## 🛠️ Tech Stack
- Python, pandas, numpy
- scikit-learn (KMeans, PCA, StandardScaler, silhouette_score)
- matplotlib, seaborn
