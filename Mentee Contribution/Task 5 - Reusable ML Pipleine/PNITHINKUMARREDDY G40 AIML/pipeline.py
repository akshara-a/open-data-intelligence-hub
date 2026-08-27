import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# 1. Load the Original Dataset (Directly from the root directory)
df = pd.read_csv('churn.csv') 

# Clean 'TotalCharges' column by replacing blank spaces with NaN and converting to numeric
df['TotalCharges'] = df['TotalCharges'].replace(" ", np.nan)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])

# Map target variable 'Churn' from text (Yes/No) to binary integers (1/0)
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Separate features (X) and target variable (y)
# Dropping 'customerID' as it is just a unique identifier and holds no predictive value
X = df.drop(columns=['customerID', 'Churn']) 
y = df['Churn']

# 2. Automatically Identify Column Types
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

# 3. Define Preprocessing Pipelines for Numeric and Categorical Features
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), # Handles missing numerical values using median
    ('scaler', StandardScaler())                  # Scales features to have mean=0 and variance=1
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), # Handles missing categorical values using mode
    ('onehot', OneHotEncoder(handle_unknown='ignore'))     # Encodes categorical text into binary dummy vectors
])

# 4. Combine Preprocessors into a single ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ]
)

# 5. Assemble the End-to-End Production Pipeline (Preprocessing + Classifier)
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42))
])

# 6. Perform Train-Test Split (80% Training, 20% Testing)
# Using stratify=y to maintain the original class distribution across splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 7. Train the Complete Pipeline
print("🤖 Training the production ML pipeline...")
full_pipeline.fit(X_train, y_train)

# 8. Evaluate Model Performance on Test Data
y_pred = full_pipeline.predict(X_test)
y_pred_proba = full_pipeline.predict_proba(X_test)[:, 1]

print("\n=== PRODUCTION PIPELINE CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}\n")