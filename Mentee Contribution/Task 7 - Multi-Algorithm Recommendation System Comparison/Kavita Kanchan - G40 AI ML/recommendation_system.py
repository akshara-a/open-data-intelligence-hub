import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix,
    silhouette_score
)
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.cluster import KMeans

# Set seed for reproducible results
np.random.seed(42)

# ==========================================
# STEP 1: Generate Synthetic E-Commerce Dataset
# ==========================================
print("Generating synthetic e-commerce dataset...")

n_samples = 1000

user_ids = [f"USR_{i:04d}" for i in range(1, n_samples + 1)]
product_ids = [f"PRD_{np.random.randint(100, 300)}" for _ in range(n_samples)]
categories = np.random.choice(["Electronics", "Fashion", "Home & Kitchen", "Books"], size=n_samples)
views = np.random.randint(1, 30, size=n_samples)
time_spent = np.round(np.random.exponential(scale=120, size=n_samples) + 10, 2)  # in seconds
cart_status = np.random.choice([0, 1], size=n_samples, p=[0.6, 0.4])
previous_purchases = np.random.poisson(lam=3, size=n_samples)
price = np.round(np.random.uniform(10, 500, size=n_samples), 2)

# Rating generation logic: Higher time spent and views slightly boost rating
rating_noise = np.random.normal(0, 0.4, size=n_samples)
rating = np.clip(
    np.round(3.0 + (0.002 * time_spent) + (0.04 * views) - (0.001 * price) + rating_noise, 1),
    1.0, 5.0
)

# Purchase likelihood logic: Adding to cart and high dwell time increase probability
logit = -2.0 + (2.5 * cart_status) + (0.008 * time_spent) + (0.4 * rating) - (0.002 * price)
purchase_prob = 1 / (1 + np.exp(-logit))
purchase_status = np.random.binomial(1, purchase_prob)

df = pd.DataFrame({
    'User ID': user_ids,
    'Product ID': product_ids,
    'Product Category': categories,
    'Price': price,
    'Number of Views': views,
    'Time Spent': time_spent,
    'Cart Status': cart_status,
    'Previous Purchases': previous_purchases,
    'Rating': rating,
    'Purchase Status': purchase_status
})

print("\n--- Dataset Preview ---")
print(df.head())
print(f"Dataset shape: {df.shape}")

# ==========================================
# STEP 2: Preprocessing Setup
# ==========================================
num_features = ['Price', 'Number of Views', 'Time Spent', 'Previous Purchases']
cat_features = ['Product Category']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_features)
    ]
)

# ==========================================
# STEP 3: Regression (Predict Product Rating)
# ==========================================
print("\n==========================================")
print(" 1. RIDGE REGRESSION - Rating Prediction")
print("==========================================")

reg_features = ['Price', 'Number of Views', 'Time Spent', 'Previous Purchases', 'Cart Status', 'Product Category']
X_reg = df[reg_features]
y_reg = df['Rating']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

reg_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', Ridge())
])

param_grid_reg = {'regressor__alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
grid_reg = GridSearchCV(reg_pipeline, param_grid_reg, cv=5, scoring='neg_root_mean_squared_error')
grid_reg.fit(X_train_r, y_train_r)

best_reg = grid_reg.best_estimator_
y_pred_r = best_reg.predict(X_test_r)

mae_r = mean_absolute_error(y_test_r, y_pred_r)
rmse_r = np.sqrt(mean_squared_error(y_test_r, y_pred_r))
r2_r = r2_score(y_test_r, y_pred_r)

print(f"Best Alpha Parameter: {grid_reg.best_params_['regressor__alpha']}")
print(f"MAE:  {mae_r:.4f}")
print(f"RMSE: {rmse_r:.4f}")
print(f"R²:   {r2_r:.4f}")

# ==========================================
# STEP 4: Classification (Predict Purchase Likelihood)
# ==========================================
print("\n==========================================")
print(" 2. LOGISTIC REGRESSION - Purchase Prediction")
print("==========================================")

clf_features = ['Price', 'Number of Views', 'Time Spent', 'Previous Purchases', 'Cart Status', 'Rating', 'Product Category']
X_clf = df[clf_features]
y_clf = df['Purchase Status']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

clf_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

param_grid_clf = {
    'classifier__C': [0.01, 0.1, 1.0, 10.0],
    'classifier__solver': ['liblinear', 'lbfgs'],
    'classifier__max_iter': [200]
}

grid_clf = GridSearchCV(clf_pipeline, param_grid_clf, cv=5, scoring='f1')
grid_clf.fit(X_train_c, y_train_c)

best_clf = grid_clf.best_estimator_
y_pred_c = best_clf.predict(X_test_c)

acc_c = accuracy_score(y_test_c, y_pred_c)
prec_c = precision_score(y_test_c, y_pred_c)
rec_c = recall_score(y_test_c, y_pred_c)
f1_c = f1_score(y_test_c, y_pred_c)
cm_c = confusion_matrix(y_test_c, y_pred_c)

print(f"Best Hyperparameters: {grid_clf.best_params_}")
print(f"Accuracy:  {acc_c:.4f}")
print(f"Precision: {prec_c:.4f}")
print(f"Recall:    {rec_c:.4f}")
print(f"F1 Score:  {f1_c:.4f}")

# ==========================================
# STEP 5: Clustering (Customer Segmentation)
# ==========================================
print("\n==========================================")
print(" 3. K-MEANS - Customer Segmentation")
print("==========================================")

# Aggregate data by User to build user profiles
customer_df = df.groupby('User ID').agg({
    'Number of Views': 'sum',
    'Previous Purchases': 'max',
    'Rating': 'mean',
    'Time Spent': 'mean',
    'Price': 'sum',
    'Cart Status': 'sum'
}).rename(columns={'Price': 'Total Spent', 'Rating': 'Avg Rating', 'Time Spent': 'Avg Time Spent'})

scaler = StandardScaler()
X_cluster = scaler.fit_transform(customer_df)

k_range = range(2, 7)
inertias = []
silhouette_scores = []

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_cluster)
    inertias.append(km.inertia_)
    silhouette_scores.append(silhouette_score(X_cluster, km.labels_))

best_k = k_range[np.argmax(silhouette_scores)]
final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
customer_df['Cluster'] = final_kmeans.fit_predict(X_cluster)

print(f"Optimal Cluster Count (K): {best_k}")
print(f"Best Silhouette Score:    {max(silhouette_scores):.4f}")
print("\nCluster Center Summaries (Unscaled Averages):")
print(customer_df.groupby('Cluster').mean().round(2))

# ==========================================
# STEP 6: Consolidated Business Summary Table
# ==========================================
print("\n==========================================")
print(" FINAL MODEL COMPARISON & BUSINESS SUMMARY")
print("==========================================")

summary_data = [
    {
        "ML Task": "Regression",
        "Algorithm": "Ridge Regression",
        "Target Goal": "Predict Product Rating",
        "Metrics Used": "MAE, RMSE, R²",
        "Best Performance": f"R²: {r2_r:.2f}, RMSE: {rmse_r:.2f}",
        "Business Utility": "Surface items predicted to receive high ratings"
    },
    {
        "ML Task": "Classification",
        "Algorithm": "Logistic Regression",
        "Target Goal": "Predict Purchase Likelihood",
        "Metrics Used": "Accuracy, F1 Score",
        "Best Performance": f"Acc: {acc_c:.2f}, F1: {f1_c:.2f}",
        "Business Utility": "Trigger personalized popups & deals to high-intent buyers"
    },
    {
        "ML Task": "Clustering",
        "Algorithm": "K-Means",
        "Target Goal": "Segment Customers",
        "Metrics Used": "Silhouette Score",
        "Best Performance": f"K={best_k}, Sil: {max(silhouette_scores):.2f}",
        "Business Utility": "Tailor marketing strategy according to user spending tiers"
    }
]

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))
# ==========================================
# STEP 7: Save Visualizations to File
# ==========================================
print("\nGenerating visual plots for GitHub & Report...")

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Classification: Confusion Matrix Heatmap
sns.heatmap(cm_c, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['Not Purchased', 'Purchased'], 
            yticklabels=['Not Purchased', 'Purchased'])
axes[0].set_title('Classification: Confusion Matrix', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Predicted Label')
axes[0].set_ylabel('True Label')

# 2. Clustering: Elbow Method Curve
axes[1].plot(k_range, inertias, marker='o', color='purple', linewidth=2)
axes[1].set_title('Clustering: Elbow Method (K-Means)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Number of Clusters (K)')
axes[1].set_ylabel('Inertia')

# 3. Regression: Actual vs Predicted Ratings Scatter Plot
axes[2].scatter(y_test_r, y_pred_r, alpha=0.5, color='teal')
axes[2].plot([y_test_r.min(), y_test_r.max()], [y_test_r.min(), y_test_r.max()], 'r--', lw=2)
axes[2].set_title('Regression: Actual vs Predicted Ratings', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Actual Rating')
axes[2].set_ylabel('Predicted Rating')

plt.tight_layout()
plt.savefig('project_visualizations.png', dpi=300)
print("Graph saved as 'project_visualizations.png'!")