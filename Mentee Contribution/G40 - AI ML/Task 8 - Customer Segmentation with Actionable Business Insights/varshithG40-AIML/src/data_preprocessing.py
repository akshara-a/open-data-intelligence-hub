from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def load_datasets(data_dir: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    data_dir = Path(data_dir or Path(__file__).resolve().parent.parent / "data")
    customer_df = pd.read_csv(data_dir / "customer_data.csv")
    transactions_df = pd.read_csv(data_dir / "transactions.csv")
    transactions_df["OrderDate"] = pd.to_datetime(transactions_df["OrderDate"])
    customer_df["CustomerID"] = customer_df["CustomerID"].astype(str)
    transactions_df["CustomerID"] = transactions_df["CustomerID"].astype(str)
    return customer_df, transactions_df


def build_rfm_features(transactions_df: pd.DataFrame, reference_date: pd.Timestamp | None = None) -> pd.DataFrame:
    if reference_date is None:
        reference_date = transactions_df["OrderDate"].max() + pd.Timedelta(days=1)

    rfm = (
        transactions_df.groupby("CustomerID")
        .agg(
            Recency=("OrderDate", lambda dates: (reference_date - dates.max()).days),
            Frequency=("OrderID", "nunique"),
            Monetary=("Amount", "sum"),
        )
        .reset_index()
    )
    rfm["AverageOrderValue"] = (rfm["Monetary"] / rfm["Frequency"]).round(2)
    return rfm


def prepare_feature_frame(customer_df: pd.DataFrame, rfm_df: pd.DataFrame) -> pd.DataFrame:
    merged = customer_df.merge(
        rfm_df.drop(columns=["AverageOrderValue"], errors="ignore"),
        on="CustomerID",
        how="left",
    )
    merged["DiscountUsage"] = merged["DiscountUsage"].fillna(0.0)
    merged["CustomerRating"] = merged["CustomerRating"].fillna(merged["CustomerRating"].mean())
    merged["AnnualIncome"] = merged["AnnualIncome"].fillna(merged["AnnualIncome"].mean())
    merged["DaysSinceLastPurchase"] = merged["DaysSinceLastPurchase"].fillna(merged["DaysSinceLastPurchase"].mean())

    merged["log_monetary"] = np.log1p(merged["Monetary"])
    merged["log_spending"] = np.log1p(merged["TotalSpending"])
    return merged


def scale_features(features: pd.DataFrame) -> tuple[pd.DataFrame, StandardScaler]:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    return pd.DataFrame(scaled, columns=features.columns, index=features.index), scaler
