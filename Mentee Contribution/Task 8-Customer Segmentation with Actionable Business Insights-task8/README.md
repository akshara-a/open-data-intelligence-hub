# 🛍️ Customer Segmentation with Actionable Business Insights

## 📌 Project Overview

Customer segmentation is one of the most effective techniques used by businesses to understand customer behavior and create personalized marketing strategies.

This project applies **K-Means Clustering**, an unsupervised machine learning algorithm, to segment mall customers based on their demographic and spending characteristics. The identified customer groups are analyzed to generate actionable business insights that can help improve customer engagement, retention, and revenue.

---

## 🎯 Objectives

* Analyze customer purchasing behavior.
* Segment customers into meaningful groups.
* Visualize customer clusters.
* Generate actionable marketing strategies for each customer segment.
* Build an interactive Streamlit dashboard for business users.

---

## 📂 Project Structure

```
Customer-Segmentation-with-Actionable-Business-Insights/
│
├── data/
│   ├── Mall_Customers.csv
│   ├── clean_customers.csv
│   └── scaled_customers.csv
│
├── notebooks/
│   └── eda.py
│
├── models/
│   ├── preprocessing.py
│   ├── elbow_method.py
│   ├── clustering.py
│   └── business_insights.py
│
├── outputs/
│   ├── clustered_customers.csv
│   ├── age_distribution.png
│   ├── gender_distribution.png
│   ├── income_distribution.png
│   ├── spending_distribution.png
│   └── correlation_heatmap.png
│
├── images/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📊 Dataset

**Dataset:** Mall Customer Segmentation Dataset

The dataset contains customer information such as:

* Customer ID
* Gender
* Age
* Annual Income (k$)
* Spending Score (1–100)

These features are used to identify different customer groups using clustering techniques.

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* Scikit-learn
* Streamlit

---

## ⚙️ Machine Learning Workflow

1. Data Loading
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Selection
5. Feature Scaling using StandardScaler
6. Elbow Method for optimal K selection
7. K-Means Clustering
8. Cluster Visualization
9. Business Insight Generation
10. Interactive Dashboard

---

## 📈 Exploratory Data Analysis

The project includes visualizations such as:

* Age Distribution
* Gender Distribution
* Annual Income Distribution
* Spending Score Distribution
* Correlation Heatmap

---

## 🤖 Machine Learning Model

### Algorithm Used

**K-Means Clustering**

Why K-Means?

* Fast and efficient
* Easy to interpret
* Ideal for customer segmentation
* Widely used in business analytics

---

## 💡 Customer Segments & Business Strategies

### ⭐ VIP Customers

Characteristics:

* High Income
* High Spending

Business Strategy:

* Premium Membership
* Loyalty Rewards
* Exclusive Product Launches
* Personalized Services

---

### 💰 High Income – Low Spending

Business Strategy:

* Personalized Discounts
* Premium Product Recommendations
* Upselling Campaigns
* Email Marketing

---

### 🛍️ High Spending – Moderate Income

Business Strategy:

* Cashback Offers
* Bundle Deals
* Referral Programs
* Seasonal Promotions

---

### 📦 Budget Customers

Business Strategy:

* Coupons
* Flash Sales
* Student Discounts
* Festival Offers

---

## 📊 Dashboard Features

The Streamlit dashboard includes:

* 🏠 Home Page
* 📊 Dataset Overview
* 📈 Interactive EDA Charts
* 🤖 Customer Segmentation Visualization
* 💡 Business Insights
* 📥 Download Clustered Dataset

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/Customer-Segmentation-with-Actionable-Business-Insights.git
```

### Navigate to the Project Folder

```bash
cd Customer-Segmentation-with-Actionable-Business-Insights
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📷 Project Screenshots

Add screenshots of:

* Dashboard Home
* Customer Segments
* Business Insights
* EDA Visualizations

inside the **images** folder and include them here after deployment.

---

## 📈 Future Enhancements

* DBSCAN Clustering
* Hierarchical Clustering
* PCA for dimensionality reduction
* Customer Lifetime Value (CLV) Analysis
* RFM Analysis
* Predictive Customer Segmentation
* AI-powered marketing recommendations
* Dashboard filtering and search options

---

## 🎓 Learning Outcomes

Through this project, you will learn:

* Data Cleaning & Preprocessing
* Exploratory Data Analysis
* Feature Engineering
* Feature Scaling
* K-Means Clustering
* Customer Analytics
* Business Intelligence
* Data Visualization
* Streamlit Dashboard Development

---

## 🤝 Contributing

Contributions are welcome.

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

* GitHub: https://github.com/Aiesha22
* LinkedIn: *(Add your LinkedIn profile here)*

---

⭐ If you found this project helpful, please consider giving it a **Star** on GitHub!
