import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(filepath):
    """
    Load the e-commerce dataset using Pandas.
    """
    df = pd.read_csv(filepath)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def clean_data(df):
    """
    Clean the dataset by removing duplicate records and handling missing values.
    """
    # Check for duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    dropped_dupes = initial_rows - len(df)
    if dropped_dupes > 0:
        print(f"Dropped {dropped_dupes} duplicate records.")
    
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        print(f"Found {missing_count} missing values. Handling them...")
        # Fill numeric missing values with median, categorical with mode
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna(df[col].median())
    else:
        print("No missing values found.")
        
    return df

def preprocess_regression_data(df):
    """
    Prepare features and target for Ridge Regression.
    Target: Rating
    """
    df_clean = clean_data(df.copy())
    
    # Input features
    feature_cols = ['Price', 'Product_Category', 'Number_of_Views', 'Time_Spent', 'Previous_Purchases', 'Cart_Status']
    X = df_clean[feature_cols].copy()
    y = df_clean['Rating'].copy()
    
    # One-hot encode categorical features
    X = pd.get_dummies(X, columns=['Product_Category'], drop_first=True)
    
    # Split into 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale numerical features
    scaler = StandardScaler()
    num_cols = ['Price', 'Number_of_Views', 'Time_Spent', 'Previous_Purchases']
    
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])
    
    return X_train, X_test, y_train, y_test, scaler, X.columns.tolist()

def preprocess_classification_data(df):
    """
    Prepare features and target for Logistic Regression.
    Target: Purchase_Status
    """
    df_clean = clean_data(df.copy())
    
    # Input features
    feature_cols = ['Price', 'Product_Category', 'Number_of_Views', 'Cart_Status', 'Time_Spent', 'Previous_Purchases', 'Rating']
    X = df_clean[feature_cols].copy()
    y = df_clean['Purchase_Status'].copy()
    
    # One-hot encode categorical features
    X = pd.get_dummies(X, columns=['Product_Category'], drop_first=True)
    
    # Split into 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale numerical features
    scaler = StandardScaler()
    num_cols = ['Price', 'Number_of_Views', 'Time_Spent', 'Previous_Purchases', 'Rating']
    
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])
    
    return X_train, X_test, y_train, y_test, scaler, X.columns.tolist()

def preprocess_clustering_data(df):
    """
    Prepare customer behavior features for K-Means Clustering.
    Aggregate data by User_ID.
    """
    df_clean = clean_data(df.copy())
    
    # Create customer-level behavior metrics
    # Calculate Total Spend: Price * Purchase_Status
    df_clean['Spent_Amount'] = df_clean['Price'] * df_clean['Purchase_Status']
    
    customer_df = df_clean.groupby('User_ID').agg(
        Number_of_Products_Viewed=('Number_of_Views', 'sum'),
        Number_of_Purchases=('Purchase_Status', 'sum'),
        Average_Rating_Given=('Rating', 'mean'),
        Average_Time_Spent=('Time_Spent', 'mean'),
        Total_Amount_Spent=('Spent_Amount', 'sum'),
        Number_of_Products_Added_to_Cart=('Cart_Status', 'sum')
    ).reset_index()
    
    # Features for clustering
    features = [
        'Number_of_Products_Viewed',
        'Number_of_Purchases',
        'Average_Rating_Given',
        'Average_Time_Spent',
        'Total_Amount_Spent',
        'Number_of_Products_Added_to_Cart'
    ]
    
    X = customer_df[features].copy()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=features)
    
    return customer_df, X_scaled_df, scaler
