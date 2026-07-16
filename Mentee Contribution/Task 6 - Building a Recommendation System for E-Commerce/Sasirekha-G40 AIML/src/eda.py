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
