"""
charts.py — Premium Plotly chart generation for Social Progress Analytics.

Every function returns a ``plotly.graph_objects.Figure`` styled with a
consistent dark-navy theme, clean grid lines, rounded hover tooltips,
and smooth animations.  Colour palettes are imported from the project-level
``utils.config`` module so that every visual across the dashboard is
pixel-perfect consistent.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.config import COLORS, FACTOR_COLORS, FACTOR_COLUMNS, FACTOR_COLUMNS_REVERSE

# ---------------------------------------------------------------------------
# Shared layout helpers
# ---------------------------------------------------------------------------

_HOVER_TEMPLATE_STYLE = dict(
    bgcolor=COLORS["bg_card"],
    font_size=13,
    font_family="Inter, system-ui, sans-serif",
    font_color=COLORS["text_primary"],
    bordercolor=COLORS["border"],
)

_COMMON_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=COLORS["bg_primary"],
    font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text_primary"], size=13),
    margin=dict(l=20, r=20, t=50, b=20),
    hoverlabel=_HOVER_TEMPLATE_STYLE,
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text_primary"], size=12),
        borderwidth=0,
    ),
    xaxis=dict(
        gridcolor=COLORS.get("grid", "rgba(255,255,255,0.06)"),
        zerolinecolor=COLORS.get("grid", "rgba(255,255,255,0.06)"),
        title_font=dict(size=13),
    ),
    yaxis=dict(
        gridcolor=COLORS.get("grid", "rgba(255,255,255,0.06)"),
        zerolinecolor=COLORS.get("grid", "rgba(255,255,255,0.06)"),
        title_font=dict(size=13),
    ),
    transition=dict(duration=400, easing="cubic-in-out"),
)

_MEDAL_COLORS: dict[int, str] = {
    0: "#FFD700",  # Gold
    1: "#C0C0C0",  # Silver
    2: "#CD7F32",  # Bronze
}

_MULTI_LINE_PALETTE: list[str] = [
    COLORS.get("accent_blue", "#6C63FF"),
    COLORS.get("accent_teal", "#00D4AA"),
    COLORS.get("accent_coral", "#FF6B6B"),
    "#FFC857",
    "#17BEBB",
    "#E85D75",
    "#9B5DE5",
    "#F15BB5",
    "#00BBF9",
    "#FEE440",
]


def _apply_common_layout(fig: go.Figure, title: str, height: int) -> go.Figure:
    """Apply the shared dark-theme layout to *fig*."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=COLORS["text_primary"]), x=0.0, xanchor="left"),
        height=height,
        **_COMMON_LAYOUT,
    )
    return fig


def _empty_figure(message: str = "No data available", height: int = 400) -> go.Figure:
    """Return a placeholder figure when data is missing or empty."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color=COLORS.get("text_secondary", "rgba(255,255,255,0.5)")),
    )
    _apply_common_layout(fig, "", height)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


# ---------------------------------------------------------------------------
# 1. Ranking bar chart
# ---------------------------------------------------------------------------


def create_ranking_bar_chart(
    df: pd.DataFrame,
    top_n: int = 15,
    year: Optional[int] = None,
    height: int = 600,
) -> go.Figure:
    """Horizontal bar chart of the top *top_n* countries by Life Evaluation.

    The top-3 bars are highlighted with gold / silver / bronze colours.
    Confidence intervals are shown as error bars when ``upperwhisker``
    and ``lowerwhisker`` columns are present.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``Country name`` and ``Life Ladder`` (or similar score
        column).  Optionally ``year``, ``upperwhisker``, ``lowerwhisker``.
    top_n : int
        Number of countries to display.
    year : int, optional
        If provided the data is filtered to this year first.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df is None or df.empty:
        return _empty_figure("No ranking data available", height)

    data = df.copy()

    # ---------- filter year ----------
    year_col = _find_col(data, ["year"])
    if year is not None and year_col:
        data = data[data[year_col] == year]
    if data.empty:
        return _empty_figure(f"No data for year {year}", height)

    # ---------- identify score column ----------
    score_col = _find_col(data, ["Life Ladder", "Ladder score", "Life Evaluation"])
    country_col = _find_col(data, ["Country name", "Country"])
    if score_col is None or country_col is None:
        return _empty_figure("Required columns not found", height)

    data = data.dropna(subset=[score_col]).nlargest(top_n, score_col)
    data = data.sort_values(score_col, ascending=True)  # bottom-up for horizontal

    # ---------- error bars ----------
    upper_col = _find_col(data, ["upperwhisker", "Upper Whisker", "upper_whisker"])
    lower_col = _find_col(data, ["lowerwhisker", "Lower Whisker", "lower_whisker"])
    error_x = None
    if upper_col and lower_col:
        error_x = dict(
            type="data",
            symmetric=False,
            array=(data[upper_col] - data[score_col]).values,
            arrayminus=(data[score_col] - data[lower_col]).values,
            color="rgba(255,255,255,0.35)",
            thickness=1.5,
            width=3,
        )

    # ---------- colours ----------
    n = len(data)
    bar_colors = [COLORS.get("accent_blue", "#6C63FF")] * n
    for rank, medal in _MEDAL_COLORS.items():
        idx = n - 1 - rank  # reversed because ascending sort
        if 0 <= idx < n:
            bar_colors[idx] = medal

    fig = go.Figure(
        go.Bar(
            x=data[score_col],
            y=data[country_col],
            orientation="h",
            marker=dict(
                color=bar_colors,
                line=dict(width=0),
                cornerradius=4,
            ),
            error_x=error_x,
            hovertemplate=(
                "<b>%{y}</b><br>"
                f"{score_col}: %{{x:.2f}}<extra></extra>"
            ),
        )
    )

    display_year = year or (data[year_col].max() if year_col else "")
    title = f"Top {top_n} Countries — Life Evaluation ({display_year})"
    _apply_common_layout(fig, title, height)
    fig.update_yaxes(tickfont=dict(size=12))
    fig.update_xaxes(title_text=score_col)
    return fig


# ---------------------------------------------------------------------------
# 2. Trend line chart
# ---------------------------------------------------------------------------


def create_trend_line_chart(
    df: pd.DataFrame,
    countries: Sequence[str],
    metric: str = "Life Ladder",
    height: int = 500,
) -> go.Figure:
    """Multi-line trend chart for *countries* over time.

    Parameters
    ----------
    df : pd.DataFrame
        Long-form data with year, country, and the chosen *metric*.
    countries : sequence of str
        Country names to plot.
    metric : str
        Column name of the metric to chart.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df is None or df.empty or not countries:
        return _empty_figure("Select countries to view trends", height)

    data = df.copy()
    country_col = _find_col(data, ["Country name", "Country"])
    year_col = _find_col(data, ["year"])
    score_col = _find_col(data, [metric, "Life Ladder", "Ladder score", "Life Evaluation"])

    if not all([country_col, year_col, score_col]):
        return _empty_figure("Required columns not found", height)

    fig = go.Figure()
    for i, country in enumerate(countries):
        cdf = data[data[country_col] == country].sort_values(year_col)
        if cdf.empty:
            continue
        colour = _MULTI_LINE_PALETTE[i % len(_MULTI_LINE_PALETTE)]
        fig.add_trace(
            go.Scatter(
                x=cdf[year_col],
                y=cdf[score_col],
                mode="lines+markers",
                name=country,
                line=dict(color=colour, width=2.5, shape="spline", smoothing=1.0),
                marker=dict(size=7, color=colour, line=dict(width=1, color="rgba(255,255,255,0.4)")),
                hovertemplate=(
                    f"<b>{country}</b><br>"
                    "Year: %{x}<br>"
                    f"{score_col}: %{{y:.3f}}<extra></extra>"
                ),
            )
        )

    title = f"{score_col} Trends"
    _apply_common_layout(fig, title, height)
    fig.update_xaxes(title_text="Year", dtick=1)
    fig.update_yaxes(title_text=score_col)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    return fig


# ---------------------------------------------------------------------------
# 3. Factor stacked bar
# ---------------------------------------------------------------------------


def create_factor_stacked_bar(
    df: pd.DataFrame,
    countries_or_year: Union[Sequence[str], int],
    height: int = 550,
) -> go.Figure:
    """Stacked bar chart of factor contributions.

    * If *countries_or_year* is an ``int`` it is treated as a year and every
      country in the data for that year is shown.
    * If it is a sequence of strings the data is grouped by year for those
      countries.

    Parameters
    ----------
    df : pd.DataFrame
        Must include factor columns matching ``FACTOR_COLUMNS`` keys.
    countries_or_year : int or sequence of str
        Year or list of country names.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df is None or df.empty:
        return _empty_figure("No factor data available", height)

    data = df.copy()
    data = data.rename(columns=FACTOR_COLUMNS_REVERSE)
    country_col = _find_col(data, ["Country name", "Country"])
    year_col = _find_col(data, ["year"])
    score_col = _find_col(data, ["Life Ladder", "Ladder score", "Life Evaluation"])

    if country_col is None:
        return _empty_figure("Country column not found", height)

    # Determine mode ---------------------------------------------------------
    if isinstance(countries_or_year, (int, np.integer)):
        # Single year → bars = countries
        year_val = int(countries_or_year)
        if year_col:
            data = data[data[year_col] == year_val]
        if score_col:
            data = data.dropna(subset=[score_col]).nlargest(15, score_col)
        x_col = country_col
        title = f"Factor Contributions ({year_val})"
    else:
        # List of countries → bars = years
        if isinstance(countries_or_year, str):
            countries_or_year = [countries_or_year]
        data = data[data[country_col].isin(countries_or_year)]
        if year_col:
            data = data.sort_values(year_col)
        x_col = year_col if year_col else country_col
        title = "Factor Contributions by Year"

    available_factors = [f for f in FACTOR_COLUMNS if f in data.columns]
    if not available_factors:
        # Try matching by displayed name
        inv_map = {v: k for k, v in FACTOR_COLUMNS.items()}
        available_factors = [inv_map[c] for c in data.columns if c in inv_map]
    if not available_factors:
        return _empty_figure("No factor columns found", height)

    fig = go.Figure()
    for factor in available_factors:
        display_name = FACTOR_COLUMNS.get(factor, factor)
        colour = FACTOR_COLORS.get(factor, COLORS.get("accent_blue", "#6C63FF"))
        fig.add_trace(
            go.Bar(
                x=data[x_col] if x_col in data.columns else data.index,
                y=data[factor],
                name=display_name,
                marker=dict(color=colour, cornerradius=2),
                hovertemplate=f"<b>{display_name}</b><br>%{{x}}: %{{y:.3f}}<extra></extra>",
            )
        )

    _apply_common_layout(fig, title, height)
    fig.update_layout(barmode="stack")
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Score contribution")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    return fig


# ---------------------------------------------------------------------------
# 4. Radar / spider chart
# ---------------------------------------------------------------------------


def create_radar_chart(
    df_row_or_rows: pd.DataFrame,
    height: int = 520,
) -> go.Figure:
    """Radar chart comparing factor profiles for 1-3 countries.

    Factors are normalised to a 0-1 scale (min-max across the supplied rows)
    so that axes are directly comparable.

    Parameters
    ----------
    df_row_or_rows : pd.DataFrame
        One to three rows; each row represents a country.  Must include
        a ``Country name`` (or ``Country``) column and factor columns.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df_row_or_rows is None or df_row_or_rows.empty:
        return _empty_figure("No data for radar chart", height)

    data = df_row_or_rows.head(3).copy()
    data = data.rename(columns=FACTOR_COLUMNS_REVERSE)
    country_col = _find_col(data, ["Country name", "Country"])
    available_factors = [f for f in FACTOR_COLUMNS if f in data.columns]

    if not available_factors or country_col is None:
        return _empty_figure("Required columns not found", height)

    # Normalise to 0-1
    factor_vals = data[available_factors].apply(pd.to_numeric, errors="coerce")
    mins = factor_vals.min()
    maxs = factor_vals.max()
    rng = maxs - mins
    rng[rng == 0] = 1  # avoid div-by-zero
    normed = (factor_vals - mins) / rng

    categories = [FACTOR_COLUMNS.get(f, f) for f in available_factors]

    fig = go.Figure()
    for i, (_, row) in enumerate(data.iterrows()):
        vals = normed.loc[row.name, available_factors].tolist()
        vals += [vals[0]]  # close the loop
        cats = categories + [categories[0]]
        colour = _MULTI_LINE_PALETTE[i % len(_MULTI_LINE_PALETTE)]
        fig.add_trace(
            go.Scatterpolar(
                r=vals,
                theta=cats,
                fill="toself",
                fillcolor=_hex_to_rgba(colour, 0.12),
                line=dict(color=colour, width=2),
                name=str(row[country_col]),
                hovertemplate="%{theta}: %{r:.2f}<extra></extra>",
            )
        )

    _apply_common_layout(fig, "Factor Profile Comparison", height)
    fig.update_layout(
        polar=dict(
            bgcolor=COLORS["bg_primary"],
            radialaxis=dict(
                visible=True,
                range=[0, 1.05],
                gridcolor=COLORS.get("grid", "rgba(255,255,255,0.06)"),
                tickfont=dict(size=10, color=COLORS.get("text_secondary", "rgba(255,255,255,0.5)")),
            ),
            angularaxis=dict(
                gridcolor=COLORS.get("grid", "rgba(255,255,255,0.06)"),
                tickfont=dict(size=11, color=COLORS["text_primary"]),
            ),
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# 5. Correlation heatmap
# ---------------------------------------------------------------------------


def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    height: int = 550,
) -> go.Figure:
    """Annotated heatmap of correlation coefficients.

    Uses a blue-white-red diverging colour scale centred on zero.

    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Square correlation matrix (e.g. from ``df.corr()``).
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if corr_matrix is None or corr_matrix.empty:
        return _empty_figure("No correlation data available", height)

    labels = [FACTOR_COLUMNS.get(c, c) for c in corr_matrix.columns]
    z = corr_matrix.values

    # Annotations
    annotations: list[dict] = []
    for i, row in enumerate(z):
        for j, val in enumerate(row):
            annotations.append(
                dict(
                    x=j, y=i,
                    text=f"{val:.2f}",
                    font=dict(size=11, color="white" if abs(val) > 0.5 else COLORS["text_primary"]),
                    showarrow=False,
                )
            )

    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=labels,
            y=labels,
            colorscale=[
                [0.0, "#1e3a5f"],
                [0.25, "#4a90d9"],
                [0.5, "#f0f0f0"],
                [0.75, "#e05252"],
                [1.0, "#8b1a1a"],
            ],
            zmin=-1,
            zmax=1,
            colorbar=dict(
                title="r",
                tickfont=dict(color=COLORS["text_primary"]),
                title_font=dict(color=COLORS["text_primary"]),
            ),
            hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>",
        )
    )

    _apply_common_layout(fig, "Correlation Matrix", height)
    fig.update_layout(annotations=annotations)
    fig.update_xaxes(tickangle=45, tickfont=dict(size=11))
    fig.update_yaxes(tickfont=dict(size=11), autorange="reversed")
    return fig


# ---------------------------------------------------------------------------
# 6. Scatter plot
# ---------------------------------------------------------------------------


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    height: int = 500,
) -> go.Figure:
    """Scatter plot with optional colour encoding and OLS trend line.

    Parameters
    ----------
    df : pd.DataFrame
        Source data.
    x_col, y_col : str
        Column names for the x and y axes.
    color_col : str, optional
        Column used for colour grouping.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df is None or df.empty:
        return _empty_figure("No data for scatter plot", height)

    data = df.dropna(subset=[x_col, y_col]).copy()
    if data.empty:
        return _empty_figure("Insufficient data after removing NaNs", height)

    x_display = FACTOR_COLUMNS.get(x_col, x_col)
    y_display = FACTOR_COLUMNS.get(y_col, y_col)

    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        trendline="ols",
        labels={x_col: x_display, y_col: y_display},
        color_discrete_sequence=_MULTI_LINE_PALETTE,
        hover_data={
            _find_col(data, ["Country name", "Country"]) or x_col: True,
        },
    )

    fig.update_traces(
        marker=dict(size=8, opacity=0.8, line=dict(width=0.5, color="rgba(255,255,255,0.3)")),
    )
    # Style trendline
    for trace in fig.data:
        if trace.mode == "lines":
            trace.update(line=dict(dash="dot", width=2, color="rgba(255,255,255,0.45)"))

    _apply_common_layout(fig, f"{y_display} vs {x_display}", height)
    return fig


# ---------------------------------------------------------------------------
# 7. Rank bump chart
# ---------------------------------------------------------------------------


def create_rank_bump_chart(
    df: pd.DataFrame,
    countries: Sequence[str],
    height: int = 550,
) -> go.Figure:
    """Bump chart showing rank trajectories over time (rank 1 at the top).

    Parameters
    ----------
    df : pd.DataFrame
        Must contain year, country, and a score column from which ranks
        are computed per year.
    countries : sequence of str
        Countries to highlight.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df is None or df.empty or not countries:
        return _empty_figure("Select countries to view rank changes", height)

    data = df.copy()
    country_col = _find_col(data, ["Country name", "Country"])
    year_col = _find_col(data, ["year"])
    score_col = _find_col(data, ["Life Ladder", "Ladder score", "Life Evaluation"])

    if not all([country_col, year_col, score_col]):
        return _empty_figure("Required columns not found", height)

    # Compute ranks per year (1 = best)
    data["_rank"] = data.groupby(year_col)[score_col].rank(ascending=False, method="min").astype(int)

    fig = go.Figure()
    for i, country in enumerate(countries):
        cdf = data[data[country_col] == country].sort_values(year_col)
        if cdf.empty:
            continue
        colour = _MULTI_LINE_PALETTE[i % len(_MULTI_LINE_PALETTE)]
        fig.add_trace(
            go.Scatter(
                x=cdf[year_col],
                y=cdf["_rank"],
                mode="lines+markers+text",
                name=country,
                line=dict(color=colour, width=3, shape="spline", smoothing=0.8),
                marker=dict(size=9, color=colour, line=dict(width=1.5, color="rgba(255,255,255,0.5)")),
                text=cdf["_rank"].astype(str),
                textposition="top center",
                textfont=dict(size=10, color=colour),
                hovertemplate=(
                    f"<b>{country}</b><br>"
                    "Year: %{x}<br>"
                    "Rank: %{y}<extra></extra>"
                ),
            )
        )

    _apply_common_layout(fig, "Rank Trajectories Over Time", height)
    fig.update_yaxes(autorange="reversed", title_text="Rank", dtick=5)
    fig.update_xaxes(title_text="Year", dtick=1)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    return fig


# ---------------------------------------------------------------------------
# 8. Factor comparison grouped bar
# ---------------------------------------------------------------------------


def create_factor_comparison_grouped_bar(
    df_list: Sequence[pd.DataFrame],
    country_names: Sequence[str],
    height: int = 500,
) -> go.Figure:
    """Grouped bar chart comparing factor contributions across countries.

    Parameters
    ----------
    df_list : list of pd.DataFrame
        One DataFrame (single-row or pre-filtered) per country.
    country_names : list of str
        Display names corresponding to each DataFrame.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if not df_list or not country_names:
        return _empty_figure("No comparison data available", height)

    # Rename factor columns in df_list to short names
    df_list = [cdf.rename(columns=FACTOR_COLUMNS_REVERSE) if cdf is not None else None for cdf in df_list]

    # Union of available factor columns across all DataFrames
    all_factors = []
    for cdf in df_list:
        if cdf is not None and not cdf.empty:
            all_factors = [f for f in FACTOR_COLUMNS if f in cdf.columns]
            break
    if not all_factors:
        return _empty_figure("No factor columns found", height)

    categories = [FACTOR_COLUMNS.get(f, f) for f in all_factors]

    fig = go.Figure()
    for i, (cdf, name) in enumerate(zip(df_list, country_names)):
        if cdf is None or cdf.empty:
            continue
        vals = cdf[all_factors].iloc[0].values if len(cdf) else [0] * len(all_factors)
        colour = _MULTI_LINE_PALETTE[i % len(_MULTI_LINE_PALETTE)]
        fig.add_trace(
            go.Bar(
                x=categories,
                y=vals,
                name=name,
                marker=dict(color=colour, cornerradius=3),
                hovertemplate=f"<b>{name}</b><br>%{{x}}: %{{y:.3f}}<extra></extra>",
            )
        )

    _apply_common_layout(fig, "Factor Comparison", height)
    fig.update_layout(barmode="group")
    fig.update_yaxes(title_text="Contribution")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    return fig


# ---------------------------------------------------------------------------
# 9. Box / Violin chart
# ---------------------------------------------------------------------------


def create_box_violin_chart(
    df: pd.DataFrame,
    metric: str,
    group_by: Optional[str] = None,
    kind: str = "violin",
    height: int = 500,
) -> go.Figure:
    """Box or violin plot for distribution analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Source data.
    metric : str
        Numeric column whose distribution is analysed.
    group_by : str
        Categorical column used to split distributions.
    kind : str
        ``'box'`` or ``'violin'``.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df is None or df.empty:
        return _empty_figure("No distribution data available", height)

    data = df.dropna(subset=[metric]).copy()
    if data.empty:
        return _empty_figure("Insufficient data for distribution", height)

    metric_display = FACTOR_COLUMNS.get(metric, metric)

    fig = go.Figure()
    
    if group_by is None:
        groups = ["All Data"]
        group_display = ""
        group_col = None
    else:
        groups = data[group_by].dropna().unique()
        group_display = f" by {FACTOR_COLUMNS.get(group_by, group_by)}"
        group_col = group_by

    for i, grp in enumerate(groups):
        if group_col is None:
            subset = data[metric]
        else:
            subset = data[data[group_col] == grp][metric]
            
        colour = _MULTI_LINE_PALETTE[i % len(_MULTI_LINE_PALETTE)]

        if kind == "box":
            fig.add_trace(
                go.Box(
                    y=subset,
                    name=str(grp),
                    marker_color=colour,
                    line=dict(color=colour),
                    boxmean="sd",
                    hoverinfo="y+name",
                )
            )
        else:
            fig.add_trace(
                go.Violin(
                    y=subset,
                    name=str(grp),
                    line_color=colour,
                    fillcolor=_hex_to_rgba(colour, 0.25),
                    meanline_visible=True,
                    hoverinfo="y+name",
                )
            )

    _apply_common_layout(fig, f"{metric_display} Distribution{group_display}", height)
    fig.update_yaxes(title_text=metric_display)
    return fig


# ---------------------------------------------------------------------------
# 10. Confidence interval chart
# ---------------------------------------------------------------------------


def create_confidence_interval_chart(
    df: pd.DataFrame,
    countries: Sequence[str],
    height: int = 500,
) -> go.Figure:
    """Line chart with shaded 95% confidence-interval bands.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain year, country, score, ``upperwhisker``, and
        ``lowerwhisker`` columns.
    countries : sequence of str
        Countries to include.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if df is None or df.empty or not countries:
        return _empty_figure("Select countries to view CIs", height)

    data = df.copy()
    country_col = _find_col(data, ["Country name", "Country"])
    year_col = _find_col(data, ["year"])
    score_col = _find_col(data, ["Life Ladder", "Ladder score", "Life Evaluation"])
    upper_col = _find_col(data, ["upperwhisker", "Upper Whisker", "upper_whisker"])
    lower_col = _find_col(data, ["lowerwhisker", "Lower Whisker", "lower_whisker"])

    if not all([country_col, year_col, score_col, upper_col, lower_col]):
        return _empty_figure("Confidence interval columns not found", height)

    fig = go.Figure()
    for i, country in enumerate(countries):
        cdf = data[data[country_col] == country].sort_values(year_col)
        if cdf.empty:
            continue
        colour = _MULTI_LINE_PALETTE[i % len(_MULTI_LINE_PALETTE)]
        rgba_fill = _hex_to_rgba(colour, 0.15)

        # Upper bound (invisible line for fill)
        fig.add_trace(
            go.Scatter(
                x=cdf[year_col], y=cdf[upper_col],
                mode="lines",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Lower bound with fill to upper
        fig.add_trace(
            go.Scatter(
                x=cdf[year_col], y=cdf[lower_col],
                mode="lines",
                line=dict(width=0),
                fill="tonexty",
                fillcolor=rgba_fill,
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Centre line
        fig.add_trace(
            go.Scatter(
                x=cdf[year_col], y=cdf[score_col],
                mode="lines+markers",
                name=country,
                line=dict(color=colour, width=2.5),
                marker=dict(size=6, color=colour),
                hovertemplate=(
                    f"<b>{country}</b><br>"
                    "Year: %{x}<br>"
                    f"{score_col}: %{{y:.3f}}<extra></extra>"
                ),
            )
        )

    _apply_common_layout(fig, "Life Evaluation with Confidence Intervals", height)
    fig.update_xaxes(title_text="Year", dtick=1)
    fig.update_yaxes(title_text=score_col)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    return fig


# ---------------------------------------------------------------------------
# 11. Year comparison chart
# ---------------------------------------------------------------------------


def create_year_comparison_chart(
    df_y1: pd.DataFrame,
    df_y2: pd.DataFrame,
    top_n: int = 15,
    height: int = 600,
) -> go.Figure:
    """Grouped bar chart comparing scores between two years.

    Parameters
    ----------
    df_y1, df_y2 : pd.DataFrame
        DataFrames for year-1 and year-2 respectively, each containing
        country and score columns.  A ``year`` column is used for labels.
    top_n : int
        Number of countries to show (union of top performers).
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    if (df_y1 is None or df_y1.empty) and (df_y2 is None or df_y2.empty):
        return _empty_figure("No comparison data available", height)

    def _prep(frame: pd.DataFrame) -> tuple[pd.DataFrame, str, str, str]:
        c = _find_col(frame, ["Country name", "Country"])
        s = _find_col(frame, ["Life Ladder", "Ladder score", "Life Evaluation"])
        y = _find_col(frame, ["year"])
        return frame, c, s, y

    d1, cc1, sc1, yc1 = _prep(df_y1)
    d2, cc2, sc2, yc2 = _prep(df_y2)

    score_col = sc1 or sc2
    country_col = cc1 or cc2
    if score_col is None or country_col is None:
        return _empty_figure("Required columns not found", height)

    # Get union of top-N countries from both years
    top1 = set(d1.nlargest(top_n, score_col)[country_col]) if not d1.empty else set()
    top2 = set(d2.nlargest(top_n, score_col)[country_col]) if not d2.empty else set()
    keep = top1 | top2

    d1 = d1[d1[country_col].isin(keep)].set_index(country_col)
    d2 = d2[d2[country_col].isin(keep)].set_index(country_col)
    all_countries = sorted(keep, key=lambda c: d2[score_col].get(c, d1[score_col].get(c, 0)), reverse=True)

    y1_label = str(int(d1[yc1].iloc[0])) if (yc1 and not d1.empty) else "Year 1"
    y2_label = str(int(d2[yc2].iloc[0])) if (yc2 and not d2.empty) else "Year 2"

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=all_countries,
            x=[d1[score_col].get(c, None) for c in all_countries],
            name=y1_label,
            orientation="h",
            marker=dict(color=COLORS.get("accent_blue", "#6C63FF"), cornerradius=3, opacity=0.7),
            hovertemplate=f"<b>%{{y}}</b> ({y1_label})<br>Score: %{{x:.2f}}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            y=all_countries,
            x=[d2[score_col].get(c, None) for c in all_countries],
            name=y2_label,
            orientation="h",
            marker=dict(color=COLORS.get("accent_teal", "#00D4AA"), cornerradius=3, opacity=0.9),
            hovertemplate=f"<b>%{{y}}</b> ({y2_label})<br>Score: %{{x:.2f}}<extra></extra>",
        )
    )

    _apply_common_layout(fig, f"Year-over-Year Comparison: {y1_label} vs {y2_label}", height)
    fig.update_layout(barmode="group")
    fig.update_xaxes(title_text=score_col)
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=11))
    return fig


# ---------------------------------------------------------------------------
# 12. Top movers chart
# ---------------------------------------------------------------------------


def create_top_movers_chart(
    gainers_df: pd.DataFrame,
    losers_df: pd.DataFrame,
    height: int = 550,
) -> go.Figure:
    """Horizontal diverging bar chart of biggest improvements and declines.

    Parameters
    ----------
    gainers_df : pd.DataFrame
        Must contain ``Country name`` (or ``Country``) and a ``change``
        column with positive values.
    losers_df : pd.DataFrame
        Same structure with negative ``change`` values.
    height : int
        Figure height in pixels.

    Returns
    -------
    go.Figure
    """
    has_gainers = gainers_df is not None and not gainers_df.empty
    has_losers = losers_df is not None and not losers_df.empty
    if not has_gainers and not has_losers:
        return _empty_figure("No mover data available", height)

    fig = go.Figure()

    change_col_names = ["change", "Change", "score_change", "delta"]

    if has_gainers:
        cc = _find_col(gainers_df, ["Country name", "Country"])
        chg = _find_col(gainers_df, change_col_names)
        if cc and chg:
            gdf = gainers_df.sort_values(chg, ascending=True)
            fig.add_trace(
                go.Bar(
                    y=gdf[cc],
                    x=gdf[chg],
                    orientation="h",
                    name="Gainers",
                    marker=dict(color=COLORS.get("success", "#00D4AA"), cornerradius=4),
                    hovertemplate="<b>%{y}</b><br>Change: +%{x:.3f}<extra></extra>",
                )
            )

    if has_losers:
        cc = _find_col(losers_df, ["Country name", "Country"])
        chg = _find_col(losers_df, change_col_names)
        if cc and chg:
            ldf = losers_df.sort_values(chg, ascending=False)
            fig.add_trace(
                go.Bar(
                    y=ldf[cc],
                    x=ldf[chg],
                    orientation="h",
                    name="Decliners",
                    marker=dict(color=COLORS.get("danger", "#FF6B6B"), cornerradius=4),
                    hovertemplate="<b>%{y}</b><br>Change: %{x:.3f}<extra></extra>",
                )
            )

    _apply_common_layout(fig, "Biggest Movers", height)
    fig.update_xaxes(title_text="Score Change", zeroline=True, zerolinewidth=2, zerolinecolor="rgba(255,255,255,0.3)")
    fig.update_yaxes(tickfont=dict(size=11))
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    return fig


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _find_col(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    """Return the first column name in *candidates* that exists in *df*."""
    for c in candidates:
        if c in df.columns:
            return c
    # case-insensitive fallback
    lower_map = {col.lower(): col for col in df.columns}
    for c in candidates:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    return None


def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert a hex colour string to an ``rgba(...)`` CSS string."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    try:
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    except (ValueError, IndexError):
        return f"rgba(108,99,255,{alpha})"
    return f"rgba({r},{g},{b},{alpha})"
