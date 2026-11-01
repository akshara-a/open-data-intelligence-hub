# Building a Recommendation System for E-Commerce

## Contents
- `main.ipynb` — Main Colab/Jupyter notebook: EDA, popularity-based, content-based,
  item-based collaborative filtering, hybrid recommender, and evaluation (Precision@K).
- `ecommerce_dataset.csv` — E-commerce interaction dataset (users, products, categories,
  ratings, prices, purchases, timestamps).

## How to Run
1. Open `main.ipynb` in Google Colab (File > Upload notebook) or Jupyter.
2. Upload `ecommerce_dataset.csv` to the same Colab session (or place it in the same
   folder if running locally).
3. Run all cells top to bottom (Runtime > Run all).

## Dataset Columns
| Column | Description |
|---|---|
| user_id | Unique customer identifier |
| product_id | Unique product identifier |
| product_name | Product name |
| category | Product category |
| price | Product price ($) |
| rating | Rating given by user (1-5) |
| quantity | Quantity purchased/interacted with |
| purchased | 1 if the interaction resulted in a purchase, else 0 |
| timestamp | Date of interaction |
