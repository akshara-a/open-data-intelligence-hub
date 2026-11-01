import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from data_loader import load_data
from preprocessing import preprocess_data
from feature_engineering import feature_engineering

# Load data
df = load_data("data/customer_churn.csv")

# Check original dataset
print("Columns in Dataset:")
print(df.columns)

print("\nFirst 5 Rows of Original Dataset:")
print(df.head())

# Preprocess
df = preprocess_data(df)

# Feature Engineering
df = feature_engineering(df)

# Remove customerID if present
if 'customerID' in df.columns:
    df = df.drop('customerID', axis=1)

# DO NOT convert everything to numeric using errors='coerce'
# Remove these lines if they exist:
# for col in df.columns:
#     df[col] = pd.to_numeric(df[col], errors='coerce')

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Print data types
print("\nData Types:")
print(df.dtypes)

# Print transformed dataset
print("\nFirst 5 Rows After Preprocessing:")
print(df.head())

# Separate features and target
X = df.drop('Churn', axis=1)
y = df['Churn']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000))
])

# Train model
pipeline.fit(X_train, y_train)

# Save model
joblib.dump(pipeline, "models/churn_model.pkl")

print("\nModel trained and saved successfully!")