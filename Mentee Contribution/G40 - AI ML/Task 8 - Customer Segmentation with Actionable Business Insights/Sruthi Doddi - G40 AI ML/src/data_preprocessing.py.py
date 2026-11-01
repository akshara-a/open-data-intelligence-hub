"""
Data Preprocessing Module
Handles data loading, cleaning, feature engineering, and scaling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')


class DataPreprocessor:
    """Class to handle all data preprocessing tasks"""
    
    def __init__(self, file_path):
        """
        Initialize with data file path
        
        Parameters:
        -----------
        file_path : str
            Path to the CSV file
        """
        self.file_path = file_path
        self.df = None
        self.df_clean = None
        self.df_encoded = None
        self.df_scaled = None
        self.label_encoders = {}
        self.scaler = None
        
    def load_data(self):
        """Load data from CSV file"""
        print("Loading data...")
        self.df = pd.read_csv(self.file_path)
        print(f"Loaded {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
        return self.df
    
    def check_data_quality(self):
        """Check for missing values, duplicates, and data types"""
        print("\n" + "="*50)
        print("DATA QUALITY CHECK")
        print("="*50)
        
        # Missing values
        missing = self.df.isnull().sum()
        print(f"Missing values: {missing.sum()}")
        
        # Duplicates
        print(f"Duplicate rows: {self.df.duplicated().sum()}")
        
        # Data types
        print(f"\nData types:\n{self.df.dtypes.value_counts()}")
        
        # Key statistics
        print("\nKey Statistics:")
        print(f"Total Revenue: ${self.df['revenue'].sum():,.2f}")
        print(f"Purchase Rate: {self.df['purchased'].mean()*100:.2f}%")
        print(f"Avg Rating: {self.df['rating'].mean():.2f}")
        print(f"Unique Customers: {self.df['customer_id'].nunique():,}")
        
        return self.df
    
    def feature_engineering(self):
        """Create new features from existing data"""
        print("\n" + "="*50)
        print("FEATURE ENGINEERING")
        print("="*50)
        
        # Copy data
        self.df_clean = self.df.copy()
        
        # Drop unnecessary columns
        drop_cols = ['session_id', 'visit_date', 'product_id', 'review_text', 
                     'review_helpful_votes', 'revenue_normalized']
        self.df_clean = self.df_clean.drop(columns=drop_cols)
        
        # Create new features
        self.df_clean['avg_spending_per_session'] = self.df_clean['revenue'] / self.df_clean.groupby('customer_id')['customer_id'].transform('count')
        self.df_clean['pages_per_minute'] = self.df_clean['pages_viewed'] / (self.df_clean['time_on_site_sec'] / 60 + 0.001)
        self.df_clean['discount_impact'] = self.df_clean['discount_percent'] * self.df_clean['unit_price'] / 100
        
        print("Created new features:")
        print(f"  avg_spending_per_session: {self.df_clean['avg_spending_per_session'].mean():.2f}")
        print(f"  pages_per_minute: {self.df_clean['pages_per_minute'].mean():.2f}")
        print(f"  discount_impact: {self.df_clean['discount_impact'].mean():.2f}")
        
        return self.df_clean
    
    def encode_categorical(self):
        """Encode categorical columns using LabelEncoder"""
        print("\nEncoding categorical columns...")
        
        cat_cols = ['device_type', 'user_type', 'marketing_channel', 'product_category', 
                    'payment_method', 'visit_season', 'session_duration_bucket']
        
        self.df_encoded = self.df_clean.copy()
        
        for col in cat_cols:
            le = LabelEncoder()
            self.df_encoded[col] = le.fit_transform(self.df_encoded[col])
            self.label_encoders[col] = le
        
        print(f"Encoded {len(cat_cols)} categorical columns")
        print(f"Shape: {self.df_encoded.shape}")
        
        return self.df_encoded
    
    def scale_features(self):
        """Scale numerical features using StandardScaler"""
        print("\n" + "="*50)
        print("FEATURE SCALING")
        print("="*50)
        
        # Features to scale
        scale_cols = ['unit_price', 'quantity', 'discount_percent', 'discount_amount', 
                      'revenue', 'pages_viewed', 'time_on_site_sec', 'visit_day', 
                      'visit_month', 'visit_weekday', 'location', 
                      'avg_spending_per_session', 'pages_per_minute', 'discount_impact']
        
        self.scaler = StandardScaler()
        self.df_scaled = self.df_encoded.copy()
        self.df_scaled[scale_cols] = self.scaler.fit_transform(self.df_scaled[scale_cols])
        
        print(f"Scaled {len(scale_cols)} numerical features")
        print(f"Shape: {self.df_scaled.shape}")
        
        return self.df_scaled
    
    def aggregate_customers(self):
        """Aggregate data at customer level"""
        print("\n" + "="*50)
        print("CUSTOMER AGGREGATION")
        print("="*50)
        
        customer_features = self.df.groupby('customer_id').agg({
            'revenue': 'sum',
            'purchased': 'sum',
            'rating': 'mean',
            'pages_viewed': 'sum',
            'time_on_site_sec': 'sum',
            'cart_abandoned': 'sum',
            'session_id': 'count'
        }).reset_index()
        
        customer_features.columns = ['customer_id', 'total_revenue', 'total_purchases', 
                                     'avg_rating', 'total_pages_viewed', 'total_time_on_site',
                                     'total_cart_abandoned', 'total_sessions']
        
        print(f"Aggregated {customer_features.shape[0]:,} customers")
        print(f"Shape: {customer_features.shape}")
        
        return customer_features
    
    def run_pipeline(self):
        """Run the complete preprocessing pipeline"""
        self.load_data()
        self.check_data_quality()
        self.feature_engineering()
        self.encode_categorical()
        self.scale_features()
        customer_data = self.aggregate_customers()
        
        print("\n" + "="*50)
        print("PREPROCESSING COMPLETE!")
        print("="*50)
        
        return customer_data


# Example usage
if __name__ == "__main__":
    preprocessor = DataPreprocessor("../data/customer_data.csv")
    customer_data = preprocessor.run_pipeline()
    
    # Save processed data
    customer_data.to_csv("../data/customer_features.csv", index=False)
    print("\n✓ Customer features saved to '../data/customer_features.csv'")