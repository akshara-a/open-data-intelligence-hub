import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Programming Language Popularity Tracker",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("language_trends.csv")

df = load_data()

# --------------------------------------------------
# AUTO FIX COLUMN NAME
# --------------------------------------------------

if "count" not in df.columns:
    if "len" in df.columns:
        df = df.rename(columns={"len": "count"})
    else:
        st.error(
            f"Expected a column named 'count' or 'len'. Found: {list(df.columns)}"
        )
        st.stop()

# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

df = df.dropna(subset=["language"])

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📊 Programming Language Popularity Tracker")

st.markdown(
    """
    Analyze programming language popularity trends on GitHub
    using GH Archive Pull Request Events.
    """
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📌 Project Info")

st.sidebar.markdown("""
## Programming Language Popularity Tracker

Track how programming language popularity changes over time across GitHub using GH Archive data.

### 🔧 Technologies
- Python
- Polars
- Streamlit
- Pandas
- Plotly

### 📊 Data Source
GH Archive

### 📈 Analysis
- Pull Request Events
- Language Trend Analysis
- Popularity Ranking
- Market Share Analysis

### 🎯 Objective
Identify trending programming languages and analyze their popularity across GitHub repositories over time.

### 👨‍💻 Developed By
SANJANA MANTHENA
""")

st.sidebar.header("Filters")

languages = sorted(df["language"].unique())

selected_languages = st.sidebar.multiselect(
    "Select Languages",
    languages,
    default=languages[:5] if len(languages) >= 5 else languages
)

dates = sorted(df["date"].unique())

selected_dates = st.sidebar.multiselect(
    "Select Dates",
    dates,
    default=dates
)

filtered_df = df[
    (df["language"].isin(selected_languages))
    & (df["date"].isin(selected_dates))
]


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_languages = filtered_df["language"].nunique()
total_events = int(filtered_df["count"].sum())

language_totals = (
    filtered_df.groupby("language")["count"]
    .sum()
    .sort_values(ascending=False)
)

if len(language_totals) > 0:
    top_language = language_totals.index[0]
    top_count = int(language_totals.iloc[0])
else:
    top_language = "N/A"
    top_count = 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Languages", total_languages)
c2.metric("Total PR Events", f"{total_events:,}")
c3.metric("Top Language", top_language)
c4.metric("Top Language Events", f"{top_count:,}")

st.divider()

# --------------------------------------------------
# TREND CHART
# --------------------------------------------------

st.subheader("📈 Language Popularity Trend")

fig = px.line(
    filtered_df,
    x="date",
    y="count",
    color="language",
    markers=True
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 Top Languages")

    ranking = (
        filtered_df.groupby("language")["count"]
        .sum()
        .reset_index()
        .sort_values("count", ascending=False)
        .head(10)
    )

    bar_fig = px.bar(
        ranking,
        x="count",
        y="language",
        orientation="h"
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )

with col2:

    st.subheader("🥧 Language Market Share")

    pie_df = (
        filtered_df.groupby("language")["count"]
        .sum()
        .reset_index()
        .sort_values("count", ascending=False)
        .head(10)
    )

    pie_fig = px.pie(
        pie_df,
        values="count",
        names="language"
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

# --------------------------------------------------
# TABLE
# --------------------------------------------------

st.subheader("📋 Language Ranking")

table_df = (
    filtered_df.groupby("language")["count"]
    .sum()
    .reset_index()
    .sort_values("count", ascending=False)
)

table_df.insert(
    0,
    "Rank",
    range(1, len(table_df) + 1)
)

st.dataframe(
    table_df,
    use_container_width=True
)

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.subheader("⬇️ Download Dataset")

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="language_popularity.csv",
    mime="text/csv"
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.subheader("💡 Insights")

if len(table_df) >= 3:

    st.markdown(
        f"""
        - **{table_df.iloc[0]['language']}** is the most active language.
        - **{table_df.iloc[1]['language']}** is ranked second.
        - **{table_df.iloc[2]['language']}** is ranked third.
        - Total tracked languages: **{total_languages}**
        - Total Pull Request Events analyzed: **{total_events:,}**
        """
    )