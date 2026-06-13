from pathlib import Path
import json
import pickle

import polars as pl
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "survey_results_public.csv"
MODEL_PATH = ROOT / "salary_model.pkl"
METADATA_PATH = ROOT / "model_metadata.json"


def load_data(path: Path = DATA_PATH) -> pl.DataFrame:
    return pl.read_csv(path)


def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(
            pl.col("ConvertedCompYearly")
            .str.replace_all(r"[^0-9.]", "")
            .cast(pl.Float64, strict=False),
            pl.col("YearsCodePro")
            .str.replace_all(r"[^0-9.]", "")
            .cast(pl.Float64, strict=False),
        )
        .filter(
            pl.col("ConvertedCompYearly").is_not_null()
            & pl.col("YearsCodePro").is_not_null()
            & pl.col("RemoteWork").is_not_null()
            & pl.col("Country").is_not_null()
        )
    )


def train_model(df: pl.DataFrame) -> Pipeline:
    model_df = df.select(
        ["Country", "YearsCodePro", "RemoteWork", "ConvertedCompYearly"]
    ).to_pandas()

    feature_columns = ["Country", "YearsCodePro", "RemoteWork"]
    preprocessor = ColumnTransformer(
        [
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                ["Country", "RemoteWork"],
            )
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        [
            ("preprocess", preprocessor),
            ("regressor", Ridge()),
        ]
    )

    pipeline.fit(model_df[feature_columns], model_df["ConvertedCompYearly"])
    return pipeline


def save_model(model: Pipeline, path: Path = MODEL_PATH) -> None:
    with path.open("wb") as model_file:
        pickle.dump(model, model_file)


def save_metadata(df: pl.DataFrame, path: Path = METADATA_PATH) -> None:
    valid_countries = df.filter(
        pl.col("Country").is_not_null()
        & (pl.col("Country") != "NA")
        & (pl.col("Country") != "")
    )
    valid_remote = valid_countries.filter(
        pl.col("RemoteWork").is_not_null()
        & (pl.col("RemoteWork") != "NA")
        & (pl.col("RemoteWork") != "")
    )
    metadata = {
        "countries": sorted(valid_countries.select("Country").unique().to_series().to_list()),
        "remoteWorkOptions": sorted(valid_remote.select("RemoteWork").unique().to_series().to_list()),
    }
    with path.open("w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)


def main() -> None:
    df = load_data()
    df = clean_data(df)
    model = train_model(df)
    save_model(model)
    save_metadata(df)
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved metadata to: {METADATA_PATH}")


if __name__ == "__main__":
    main()
