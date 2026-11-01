"""
Configuration module for Social Progress Analytics Dashboard.

Contains color palettes, chart themes, column mappings, CSS generators,
and formatting utilities for a premium dark-themed analytics experience.
"""

from __future__ import annotations

# =============================================================================
# Color Palette — Premium Dark Theme
# =============================================================================

COLORS: dict[str, str] = {
    # Primary backgrounds
    "bg_primary": "#0a0e1a",
    "bg_secondary": "#111827",
    "bg_card": "rgba(17, 24, 39, 0.65)",
    "bg_card_solid": "#111827",
    "bg_hover": "#1e293b",
    # Accent / brand
    "accent_blue": "#3b82f6",
    "accent_teal": "#14b8a6",
    "accent_gold": "#f59e0b",
    "accent_coral": "#f472b6",
    "accent_purple": "#a78bfa",
    "accent_emerald": "#10b981",
    "accent_cyan": "#22d3ee",
    "accent_rose": "#fb7185",
    # Text
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    # Borders & dividers
    "border": "rgba(148, 163, 184, 0.12)",
    "border_hover": "rgba(148, 163, 184, 0.25)",
    # Gradients (start, end)
    "gradient_start": "#0a0e1a",
    "gradient_end": "#1a1a2e",
    # Status
    "positive": "#10b981",
    "negative": "#ef4444",
    "neutral": "#94a3b8",
}

# =============================================================================
# Factor Column Mapping
# =============================================================================

FACTOR_COLUMNS: dict[str, str] = {
    "GDP": "Explained by: Log GDP per capita",
    "Social Support": "Explained by: Social support",
    "Health": "Explained by: Healthy life expectancy",
    "Freedom": "Explained by: Freedom to make life choices",
    "Generosity": "Explained by: Generosity",
    "Corruption": "Explained by: Perceptions of corruption",
    "Dystopia + Residual": "Dystopia + residual",
}

# Reverse mapping (full column name → short name)
FACTOR_COLUMNS_REVERSE: dict[str, str] = {v: k for k, v in FACTOR_COLUMNS.items()}

# =============================================================================
# Factor Colors — One distinct color per factor
# =============================================================================

FACTOR_COLORS: dict[str, str] = {
    "GDP": "#3b82f6",                  # Blue
    "Social Support": "#14b8a6",       # Teal
    "Health": "#10b981",               # Emerald
    "Freedom": "#f59e0b",              # Gold
    "Generosity": "#a78bfa",           # Purple
    "Corruption": "#f472b6",           # Coral / Pink
    "Dystopia + Residual": "#64748b",  # Slate (muted)
}

# Ordered list of factor short names for consistent iteration
FACTOR_ORDER: list[str] = [
    "GDP",
    "Social Support",
    "Health",
    "Freedom",
    "Generosity",
    "Corruption",
    "Dystopia + Residual",
]

# =============================================================================
# Plotly Chart Theme
# =============================================================================

CHART_FONT_FAMILY: str = "'Inter', 'Segoe UI', system-ui, sans-serif"

PLOTLY_LAYOUT_DEFAULTS: dict = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": CHART_FONT_FAMILY,
        "color": COLORS["text_secondary"],
        "size": 13,
    },
    "title": {
        "font": {
            "family": CHART_FONT_FAMILY,
            "size": 18,
            "color": COLORS["text_primary"],
        },
        "x": 0.0,
        "xanchor": "left",
    },
    "legend": {
        "font": {"size": 12, "color": COLORS["text_secondary"]},
        "bgcolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
    },
    "margin": {"l": 60, "r": 30, "t": 60, "b": 50},
    "hoverlabel": {
        "bgcolor": COLORS["bg_secondary"],
        "font_size": 13,
        "font_family": CHART_FONT_FAMILY,
        "bordercolor": COLORS["border"],
    },
    "xaxis": {
        "gridcolor": "rgba(148,163,184,0.08)",
        "zerolinecolor": "rgba(148,163,184,0.12)",
        "title_font": {"size": 13, "color": COLORS["text_secondary"]},
        "tickfont": {"size": 11, "color": COLORS["text_muted"]},
    },
    "yaxis": {
        "gridcolor": "rgba(148,163,184,0.08)",
        "zerolinecolor": "rgba(148,163,184,0.12)",
        "title_font": {"size": 13, "color": COLORS["text_secondary"]},
        "tickfont": {"size": 11, "color": COLORS["text_muted"]},
    },
}

# Default color sequence for multi-series charts
PLOTLY_COLOR_SEQUENCE: list[str] = [
    COLORS["accent_blue"],
    COLORS["accent_teal"],
    COLORS["accent_gold"],
    COLORS["accent_coral"],
    COLORS["accent_purple"],
    COLORS["accent_emerald"],
    COLORS["accent_cyan"],
    COLORS["accent_rose"],
]

# =============================================================================
# App Configuration Constants
# =============================================================================

APP_TITLE: str = "Social Progress Analytics"
APP_SUBTITLE: str = "World Happiness Report — Interactive Explorer"
APP_PAGE_ICON: str = "🌍"
APP_LAYOUT: str = "wide"
APP_INITIAL_SIDEBAR_STATE: str = "expanded"
APP_DESCRIPTION: str = (
    "Explore the factors that drive national well-being across the globe, "
    "powered by data from the World Happiness Report."
)

DEFAULT_TOP_N: int = 20
SCORE_DECIMAL_PLACES: int = 3


# =============================================================================
# Number Formatting Helpers
# =============================================================================


def format_number(value: float, decimals: int = 2) -> str:
    """Format a numeric value with thousands separator and fixed decimals.

    Args:
        value: The number to format.
        decimals: Number of decimal places (default 2).

    Returns:
        Formatted string, e.g. ``"1,234.56"``.
    """
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.{decimals}f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:,.{decimals}f}K"
    return f"{value:,.{decimals}f}"


def format_rank(rank: int | float) -> str:
    """Return an ordinal string for a rank (1 → '1st', 2 → '2nd', …).

    Args:
        rank: Integer rank value.

    Returns:
        Ordinal string representation.
    """
    rank = int(rank)
    if 11 <= (rank % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(rank % 10, "th")
    return f"{rank}{suffix}"


def format_score(score: float, decimals: int = SCORE_DECIMAL_PLACES) -> str:
    """Format a happiness / life-evaluation score.

    Args:
        score: The score to format.
        decimals: Decimal places (default from config).

    Returns:
        Fixed-decimal string, e.g. ``"7.842"``.
    """
    return f"{score:.{decimals}f}"


# =============================================================================
# KPI Card CSS Generator (Glassmorphism)
# =============================================================================


def kpi_card_html(
    title: str,
    value: str,
    delta: str | None = None,
    delta_color: str | None = None,
    icon: str = "",
) -> str:
    """Generate an HTML/CSS snippet for a glassmorphism KPI metric card.

    Args:
        title: Card label (e.g. "Happiness Score").
        value: Primary display value (already formatted).
        delta: Optional delta/change string (e.g. "+0.12").
        delta_color: CSS color for the delta text.
        icon: Optional emoji or icon character.

    Returns:
        Raw HTML string safe for ``st.markdown(…, unsafe_allow_html=True)``.
    """
    delta_color = delta_color or COLORS["text_secondary"]
    delta_html = (
        f'<span style="font-size:0.85rem;color:{delta_color};'
        f'font-weight:500;">{delta}</span>'
        if delta
        else ""
    )
    icon_html = (
        f'<span style="font-size:1.6rem;margin-right:6px;">{icon}</span>'
        if icon
        else ""
    )

    return f"""
    <div style="
        background: {COLORS['bg_card']};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    " onmouseenter="this.style.borderColor='{COLORS['border_hover']}';this.style.transform='translateY(-2px)'"
       onmouseleave="this.style.borderColor='{COLORS['border']}';this.style.transform='translateY(0)'">
        <div style="display:flex;align-items:center;margin-bottom:0.35rem;">
            {icon_html}
            <span style="font-size:0.82rem;color:{COLORS['text_muted']};
                         text-transform:uppercase;letter-spacing:0.06em;
                         font-weight:600;">{title}</span>
        </div>
        <div style="font-size:1.85rem;font-weight:700;color:{COLORS['text_primary']};
                     line-height:1.2;margin-bottom:0.2rem;">
            {value}
        </div>
        {delta_html}
    </div>
    """


# =============================================================================
# Global Custom CSS Generator
# =============================================================================


def get_custom_css() -> str:
    """Return a ``<style>`` block with the full premium dark-theme CSS.

    Includes:
    - Google Fonts import (Inter)
    - Gradient page background
    - Card / glass-panel styling
    - Custom scrollbar
    - Streamlit element overrides (sidebar, metrics, buttons, tabs, etc.)

    Returns:
        A complete ``<style>…</style>`` string for ``st.markdown``.
    """
    return f"""
    <style>
        /* ── Google Fonts ─────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Root / Page ──────────────────────────────────────── */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
            color: {COLORS['text_primary']};
        }}

        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(145deg, {COLORS['gradient_start']} 0%,
                                                 {COLORS['gradient_end']} 100%);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        /* ── Sidebar ──────────────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background: {COLORS['bg_secondary']};
            border-right: 1px solid {COLORS['border']};
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: {COLORS['text_secondary']};
        }}

        /* ── Glass Card Utility ───────────────────────────────── */
        .glass-card {{
            background: {COLORS['bg_card']};
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: border-color 0.2s ease;
        }}
        .glass-card:hover {{
            border-color: {COLORS['border_hover']};
        }}

        /* ── Plotly Charts Container ──────────────────────────── */
        [data-testid="stPlotlyChart"] {{
            background: {COLORS['bg_card']};
            backdrop-filter: blur(12px);
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 0.5rem;
        }}

        /* ── Streamlit Metric Override ────────────────────────── */
        [data-testid="stMetric"] {{
            background: {COLORS['bg_card']};
            backdrop-filter: blur(16px);
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 1rem 1.25rem;
        }}
        [data-testid="stMetricLabel"] p {{
            color: {COLORS['text_muted']} !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.78rem !important;
            letter-spacing: 0.05em;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLORS['text_primary']} !important;
            font-weight: 700 !important;
        }}
        [data-testid="stMetricDelta"] {{
            font-weight: 500 !important;
        }}

        /* ── Buttons ──────────────────────────────────────────── */
        .stButton > button {{
            background: linear-gradient(135deg, {COLORS['accent_blue']}, {COLORS['accent_teal']});
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.25rem;
            transition: opacity 0.2s ease, transform 0.15s ease;
        }}
        .stButton > button:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
        }}

        /* ── Tabs ─────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            background: transparent;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            color: {COLORS['text_secondary']};
            font-weight: 500;
            padding: 0.5rem 1rem;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {COLORS['accent_blue']}, {COLORS['accent_teal']}) !important;
            color: white !important;
            border-color: transparent !important;
        }}

        /* ── Select / Multiselect Boxes ───────────────────────── */
        [data-testid="stSelectbox"],
        [data-testid="stMultiSelect"] {{
            color: {COLORS['text_primary']};
        }}

        /* ── Expander ─────────────────────────────────────────── */
        [data-testid="stExpander"] {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
        }}

        /* ── Divider ──────────────────────────────────────────── */
        hr {{
            border-color: {COLORS['border']} !important;
        }}

        /* ── Custom Scrollbar ─────────────────────────────────── */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {COLORS['bg_primary']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['text_muted']};
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['text_secondary']};
        }}

        /* ── Misc ─────────────────────────────────────────────── */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* Hide Streamlit footer & menu */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """
