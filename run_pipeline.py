import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

# Setup directories
os.makedirs('images', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Load dataset
df = pd.read_csv('data/ecommerce_dataset.csv')

# --- STEP 1: EXPLORATORY DATA ANALYSIS (EDA) ---
print("Running Exploratory Data Analysis...")

# Plot 1: Most purchased product categories
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Category', hue='Purchase_Status', palette='viridis')
plt.title('Purchase Status by Product Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/eda_category_distribution.png')
plt.close()

# Plot 2: Relationship between browsing time and purchase
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Purchase_Status', y='Browsing_Time', palette='coolwarm')
plt.title('Browsing Time vs Purchase Status')
plt.xlabel('Purchase Status (0 = No, 1 = Yes)')
plt.ylabel('Browsing Time (minutes)')
plt.tight_layout()
plt.savefig('images/eda_browsing_vs_purchase.png')
plt.close()

# Plot 3: Distribution of Customer Spending
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='Total_Spending', kde=True, color='purple')
plt.title('Distribution of Customer Total Spending')
plt.tight_layout()
plt.savefig('images/eda_total_spending_distribution.png')
plt.close()


# --- STEP 2: REGRESSION (RATING PREDICTION) ---
print("\n--- Running Part A: Regression (Rating Prediction) ---")
X_reg = df[['Price', 'Browsing_Time', 'Previous_Purchases', 'Discount_Applied', 'Age', 'Total_Spending', 'Category']]
y_reg = df['Rating']

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

# Column Transformer for Preprocessing
categorical_cols = ['Category']
numeric_cols = ['Price', 'Browsing_Time', 'Previous_Purchases', 'Discount_Applied', 'Age', 'Total_Spending']

preprocessor_reg = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]
)

# Linear Regression Baseline
lr_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor_reg),
    ('regressor', LinearRegression())
])
lr_pipeline.fit(X_train_reg, y_train_reg)
y_pred_lr = lr_pipeline.predict(X_test_reg)

lr_mae = mean_absolute_error(y_test_reg, y_pred_lr)
lr_mse = mean_squared_error(y_test_reg, y_pred_lr)
lr_rmse = np.sqrt(lr_mse)
lr_r2 = r2_score(y_test_reg, y_pred_lr)

print("Linear Regression Baseline Metrics:")
print(f"  MAE: {lr_mae:.4f}, MSE: {lr_mse:.4f}, RMSE: {lr_rmse:.4f}, R²: {lr_r2:.4f}")

# Ridge Regression with Grid Search Tuning
ridge_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor_reg),
    ('regressor', Ridge())
])

param_grid_ridge = {
    'regressor__alpha': [0.01, 0.1, 1.0, 10.0, 100.0]
}

grid_ridge = GridSearchCV(ridge_pipeline, param_grid_ridge, cv=3, scoring='neg_mean_squared_error')
grid_ridge.fit(X_train_reg, y_train_reg)

best_ridge = grid_ridge.best_estimator_
y_pred_ridge = best_ridge.predict(X_test_reg)

ridge_mae = mean_absolute_error(y_test_reg, y_pred_ridge)
ridge_mse = mean_squared_error(y_test_reg, y_pred_ridge)
ridge_rmse = np.sqrt(ridge_mse)
ridge_r2 = r2_score(y_test_reg, y_pred_ridge)

print(f"Best Ridge Alpha: {grid_ridge.best_params_['regressor__alpha']}")
print("Ridge Regression Metrics:")
print(f"  MAE: {ridge_mae:.4f}, MSE: {ridge_mse:.4f}, RMSE: {ridge_rmse:.4f}, R²: {ridge_r2:.4f}")

# Save the best regression model (Ridge)
with open('models/regression_model.pkl', 'wb') as f:
    pickle.dump(best_ridge, f)


# --- STEP 3: CLASSIFICATION (PURCHASE STATUS PREDICTION) ---
print("\n--- Running Part B: Classification (Purchase Likelihood Prediction) ---")
X_cls = df[['Browsing_Time', 'Cart_Addition', 'Previous_Purchases', 'Rating', 'Price', 'Discount_Applied', 'Total_Spending']]
y_cls = df['Purchase_Status']

X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(
    X_cls, y_cls, test_size=0.2, random_state=42
)

# Preprocessing: Scale features except binary ones
numeric_cols_cls = ['Browsing_Time', 'Previous_Purchases', 'Rating', 'Price', 'Total_Spending']
preprocessor_cls = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols_cls)
    ],
    remainder='passthrough'  # Keep Cart_Addition and Discount_Applied as is
)

# Logistic Regression with GridSearchCV
lr_cls_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor_cls),
    ('classifier', LogisticRegression(random_state=42))
])

param_grid_cls = {
    'classifier__C': [0.01, 0.1, 1.0, 10.0, 100.0],
    'classifier__penalty': ['l2'],
    'classifier__solver': ['lbfgs', 'liblinear'],
    'classifier__max_iter': [100, 200, 500]
}

grid_cls = GridSearchCV(lr_cls_pipeline, param_grid_cls, cv=3, scoring='accuracy')
grid_cls.fit(X_train_cls, y_train_cls)

best_cls = grid_cls.best_estimator_
y_pred_cls = best_cls.predict(X_test_cls)
y_prob_cls = best_cls.predict_proba(X_test_cls)[:, 1]

# Classification Metrics
cls_accuracy = accuracy_score(y_test_cls, y_pred_cls)
cls_precision = precision_score(y_test_cls, y_pred_cls, zero_division=0)
cls_recall = recall_score(y_test_cls, y_pred_cls, zero_division=0)
cls_f1 = f1_score(y_test_cls, y_pred_cls, zero_division=0)
try:
    cls_roc_auc = roc_auc_score(y_test_cls, y_prob_cls)
except Exception:
    cls_roc_auc = float('nan')

print(f"Best Classification Params: {grid_cls.best_params_}")
print("Logistic Regression Metrics:")
print(f"  Accuracy: {cls_accuracy:.4f}, Precision: {cls_precision:.4f}, Recall: {cls_recall:.4f}, F1-Score: {cls_f1:.4f}, ROC-AUC: {cls_roc_auc}")

# Save ROC Curve
if not np.isnan(cls_roc_auc) and len(set(y_test_cls)) > 1:
    fpr, tpr, _ = roc_curve(y_test_cls, y_prob_cls)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='blue', label=f'Logistic Regression (AUC = {cls_roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='red', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('images/roc_curve.png')
    plt.close()
else:
    # Handle single-class in test set gracefully for ROC curve
    print("Warning: Only one class present in y_test_cls. ROC Curve not generated.")

# Save classification model
with open('models/classification_model.pkl', 'wb') as f:
    pickle.dump(best_cls, f)


# --- STEP 4: CLUSTERING (CUSTOMER SEGMENTATION) ---
print("\n--- Running Part C: Clustering (Customer Segmentation) ---")
# Customer level features: Browsing_Time, Previous_Purchases, Rating (Average Rating), Total_Spending, Cart_Addition (Cart_Addition_Count), Discount_Applied (Discount_Usage)
features_cluster = ['Browsing_Time', 'Previous_Purchases', 'Rating', 'Total_Spending', 'Cart_Addition', 'Discount_Applied']
X_clust = df[features_cluster].copy()

# Scale features
scaler_clust = StandardScaler()
X_clust_scaled = scaler_clust.fit_transform(X_clust)

# Elbow Method to find K
inertia = []
k_range = range(2, 8)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_clust_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(k_range, inertia, marker='o', linestyle='-', color='teal')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (SSE)')
plt.title('Elbow Method for Optimal K')
plt.tight_layout()
plt.savefig('images/elbow_method.png')
plt.close()

# We tune n_clusters, init, max_iter using custom search or silhouette analysis
best_k = 4 # Default standard segment count specified in business use case
best_silhouette = -1
best_kmeans = None
best_params = {}

for k in [2, 3, 4, 5]:
    for init in ['k-means++', 'random']:
        for max_iter in [100, 300, 500]:
            kmeans = KMeans(n_clusters=k, init=init, max_iter=max_iter, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_clust_scaled)
            score = silhouette_score(X_clust_scaled, labels)
            if score > best_silhouette:
                best_silhouette = score
                best_k = k
                best_kmeans = kmeans
                best_params = {'n_clusters': k, 'init': init, 'max_iter': max_iter}

print(f"Best Clustering Hyperparameters: {best_params}")
print(f"Best Silhouette Score: {best_silhouette:.4f}")

# Final Clustering Model Fit
final_kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, random_state=42, n_init=10)
cluster_labels = final_kmeans.fit_predict(X_clust_scaled)
final_silhouette = silhouette_score(X_clust_scaled, cluster_labels)
print(f"Silhouette Score with K=4: {final_silhouette:.4f}")
print(f"Inertia with K=4: {final_kmeans.inertia_:.4f}")

# Add Cluster Labels to DataFrame
df['Cluster'] = cluster_labels

# Save Clustering Model & Scaler (as a pipeline or tuple)
with open('models/clustering_model.pkl', 'wb') as f:
    pickle.dump((scaler_clust, final_kmeans), f)

# Silhouette Analysis Plot
fig, ax1 = plt.subplots(1, 1, figsize=(7, 5))
sample_silhouette_values = silhouette_samples(X_clust_scaled, cluster_labels)
y_lower = 10
for i in range(4):
    ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
    ith_cluster_silhouette_values.sort()
    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i
    color = plt.cm.nipy_spectral(float(i) / 4)
    ax1.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values, facecolor=color, edgecolor=color, alpha=0.7)
    ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    y_lower = y_upper + 10

ax1.set_title("Silhouette Plot for the Various Clusters")
ax1.set_xlabel("Silhouette Coefficient Values")
ax1.set_ylabel("Cluster Label")
ax1.axvline(x=final_silhouette, color="red", linestyle="--")
ax1.set_yticks([])
ax1.set_xlim([-0.1, 1])
plt.tight_layout()
plt.savefig('images/silhouette_analysis.png')
plt.close()

# Characterize Clusters
cluster_summary = df.groupby('Cluster')[features_cluster].mean()
print("\nCluster Characteristics (Feature Means):")
print(cluster_summary)

print("\nPipeline run complete. Models saved successfully and plots generated in 'images/'.")
