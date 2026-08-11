from src.data_preprocessing import preprocess_data
from src.elbow_method import plot_elbow
from src.clustering import perform_clustering
from src.regression import run_regression
from src.classification import run_classification

# ==========================================
# Load and Preprocess Data
# ==========================================
print("\nLoading dataset and preprocessing...")

df, scaled_data = preprocess_data("data/customer_data.csv")

# ==========================================
# Elbow Method
# ==========================================
print("\nGenerating Elbow Method graph...")
plot_elbow(scaled_data)

# ==========================================
# K-Means Clustering
# ==========================================
print("\nPerforming K-Means Clustering...")

clusters = perform_clustering(scaled_data)

# Add cluster labels
df["Cluster"] = clusters

# ==========================================
# Display Results
# ==========================================
print("\nFirst 5 Rows with Cluster Labels:")
print(df.head())

print("\nCluster Distribution:")
print(df["Cluster"].value_counts().sort_index())

# ==========================================
# Save Clustered Dataset
# ==========================================
df.to_csv("outputs/customer_segments.csv", index=False)

print("\nCustomer segments saved successfully!")

# ==========================================
# Regression
# ==========================================
print("\nRunning Regression Models...")
run_regression(df)

# ==========================================
# Classification
# ==========================================
print("\nRunning Classification Model...")
run_classification(df)

# ==========================================
# Finished
# ==========================================
print("\n=========================================")
print("Task 8 Completed Successfully!")
print("Generated Files:")
print("1. outputs/customer_segments.csv")
print("2. outputs/charts/elbow_method.png")
print("3. outputs/charts/regression_prediction.png")
print("4. outputs/charts/confusion_matrix.png")
print("=========================================")