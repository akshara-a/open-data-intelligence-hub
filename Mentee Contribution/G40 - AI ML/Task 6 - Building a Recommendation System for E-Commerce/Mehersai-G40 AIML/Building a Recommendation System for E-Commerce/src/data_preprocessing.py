import pandas as pd
from pathlib import Path


def load_data(file_path):
    """
    Load the e-commerce dataset from a CSV file.
    """

    df = pd.read_csv(file_path)

    print("Dataset loaded successfully.")
    print(f"Original Shape: {df.shape}")

    return df


def preprocess_data(df):
    """
    Clean and preprocess the e-commerce dataset.
    """

    print("\nStarting data preprocessing...")


    # Create a copy of the original dataset
    df = df.copy()


    # Convert visit_date to datetime
    df["visit_date"] = pd.to_datetime(
        df["visit_date"],
        format="%d-%m-%Y"
    )


    # Remove duplicate records
    duplicate_count = df.duplicated().sum()

    print(f"Duplicate records found: {duplicate_count}")

    if duplicate_count > 0:
        df = df.drop_duplicates()


    # Check missing values
    missing_values = df.isnull().sum().sum()

    print(f"Total missing values: {missing_values}")


    # Remove identifier columns from ML features later
    identifier_columns = [
        "customer_id",
        "session_id",
        "product_id"
    ]

    print(
        "Identifier columns identified:",
        identifier_columns
    )


    # Check binary columns
    binary_columns = [
        "added_to_cart",
        "purchased",
        "cart_abandoned"
    ]

    print("\nBinary column values:")

    for column in binary_columns:
        print(
            f"{column}: "
            f"{sorted(df[column].unique())}"
        )


    # Check rating range
    print(
        "\nRating range:",
        df["rating"].min(),
        "to",
        df["rating"].max()
    )


    # Check invalid numerical values
    numerical_checks = [
        "unit_price",
        "quantity",
        "discount_percent",
        "discount_amount",
        "revenue",
        "pages_viewed",
        "time_on_site_sec"
    ]

    print("\nChecking negative values:")

    for column in numerical_checks:

        negative_count = (df[column] < 0).sum()

        print(
            f"{column}: "
            f"{negative_count} negative values"
        )


    # Create useful behavioral features
    df["discount_applied"] = (
        df["discount_percent"] > 0
    ).astype(int)


    df["engagement_score"] = (
        df["pages_viewed"]
        * df["time_on_site_sec"]
    )


    print("\nNew features created:")
    print("- discount_applied")
    print("- engagement_score")


    print(
        f"\nProcessed Dataset Shape: {df.shape}"
    )

    print("\nData preprocessing completed.")

    return df


def save_processed_data(df, output_path):
    """
    Save the processed dataset.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nProcessed dataset saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":

    input_file = "data/Ecommerce.csv"

    output_file = (
        "data/processed_ecommerce_data.csv"
    )

    ecommerce_df = load_data(input_file)

    processed_df = preprocess_data(
        ecommerce_df
    )

    save_processed_data(
        processed_df,
        output_file
    )