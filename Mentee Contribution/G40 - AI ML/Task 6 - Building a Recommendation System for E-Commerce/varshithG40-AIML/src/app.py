import os
import sys
import pandas as pd
import numpy as np
import pickle
from flask import Flask, render_template, request, jsonify

# Add src to system path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_preprocessing import preprocess_all
from regression_model import train_ridge_regression, train_linear_regression
from classification_model import train_logistic_regression
from clustering_model import train_kmeans, profile_clusters

app = Flask(__name__, static_folder='static', template_folder='templates')

# Global variables for models and scalers
MODELS = {}
DATA = {}

def init_models():
    global MODELS, DATA
    # Re-run or load preprocessing
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, "data", "ecommerce_data.csv")
    
    if not os.path.exists(data_path):
        from data_generation import generate_ecommerce_data
        generate_ecommerce_data(n_records=5000, output_dir=os.path.join(project_root, "data"))
        
    DATA = preprocess_all(data_path)
    
    # Train and cache models for interactive predictions
    # Regression (Ridge)
    reg_data = DATA["regression"]
    reg_model, _, _ = train_ridge_regression(
        reg_data["X_train_scaled"], reg_data["y_train"],
        reg_data["X_test_scaled"], reg_data["y_test"],
        alpha=50.0 # From tuned results
    )
    MODELS["regression"] = reg_model
    MODELS["regression_scaler"] = reg_data["scaler"]
    MODELS["regression_features"] = reg_data["feature_names"]
    
    # Classification (Logistic Regression)
    clf_data = DATA["classification"]
    clf_model, _, _, _ = train_logistic_regression(
        clf_data["X_train_scaled"], clf_data["y_train"],
        clf_data["X_test_scaled"], clf_data["y_test"],
        C=1.0, penalty="l1", solver="saga" # From tuned results
    )
    MODELS["classification"] = clf_model
    MODELS["classification_scaler"] = clf_data["scaler"]
    MODELS["classification_features"] = clf_data["feature_names"]
    
    # Clustering (K-Means)
    clust_data = DATA["clustering"]
    clust_model, labels, metrics = train_kmeans(clust_data["X_scaled"], n_clusters=4)
    MODELS["clustering"] = clust_model
    MODELS["clustering_scaler"] = clust_data["scaler"]
    MODELS["clustering_features"] = clust_data["feature_names"]
    MODELS["clustering_labels"] = labels
    MODELS["clustering_profiles"] = profile_clusters(clust_data["customer_df"], labels, clust_data["feature_names"])

@app.route('/')
def index():
    # Render main dashboard page
    # Calculate some summary stats
    df = DATA["df"]
    stats = {
        "num_records": len(df),
        "avg_rating": round(df["Rating"].mean(), 2),
        "purchase_rate": f"{df['Purchase_Status'].mean() * 100:.1f}%",
        "avg_spending": f"${df['Total_Spending'].mean():.2f}",
        "unique_users": df["User_ID"].nunique(),
        "unique_products": df["Product_ID"].nunique()
    }
    
    # Send cluster profiles as list of dicts
    profiles = MODELS["clustering_profiles"].reset_index().to_dict(orient="records")
    
    # Map cluster numbers to business segment names
    segment_names = {
        0: "Discount-Sensitive Customers",
        1: "Active Browsers (Low Purchase)",
        2: "Casual/Low-Engagement Shoppers",
        3: "Premium High-Value Customers"
    }
    for p in profiles:
        p["Segment_Name"] = segment_names.get(p["Cluster"], f"Cluster {p['Cluster']}")
        
    return render_template('index.html', stats=stats, profiles=profiles)

@app.route('/api/predict/rating', methods=['POST'])
def predict_rating():
    try:
        data = request.json
        # Feature columns: Price, Browsing_Time, Previous_Purchases, Discount_Applied, Age, Category_Encoded, Total_Spending
        category = data.get("Category", "Electronics")
        le = DATA["encoders"]["Category"]
        try:
            category_encoded = le.transform([category])[0]
        except Exception:
            category_encoded = 0
            
        features = [
            float(data.get("Price", 50)),
            float(data.get("Browsing_Time", 10)),
            float(data.get("Previous_Purchases", 5)),
            float(data.get("Discount_Applied", 0)),
            float(data.get("Age", 30)),
            float(category_encoded),
            float(data.get("Total_Spending", 200))
        ]
        
        # Scale
        scaler = MODELS["regression_scaler"]
        features_scaled = scaler.transform([features])
        
        # Predict
        pred_rating = MODELS["regression"].predict(features_scaled)[0]
        pred_rating = min(5.0, max(1.0, round(pred_rating, 2)))
        
        return jsonify({"success": True, "predicted_rating": pred_rating})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/predict/purchase', methods=['POST'])
def predict_purchase():
    try:
        data = request.json
        # Feature columns: Browsing_Time, Cart_Addition, Previous_Purchases, Rating, Price, Discount_Applied, Total_Spending
        features = [
            float(data.get("Browsing_Time", 10)),
            float(data.get("Cart_Addition", 0)),
            float(data.get("Previous_Purchases", 5)),
            float(data.get("Rating", 4)),
            float(data.get("Price", 50)),
            float(data.get("Discount_Applied", 0)),
            float(data.get("Total_Spending", 200))
        ]
        
        # Scale
        scaler = MODELS["classification_scaler"]
        features_scaled = scaler.transform([features])
        
        # Predict
        prob = MODELS["classification"].predict_proba(features_scaled)[0][1]
        pred = int(MODELS["classification"].predict(features_scaled)[0])
        
        return jsonify({
            "success": True,
            "purchase_probability": round(prob * 100, 1),
            "purchase_likelihood": "Yes" if pred == 1 else "No"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    init_models()
    # Create static assets directory structure and copy existing plots inside it
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_plots_dir = os.path.join(project_root, "src", "static", "plots")
    os.makedirs(static_plots_dir, exist_ok=True)
    
    # Copy plots from outputs/plots to static/plots
    src_plots_dir = os.path.join(project_root, "outputs", "plots")
    if os.path.exists(src_plots_dir):
        import shutil
        for f in os.listdir(src_plots_dir):
            shutil.copy(os.path.join(src_plots_dir, f), os.path.join(static_plots_dir, f))
            
    print("Dashboard server starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
