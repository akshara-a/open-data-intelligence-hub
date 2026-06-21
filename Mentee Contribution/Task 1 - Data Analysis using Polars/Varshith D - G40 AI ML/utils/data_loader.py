"""
Data loader and processing utilities for the Social Progress Analytics dashboard.

Handles loading, cleaning, transforming, filtering, and aggregating the
World Happiness Report dataset.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st

from utils.config import FACTOR_COLUMNS, FACTOR_ORDER

# =============================================================================
# Constants
# =============================================================================

_DATA_PATH: Path = Path("data/WHR26_Data_Figure_2.1.xlsx")

# Columns we expect after standardization
_CORE_COLUMNS: list[str] = [
    "Year",
    "Rank",
    "Country name",
    "Life Evaluation",
    "Upper whisker",
    "Lower whisker",
]

_FACTOR_FULL_COLUMNS: list[str] = list(FACTOR_COLUMNS.values())


# =============================================================================
# Loading & Cleaning
# =============================================================================


@st.cache_data(show_spinner="Loading World Happiness Report data …", ttl=3600)
def load_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the WHR Excel file, standardise columns, and return a clean DataFrame.

    The function is cached via ``st.cache_data`` so that the file is read only
    once per session (or until the TTL expires).

    Args:
        path: Optional override for the data file path.  Falls back to
              ``data/WHR26_Data_Figure_2.1.xlsx``.

    Returns:
        A cleaned ``pd.DataFrame`` ready for analysis.

    Raises:
        FileNotFoundError: If the Excel file cannot be found.
        ValueError: If critical columns are missing after standardization.
    """
    file_path = Path(path) if path else _DATA_PATH

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found at '{file_path.resolve()}'. "
            "Please place the WHR Excel file in the 'data/' directory."
        )

    df = pd.read_excel(file_path)

    # ── Strip whitespace from column names ──────────────────────────────
    df.columns = df.columns.str.strip()

    # ── Auto-detect the Life Evaluation column ──────────────────────────
    df = _rename_life_evaluation_column(df)

    # ── Ensure a "Rank" column exists ───────────────────────────────────
    if "Rank" not in df.columns:
        # Some file versions use an unnamed first numeric column as rank
        for col in df.columns:
            if df[col].dtype in ("int64", "float64") and col not in (
                "Year",
                "Life Evaluation",
                "Upper whisker",
                "Lower whisker",
                *_FACTOR_FULL_COLUMNS,
            ):
                df = df.rename(columns={col: "Rank"})
                break

    # ── Data-type coercion ──────────────────────────────────────────────
    df = _coerce_dtypes(df)

    # ── Handle missing values ───────────────────────────────────────────
    df = _handle_missing(df)

    # ── Validate ────────────────────────────────────────────────────────
    _validate(df)

    return df


# =============================================================================
# Internal Helpers
# =============================================================================


def _rename_life_evaluation_column(df: pd.DataFrame) -> pd.DataFrame:
    """Auto-detect and rename the life-evaluation / Cantril-ladder column.

    Searches column names (case-insensitive) for ``'life evaluation'`` or
    ``'cantril'`` and renames the first match to ``'Life Evaluation'``.

    Args:
        df: Raw DataFrame right after loading.

    Returns:
        DataFrame with the column renamed (if found).

    Raises:
        ValueError: If no matching column is found.
    """
    for col in df.columns:
        if "life evaluation" in col.lower() or "cantril" in col.lower():
            df = df.rename(columns={col: "Life Evaluation"})
            return df
    raise ValueError(
        "Could not auto-detect the Life Evaluation column. "
        "Expected a column containing 'life evaluation' or 'cantril' in its name."
    )


def _coerce_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to their expected data types.

    Args:
        df: DataFrame after column renaming.

    Returns:
        DataFrame with corrected dtypes.
    """
    # Integer columns
    for col in ("Year", "Rank"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Float columns
    float_cols = [
        "Life Evaluation",
        "Upper whisker",
        "Lower whisker",
        *_FACTOR_FULL_COLUMNS,
    ]
    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    # String columns
    if "Country name" in df.columns:
        df["Country name"] = df["Country name"].astype(str).str.strip()

    return df


def _handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values with sensible defaults.

    - Numeric factor columns: fill with ``0.0`` (they represent additive
      components, so zero means "not explained").
    - Drop rows missing *both* country name and life evaluation.

    Args:
        df: DataFrame after dtype coercion.

    Returns:
        DataFrame with missing values handled.
    """
    # Drop rows with no country AND no score
    df = df.dropna(subset=["Country name", "Life Evaluation"], how="all")

    # Fill factor columns with 0 where missing
    for col in _FACTOR_FULL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)

    return df


def _validate(df: pd.DataFrame) -> None:
    """Run basic validation checks on the cleaned DataFrame.

    Args:
        df: Cleaned DataFrame.

    Raises:
        ValueError: If critical columns are missing or the DataFrame is empty.
    """
    if df.empty:
        raise ValueError("The dataset is empty after cleaning.")

    required = {"Year", "Country name", "Life Evaluation"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing critical columns after cleaning: {missing}")


# =============================================================================
# Filter Functions
# =============================================================================


def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Return rows for a specific year.

    Args:
        df: Full dataset.
        year: Target year.

    Returns:
        Filtered DataFrame.
    """
    return df.loc[df["Year"] == year].copy()


def filter_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Return all rows for a single country (all years).

    Args:
        df: Full dataset.
        country: Country name (exact, case-sensitive).

    Returns:
        Filtered DataFrame sorted by year.
    """
    return df.loc[df["Country name"] == country].sort_values("Year").copy()


def filter_by_countries(
    df: pd.DataFrame, countries: list[str]
) -> pd.DataFrame:
    """Return rows for multiple countries.

    Args:
        df: Full dataset.
        countries: List of country names.

    Returns:
        Filtered DataFrame.
    """
    return df.loc[df["Country name"].isin(countries)].copy()


def filter_top_n(
    df: pd.DataFrame,
    year: int,
    n: int = 10,
    ascending: bool = False,
) -> pd.DataFrame:
    """Return the top (or bottom) *n* countries for a given year by Life Evaluation.

    Args:
        df: Full dataset.
        year: Target year.
        n: Number of countries to return.
        ascending: If ``True``, return the *lowest*-scoring countries instead.

    Returns:
        DataFrame with *n* rows, sorted by Life Evaluation.
    """
    year_df = filter_by_year(df, year)
    return (
        year_df.sort_values("Life Evaluation", ascending=ascending)
        .head(n)
        .copy()
    )


# =============================================================================
# Aggregation Functions
# =============================================================================


def yearly_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Compute global averages of Life Evaluation and factor columns per year.

    Args:
        df: Full dataset.

    Returns:
        DataFrame indexed by Year with mean values.
    """
    numeric_cols = ["Life Evaluation", *_FACTOR_FULL_COLUMNS]
    available = [c for c in numeric_cols if c in df.columns]
    return (
        df.groupby("Year")[available]
        .mean()
        .reset_index()
        .sort_values("Year")
    )


def country_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-country averages across all available years.

    Args:
        df: Full dataset.

    Returns:
        DataFrame indexed by Country name with mean values, sorted descending
        by Life Evaluation.
    """
    numeric_cols = ["Life Evaluation", *_FACTOR_FULL_COLUMNS]
    available = [c for c in numeric_cols if c in df.columns]
    return (
        df.groupby("Country name")[available]
        .mean()
        .reset_index()
        .sort_values("Life Evaluation", ascending=False)
    )


def year_over_year_changes(
    df: pd.DataFrame, country: str
) -> pd.DataFrame:
    """Compute year-over-year changes in Life Evaluation for a country.

    Args:
        df: Full dataset.
        country: Country name.

    Returns:
        DataFrame with columns ``Year``, ``Life Evaluation``, and
        ``YoY Change``.
    """
    cdf = filter_by_country(df, country)[["Year", "Life Evaluation"]].copy()
    cdf["YoY Change"] = cdf["Life Evaluation"].diff()
    return cdf


# =============================================================================
# Comparative / Analytical Functions
# =============================================================================


def top_gainers_losers(
    df: pd.DataFrame,
    year_start: int,
    year_end: int,
    n: int = 10,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Identify the top *n* gainers and losers in Life Evaluation between two years.

    Args:
        df: Full dataset.
        year_start: Starting year for comparison.
        year_end: Ending year for comparison.
        n: Number of countries to return for each group.

    Returns:
        A tuple ``(gainers_df, losers_df)``, each containing columns
        ``Country name``, ``Score Start``, ``Score End``, and ``Change``.
    """
    df_start = filter_by_year(df, year_start)[["Country name", "Life Evaluation"]]
    df_end = filter_by_year(df, year_end)[["Country name", "Life Evaluation"]]

    merged = df_start.merge(
        df_end, on="Country name", suffixes=(" Start", " End")
    )
    merged.columns = ["Country name", "Score Start", "Score End"]
    merged["Change"] = merged["Score End"] - merged["Score Start"]

    gainers = merged.nlargest(n, "Change").reset_index(drop=True)
    losers = merged.nsmallest(n, "Change").reset_index(drop=True)

    return gainers, losers


def compute_correlations(df: pd.DataFrame) -> pd.Series:
    """Compute Pearson correlations between Life Evaluation and each factor column.

    Args:
        df: Full dataset (or a filtered subset).

    Returns:
        A ``pd.Series`` mapping factor short names to correlation coefficients,
        sorted by absolute value descending.
    """
    correlations: dict[str, float] = {}
    for short_name, full_col in FACTOR_COLUMNS.items():
        if full_col in df.columns:
            corr = df["Life Evaluation"].corr(df[full_col])
            correlations[short_name] = round(corr, 4)

    series = pd.Series(correlations, name="Correlation")
    return series.reindex(series.abs().sort_values(ascending=False).index)


# =============================================================================
# Convenience Accessors
# =============================================================================


def get_latest_year(df: pd.DataFrame) -> int:
    """Return the most recent year present in the dataset.

    Args:
        df: Full dataset.

    Returns:
        Latest year as an integer.
    """
    return int(df["Year"].max())


def get_latest_year_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return the dataset filtered to the latest available year.

    Args:
        df: Full dataset.

    Returns:
        DataFrame for the latest year, sorted by Rank.
    """
    latest = get_latest_year(df)
    return filter_by_year(df, latest).sort_values("Rank")


def get_available_years(df: pd.DataFrame) -> list[int]:
    """Return a sorted list of all years in the dataset.

    Args:
        df: Full dataset.

    Returns:
        Ascending list of years.
    """
    return sorted(df["Year"].dropna().unique().astype(int).tolist())


def get_available_countries(df: pd.DataFrame) -> list[str]:
    """Return an alphabetically sorted list of unique country names.

    Args:
        df: Full dataset.

    Returns:
        Sorted list of country names.
    """
    return sorted(df["Country name"].dropna().unique().tolist())


def get_country_profile(
    df: pd.DataFrame, country: str, year: Optional[int] = None
) -> dict:
    """Build a profile dictionary for a single country in a given year.

    If *year* is ``None``, the latest available year is used.  The profile
    contains the score, rank, factor breakdown, whisker bounds, and metadata.

    Args:
        df: Full dataset.
        country: Country name.
        year: Optional year override.

    Returns:
        Dictionary with keys: ``country``, ``year``, ``rank``, ``score``,
        ``upper_whisker``, ``lower_whisker``, ``factors`` (dict of short-name
        → value), and ``yoy_change``.

    Raises:
        ValueError: If the country/year combination is not found.
    """
    year = year or get_latest_year(df)
    row = df.loc[
        (df["Country name"] == country) & (df["Year"] == year)
    ]

    if row.empty:
        raise ValueError(
            f"No data found for '{country}' in year {year}."
        )

    row = row.iloc[0]

    # Factor breakdown
    factors: dict[str, float] = {}
    for short_name in FACTOR_ORDER:
        full_col = FACTOR_COLUMNS[short_name]
        factors[short_name] = float(row.get(full_col, 0.0))

    # Year-over-year change
    prev_row = df.loc[
        (df["Country name"] == country) & (df["Year"] == year - 1)
    ]
    yoy: Optional[float] = None
    if not prev_row.empty:
        yoy = float(row["Life Evaluation"]) - float(
            prev_row.iloc[0]["Life Evaluation"]
        )

    # Historical best and worst ranks
    country_all = df[df["Country name"] == country].dropna(subset=["Rank"])
    if not country_all.empty:
        best_idx = country_all["Rank"].idxmin()
        best_rank = int(country_all.loc[best_idx, "Rank"])
        best_year = int(country_all.loc[best_idx, "Year"])

        worst_idx = country_all["Rank"].idxmax()
        worst_rank = int(country_all.loc[worst_idx, "Rank"])
        worst_year = int(country_all.loc[worst_idx, "Year"])
    else:
        best_rank = int(row.get("Rank", 0))
        best_year = int(year)
        worst_rank = int(row.get("Rank", 0))
        worst_year = int(year)

    return {
        "country": country,
        "year": int(year),
        "rank": int(row.get("Rank", 0)),
        "score": float(row["Life Evaluation"]),
        "upper_whisker": float(row.get("Upper whisker", 0.0)),
        "lower_whisker": float(row.get("Lower whisker", 0.0)),
        "factors": factors,
        "yoy_change": yoy,
        "best_rank": best_rank,
        "best_year": best_year,
        "worst_rank": worst_rank,
        "worst_year": worst_year,
    }
