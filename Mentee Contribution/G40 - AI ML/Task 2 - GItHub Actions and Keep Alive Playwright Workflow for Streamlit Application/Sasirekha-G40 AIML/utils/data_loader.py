import streamlit as st
import polars as pl
import pandas as pd


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    """
    Load the Excel dataset and convert it to a Polars DataFrame.
    """

    df = pd.read_excel(
        "data/E Commerce Dataset.xlsx",
        sheet_name="E Comm"
    )

    return pl.from_pandas(df)


# --------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------
def total_customers(df):
    return df.height


def churn_customers(df):
    return df.filter(pl.col("Churn") == 1).height


def retained_customers(df):
    return df.filter(pl.col("Churn") == 0).height


def churn_rate(df):
    total = total_customers(df)

    if total == 0:
        return 0

    return round(
        (churn_customers(df) / total) * 100,
        2
    )


def average_satisfaction(df):
    value = df["SatisfactionScore"].mean()

    if value is None:
        return 0

    return round(value, 2)


def average_cashback(df):
    value = df["CashbackAmount"].mean()

    if value is None:
        return 0

    return round(value, 2)


def average_orders(df):
    value = df["OrderCount"].mean()

    if value is None:
        return 0

    return round(value, 2)


# --------------------------------------------------
# Dataset Information
# --------------------------------------------------
def dataset_shape(df):
    return {
        "Rows": df.height,
        "Columns": df.width
    }


def missing_values(df):
    return (
        df.null_count()
        .transpose(
            include_header=True,
            header_name="Column",
            column_names=["Missing Values"]
        )
    )


def statistics(df):
    return df.describe()