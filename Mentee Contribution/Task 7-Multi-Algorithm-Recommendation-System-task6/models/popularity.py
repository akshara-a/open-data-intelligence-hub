from pathlib import Path
import pandas as pd

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load cleaned dataset
DATA_PATH = BASE_DIR / "data" / "clean_amazon.csv"

df = pd.read_csv(DATA_PATH)


def popularity_recommendations(top_n=10):
    """
    Recommend the most popular products based on:
    - Average Rating
    - Number of Reviews
    """

    popularity = (
        df.groupby(["product_id", "product_name"])
        .agg(
            Average_Rating=("rating", "mean"),
            Number_of_Reviews=("rating", "count")
        )
        .reset_index()
    )

    # Only include products with at least 10 reviews
    popularity = popularity[popularity["Number_of_Reviews"] >= 10]

    # Sort by rating first, then review count
    popularity = popularity.sort_values(
        by=["Average_Rating", "Number_of_Reviews"],
        ascending=False
    )

    return popularity.head(top_n)


# Test
if __name__ == "__main__":
    print(popularity_recommendations(10))