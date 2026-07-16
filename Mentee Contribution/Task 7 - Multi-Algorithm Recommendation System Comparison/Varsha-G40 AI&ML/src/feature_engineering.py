# ==========================================================
# STEP 4 : FEATURE ENGINEERING
# ==========================================================

import os
import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

print("="*60)
print("FEATURE ENGINEERING")
print("="*60)

# ----------------------------------------------------------
# Create models folder
# ----------------------------------------------------------

os.makedirs("models", exist_ok=True)

# ----------------------------------------------------------
# Load Cleaned Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/cleaned_ecommerce.csv")

print("\nDataset Loaded Successfully")
print("\nDataset Shape:", df.shape)

# ----------------------------------------------------------
# Remove unnecessary columns
# ----------------------------------------------------------

drop_columns = [
    "session_id",
    "visit_date",
    "review_text",
    "review_helpful_votes"
]

for col in drop_columns:
    if col in df.columns:
        df.drop(columns=col, inplace=True)

print("\nColumns after dropping unnecessary columns:")
print(df.columns.tolist())

# ==========================================================
# Encode Categorical Columns
# ==========================================================

categorical_columns = [

    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "payment_method",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "session_duration_bucket",
    "location"

]

label_encoders = {}

print("\nEncoding categorical columns...")

for col in categorical_columns:

    if col in df.columns:

        le = LabelEncoder()

        df[col] = le.fit_transform(df[col].astype(str))

        label_encoders[col] = le

        print(col, "Encoded")

# ----------------------------------------------------------
# Save Label Encoders
# ----------------------------------------------------------

joblib.dump(label_encoders, "models/label_encoders.pkl")

print("\nLabel Encoders Saved")

# ==========================================================
# Scale Numerical Columns
# ==========================================================

numerical_columns = [

    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "revenue",
    "pages_viewed",
    "time_on_site_sec"

]

print("\nScaling numerical columns...")

scaler = StandardScaler()

df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

joblib.dump(scaler, "models/scaler.pkl")

print("Scaler Saved")

# ==========================================================
# Save Processed Dataset
# ==========================================================

df.to_csv(
    "data/processed_ecommerce.csv",
    index=False
)

print("\nProcessed Dataset Saved")
print("Location : data/processed_ecommerce.csv")

print("\nFinal Shape :", df.shape)

print("\nSTEP 4 COMPLETED SUCCESSFULLY")