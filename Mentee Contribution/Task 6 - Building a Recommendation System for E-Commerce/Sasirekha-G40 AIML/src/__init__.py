import pandas as pd

def load_dataset(path):
    return pd.read_csv(path)

def save_dataset(df, path):
    df.to_csv(path, index=False)
    print(f"Dataset saved to: {path}")
    
    
import matplotlib.pyplot as plt
import seaborn as sns

def plot_age_distribution(df):
    plt.figure(figsize=(8,5))
    sns.histplot(df["Age"], bins=15)
    plt.title("Age Distribution")
    plt.show()

def plot_category_distribution(df):
    plt.figure(figsize=(10,5))
    sns.countplot(x="Category", data=df)
    plt.xticks(rotation=45)
    plt.title("Category Distribution")
    plt.show()
    
    
from sklearn.linear_model import Ridge

def train_regression(X_train, y_train):
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    return model
    
       