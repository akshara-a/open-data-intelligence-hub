# Multi-Algorithm E-Commerce Recommendation System

A machine learning mini-project comparing **regression**, **classification**, and **clustering** approaches for e-commerce product recommendations and customer segmentation.

## Features

- **Regression**: Predict user ratings (Linear, Ridge, Random Forest, Gradient Boosting)
- **Classification**: Predict purchase likelihood (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, SVM)
- **Clustering**: Segment customers (K-Means, Agglomerative, DBSCAN)
- **Hyperparameter tuning** via GridSearchCV
- **Extended model comparison table** with 14 algorithm entries

## Quick Start

```bash
pip install -r requirements.txt
python generate_data.py
python recommendation_system.py
```

### Web Interface

```bash
streamlit run app.py
# or
python app.py
```

Opens a browser UI with:
- **Dashboard** — dataset overview, EDA charts, best models
- **Rating Predictor** — predict product ratings (Gradient Boosting)
- **Purchase Predictor** — predict purchase likelihood (Logistic Regression)
- **Customer Segments** — lookup or predict K-Means clusters
- **Model Comparison** — full 14-algorithm metrics table

## Outputs

| Path | Description |
| ---- | ----------- |
| `data/ecommerce_data.csv` | Synthetic dataset (5,000+ rows) |
| `outputs/model_results.json` | All evaluation metrics |
| `outputs/*.png` | EDA and model visualizations |
| `REPORT.md` | Full project report with business insights |

## Project Structure

```
algo/
├── app.py                    # Streamlit web interface
├── model_service.py          # Model loading & prediction API
├── generate_data.py          # Dataset generator
├── recommendation_system.py  # Main ML pipeline
├── requirements.txt
├── REPORT.md                 # Final deliverable report
├── data/
│   └── ecommerce_data.csv
└── outputs/
    ├── model_results.json
    ├── customer_segments.csv
    ├── eda_overview.png
    ├── confusion_matrix.png
    ├── clustering_elbow_silhouette.png
    └── kmeans_clusters.png
```

## Best Models (from executed results)

| Task | Best Algorithm | Key Metric |
| ---- | -------------- | ---------- |
| Regression | Gradient Boosting Regressor | R² = 0.374 |
| Classification | Tuned Logistic Regression | F1 = 0.873 |
| Clustering | K-Means (k=6) | Silhouette = 0.172 |

See `REPORT.md` for the full extended comparison table and business interpretation.
