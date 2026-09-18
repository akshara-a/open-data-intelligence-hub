# 🛍️ Multi-Algorithm Recommendation System Comparison

A comprehensive AI-powered Recommendation System that compares multiple recommendation algorithms using Amazon Product Reviews. This project demonstrates how different recommendation techniques perform on the same dataset through an interactive Streamlit dashboard.

---

## 📌 Project Overview

Recommendation systems are widely used in e-commerce platforms like Amazon, Netflix, Spotify, and YouTube.

This project implements and compares several recommendation algorithms, allowing users to explore the strengths of each method.

---

## 🚀 Features

- ⭐ Popularity-Based Recommendation
- 📄 Content-Based Recommendation
- 👥 User-Based Collaborative Filtering
- 🤖 SVD (Matrix Factorization)
- 🔍 KNN Item-Based Recommendation
- 🔀 Hybrid Recommendation System
- 📊 Algorithm Performance Comparison
- 🌐 Interactive Streamlit Dashboard

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Scikit-Surprise
- Streamlit
- Plotly
- Matplotlib

---

## 📂 Project Structure

```
Multi-Algorithm-Recommendation-System/
│
├── data/
│   ├── amazon.csv
│   ├── clean_amazon.csv
│
├── notebooks/
│   └── eda.py
│
├── models/
│   ├── popularity.py
│   ├── content_based.py
│   ├── collaborative.py
│   ├── svd_model.py
│   ├── knn_model.py
│   ├── hybrid.py
│   └── __init__.py
│
├── evaluation/
│   ├── metrics.py
│   └── results.csv
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📊 Dataset

**Dataset:** Amazon Product Reviews Dataset

The dataset contains:

- Product ID
- Product Name
- Brand
- Category
- User Name
- Ratings
- Review Text

This dataset is used to build and compare multiple recommendation algorithms.

---

## 🤖 Recommendation Algorithms

### ⭐ 1. Popularity-Based Recommendation

Recommends products based on:

- Highest Average Rating
- Number of Reviews

---

### 📄 2. Content-Based Filtering

Uses:

- Product Name
- Brand
- Category

Algorithms:

- TF-IDF Vectorizer
- Cosine Similarity

---

### 👥 3. User-Based Collaborative Filtering

Recommends products liked by users with similar preferences.

---

### 🤖 4. SVD Recommendation

Matrix Factorization technique that predicts ratings based on latent user-item interactions.

---

### 🔍 5. Item-Based KNN

Finds similar products based on user rating patterns.

---

### 🔀 6. Hybrid Recommendation

Combines:

- Popularity-Based
- Content-Based
- Collaborative Filtering
- SVD
- KNN

to improve recommendation quality.

---

## 📈 Evaluation Metrics

The recommendation algorithms are evaluated using:

- RMSE
- MAE
- Execution Time

Results are stored in:

```
evaluation/results.csv
```

---

## 💻 Streamlit Dashboard

The dashboard provides:

- Product Recommendation
- User Recommendation
- Algorithm Selection
- Recommendation Comparison
- Dataset Overview

Run the application:

```bash
streamlit run app.py
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Multi-Algorithm-Recommendation-System.git
```

Move into the project folder:

```bash
cd Multi-Algorithm-Recommendation-System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 📊 Future Improvements

- Deep Learning Recommendation Model
- Neural Collaborative Filtering
- Product Images
- Explainable Recommendations
- Personalized User Dashboard
- Real-time Recommendation API
- Recommendation Diversity Metrics
- Precision@K & Recall@K Evaluation

---

## 🎯 Learning Outcomes

This project demonstrates:

- Data Cleaning & Preprocessing
- Recommendation Systems
- Machine Learning
- Collaborative Filtering
- Matrix Factorization
- Content-Based Filtering
- Streamlit Dashboard Development
- Model Evaluation
- Python Project Structuring

---

## 📷 Dashboard Preview

> Add screenshots of your Streamlit dashboard here after deployment.

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Shaik Aiesha**

- GitHub: https://github.com/Aiesha22
- LinkedIn: *(Add your LinkedIn profile here)*

---

⭐ If you found this project helpful, consider giving it a star!