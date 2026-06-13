"""
Shared helper functions for Marine Climate Intelligence Platform
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.styles import PLOTLY_THEME
import copy


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_default_data() -> pd.DataFrame:
    """Load the bundled sample dataset."""
    df = pd.read_csv("data/marine_climate_data.csv", parse_dates=["Date"])
    return df


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """Parse a user-uploaded CSV."""
    df = pd.read_csv(uploaded_file)
    # Try to parse any column that looks like a date
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
    return df


# ── Chart Helpers ─────────────────────────────────────────────────────────────

def apply_theme(fig: go.Figure) -> go.Figure:
    """Apply the platform's dark-ocean Plotly theme to a figure."""
    theme = copy.deepcopy(PLOTLY_THEME["layout"])
    fig.update_layout(**theme)
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=380,
    )
    return fig


def line_chart(df: pd.DataFrame, x: str, y: str | list, title: str,
               color=None, labels=None) -> go.Figure:
    """Convenience wrapper for line charts."""
    if isinstance(y, list):
        fig = px.line(df, x=x, y=y, title=title, labels=labels or {})
    else:
        kwargs = dict(x=x, y=y, title=title, labels=labels or {})
        if color:
            kwargs["color"] = color
        fig = px.line(df, **kwargs)
    return apply_theme(fig)


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str,
              color=None, labels=None) -> go.Figure:
    kwargs = dict(x=x, y=y, title=title, labels=labels or {})
    if color:
        kwargs["color"] = color
    fig = px.bar(df, **kwargs)
    return apply_theme(fig)


def scatter_chart(df: pd.DataFrame, x: str, y: str, title: str,
                  color=None, size=None) -> go.Figure:
    kwargs = dict(x=x, y=y, title=title)
    if color:
        kwargs["color"] = color
    if size:
        kwargs["size"] = size
    fig = px.scatter(df, **kwargs)
    return apply_theme(fig)


def gauge_chart(value: float, title: str, max_val: float = 100,
                thresholds: dict = None) -> go.Figure:
    """Render a risk-gauge figure."""
    if thresholds is None:
        thresholds = {"low": 30, "medium": 60, "high": 80}

    if value < thresholds["low"]:
        color = "#00BFA5"
    elif value < thresholds["medium"]:
        color = "#FFB300"
    elif value < thresholds["high"]:
        color = "#FF6B35"
    else:
        color = "#E53935"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#E8F4FD", "size": 13}},
        number={"font": {"color": "#E8F4FD", "family": "JetBrains Mono"}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#90CAF9",
                     "tickfont": {"color": "#90CAF9"}},
            "bar": {"color": color, "thickness": 0.22},
            "bgcolor": "rgba(6,30,60,0.5)",
            "bordercolor": "rgba(0,229,255,0.15)",
            "steps": [
                {"range": [0, thresholds["low"]], "color": "rgba(0,191,165,0.08)"},
                {"range": [thresholds["low"], thresholds["medium"]], "color": "rgba(255,179,0,0.08)"},
                {"range": [thresholds["medium"], thresholds["high"]], "color": "rgba(255,107,53,0.08)"},
                {"range": [thresholds["high"], max_val], "color": "rgba(229,57,53,0.1)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.8,
                "value": value,
            },
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Space Grotesk"},
        height=240,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


# ── Risk Computation ──────────────────────────────────────────────────────────

def compute_risk_scores(df: pd.DataFrame) -> dict:
    """Return composite risk scores for the most recent period."""
    recent = df[df["Date"] >= df["Date"].max() - pd.DateOffset(years=1)]

    temp_col   = next((c for c in df.columns if "temp" in c.lower()), None)
    coral_col  = next((c for c in df.columns if "coral" in c.lower()), None)
    ph_col     = next((c for c in df.columns if "ph" in c.lower()), None)
    sl_col     = next((c for c in df.columns if "sea_level" in c.lower() or "level" in c.lower()), None)

    scores = {}

    if temp_col:
        temp_mean = recent[temp_col].mean()
        temp_base = df[df["Date"].dt.year <= 2005][temp_col].mean() if len(df) > 100 else temp_mean
        scores["ocean_warming"] = min(100, max(0, (temp_mean - temp_base) / 3 * 100))
    else:
        scores["ocean_warming"] = 45.0

    if coral_col:
        scores["coral_bleaching"] = min(100, recent[coral_col].mean())
    else:
        scores["coral_bleaching"] = 55.0

    if ph_col:
        ph_mean = recent[ph_col].mean()
        scores["acidification"] = min(100, max(0, (8.2 - ph_mean) / 0.3 * 100))
    else:
        scores["acidification"] = 40.0

    if sl_col:
        sl_max = recent[sl_col].max()
        scores["sea_level"] = min(100, max(0, sl_max / 100 * 80))
    else:
        scores["sea_level"] = 60.0

    scores["composite"] = round(
        scores["ocean_warming"] * 0.3 +
        scores["coral_bleaching"] * 0.25 +
        scores["acidification"] * 0.25 +
        scores["sea_level"] * 0.2, 1
    )
    return {k: round(v, 1) for k, v in scores.items()}


def risk_label(score: float) -> str:
    if score < 30:  return "Low"
    if score < 60:  return "Moderate"
    if score < 80:  return "High"
    return "Critical"


def risk_css_class(score: float) -> str:
    if score < 30:  return "risk-low"
    if score < 60:  return "risk-medium"
    if score < 80:  return "risk-high"
    return "risk-critical"


# ── Stats Helpers ─────────────────────────────────────────────────────────────

def compute_stats(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    stats = df[numeric_cols].describe().T
    stats.columns = ["Count", "Mean", "Std Dev", "Min", "25%", "50%", "75%", "Max"]
    return stats.round(3)


def yearly_avg(df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
    df = df.copy()
    df["Year"] = df[date_col].dt.year
    return df.groupby("Year")[value_col].mean().reset_index()
