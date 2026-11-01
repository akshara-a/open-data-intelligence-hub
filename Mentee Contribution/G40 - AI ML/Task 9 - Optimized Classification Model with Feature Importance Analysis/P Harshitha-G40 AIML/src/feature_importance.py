import os
# pyrefly: ignore [missing-import]
import matplotlib
matplotlib.use('Agg')
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np

def extract_feature_importance(pipeline, output_path=None):
    preprocessor = pipeline.named_steps["preprocessor"]
    classifier = pipeline.named_steps["classifier"]
    
    cat_encoder = preprocessor.named_transformers_["categorical"].named_steps["encoder"]
    cat_features = preprocessor.transformers_[1][2]
    cat_encoded = cat_encoder.get_feature_names_out(cat_features)
    
    num_features = preprocessor.transformers_[0][2]
    all_feature_names = list(num_features) + list(cat_encoded)
    
    if hasattr(classifier, "feature_importances_"):
        importances = classifier.feature_importances_
        df_imp = pd.DataFrame({
            "Feature": all_feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False)
    elif hasattr(classifier, "coef_"):
        coefs = classifier.coef_[0]
        df_imp = pd.DataFrame({
            "Feature": all_feature_names,
            "Importance": np.abs(coefs),
            "Coefficient": coefs
        }).sort_values(by="Importance", ascending=False)
    else:
        raise ValueError("Classifier does not support feature importances or coefficients.")
        
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.figure(figsize=(10, 6))
        top_10 = df_imp.head(10).sort_values(by="Importance", ascending=True)
        plt.barh(top_10["Feature"], top_10["Importance"], color="#3498db")
        plt.title("Top 10 Influential Features for Purchase Prediction", fontsize=12, pad=15)
        plt.xlabel("Feature Importance Score")
        plt.ylabel("Feature")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close('all')

    return df_imp

def generate_feature_business_table(df_imp):
    top_10 = df_imp.head(10).copy()
    
    business_mappings = {
        "CartItems": ("Number of items added to shopping cart", "High intent signal. Send automated cart recovery emails and limited-time checkout discounts."),
        "PreviousPurchases": ("History of past purchases made by customer", "Strong repeat behavior. Enroll in customer loyalty/VIP program and personalized cross-selling."),
        "TimeOnSite": ("Total duration spent browsing website", "Deep interest signal. Engage with live chat popups or proactive product recommendations."),
        "DiscountUsed": ("Customer responsiveness to promotional offers", "Price-sensitive segment. Deliver targeted discount vouchers and flash sale notifications."),
        "PagesViewed": ("Total pages viewed during session", "High exploration level. Display top-rated items and simplified navigation to guide conversion."),
        "DaysSinceLastVisit": ("Recency of last site interaction", "Risk of churn. Launch re-engagement email drip campaigns with 'We miss you' incentives."),
        "EmailClicked": ("Promotional email click engagement", "High email responsiveness. Prioritize for high-value product launches and marketing blasts."),
        "ReviewScoreViewed": ("Average review score of products viewed", "Trust seeker. Display prominent social proof, verified customer reviews, and guarantees."),
        "DeviceType_Desktop": ("Session initiated on desktop computer", "Higher intent/conversion platform. Optimize desktop checkout flow and multi-item comparison tools."),
        "TrafficSource_Search Engine": ("Customer arrived via search engine", "Organic/intent search traffic. Provide direct landing pages and clear search result matches.")
    }

    interpretations = []
    actions = []
    
    for feat in top_10["Feature"]:
        match = None
        for key in business_mappings:
            if key in feat:
                match = business_mappings[key]
                break
        if match:
            interpretations.append(match[0])
            actions.append(match[1])
        else:
            interpretations.append("Customer demographic/behavioral feature influencing purchase decision.")
            actions.append("Optimize targeting and personalized user experience based on customer attributes.")

    top_10["Business Interpretation"] = interpretations
    top_10["Recommended Action"] = actions
    return top_10
