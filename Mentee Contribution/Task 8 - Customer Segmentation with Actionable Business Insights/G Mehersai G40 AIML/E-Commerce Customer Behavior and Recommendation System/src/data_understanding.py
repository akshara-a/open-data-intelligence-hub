import pandas as pd


DATA_PATH = "data/Ecommerce.csv"


def load_data(file_path):
    """Load the e-commerce dataset."""
    df = pd.read_csv(file_path)
    return df


def understand_data(df):
    """Display basic information about the dataset."""

    print("\n--- DATASET SHAPE ---")
    print("Number of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])

    print("\n--- FIRST 5 ROWS ---")
    print(df.head())

    print("\n--- COLUMN NAMES ---")
    for column in df.columns:
        print(column)

    print("\n--- DATASET INFORMATION ---")
    df.info()

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DUPLICATE ROWS ---")
    print("Number of duplicate rows:", df.duplicated().sum())

    print("\n--- NUMERICAL SUMMARY ---")
    print(df.describe().T)

    print("\n--- CATEGORICAL SUMMARY ---")
    print(df.describe(include="str").T)

    print("\n--- DATASET OVERVIEW ---")
    print("Unique Customers:", df["customer_id"].nunique())
    print("Unique Products:", df["product_id"].nunique())
    print(
        "Product Categories:",
        df["product_category"].nunique()
    )

    print("\n--- PURCHASE DISTRIBUTION ---")
    print(df["purchased"].value_counts())

    print("\n--- PURCHASE DISTRIBUTION (%) ---")
    purchase_percentage = (
        df["purchased"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    print(purchase_percentage)


def main():
    df = load_data(DATA_PATH)

    print("Dataset loaded successfully.")

    understand_data(df)


if __name__ == "__main__":
    main()