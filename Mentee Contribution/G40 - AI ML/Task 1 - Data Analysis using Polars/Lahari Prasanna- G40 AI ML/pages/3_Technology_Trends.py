
import streamlit as st
import polars as pl
import plotly.express as px

st.set_page_config(page_title="Technology Trends", page_icon="🛠️", layout="wide")
st.title("🛠️ Technology Trends")
st.markdown("---")

@st.cache_data
def load_data():
    df = pl.read_parquet("data/master_survey.parquet")
    na_values = ["NA", "na", "N/A", "n/a", "", "nan", "NaN", "NULL", "null", "None"]
    string_cols = [col for col in df.columns if df[col].dtype == pl.Utf8]
    df = df.with_columns([
        pl.when(pl.col(col).is_in(na_values))
        .then(None)
        .otherwise(pl.col(col))
        .alias(col)
        for col in string_cols
    ])
    return df

df = load_data()

# ---- Filters ----
st.sidebar.header("Filters")
years = sorted(df["survey_year"].unique().to_list())
selected_years = st.sidebar.multiselect("Select Years", years, default=years)
df = df.filter(pl.col("survey_year").is_in(selected_years))

# ---- Helper Function ----
def get_trend(df, col):
    yearly_total = (
        df.filter(pl.col(col).is_not_null())
        .group_by("survey_year")
        .agg(pl.len().alias("total"))
    )
    trend = (
        df.filter(pl.col(col).is_not_null())
        .select(["survey_year", col])
        .with_columns(pl.col(col).str.split(";"))
        .explode(col)
        .with_columns(pl.col(col).str.strip_chars().alias("item"))
        .filter(pl.col("item") != "")
        .group_by(["survey_year", "item"])
        .agg(pl.len().alias("count"))
        .join(yearly_total, on="survey_year")
        .with_columns(
            (pl.col("count") / pl.col("total") * 100)
            .round(1).alias("pct")
        )
        .sort(["survey_year", "count"], descending=[False, True])
    )
    return trend

# ---- Tab Layout ----
tab1, tab2, tab3 = st.tabs(["💬 Languages", "🗄️ Databases", "🌐 Frameworks"])

# ---- Tab 1 Languages ----
with tab1:
    st.subheader("Programming Language Trends (2020–2025)")

    lang_trend = get_trend(df, "language_worked_with")

    top_langs = (
        lang_trend
        .group_by("item")
        .agg(pl.col("count").sum())
        .sort("count", descending=True)
        .head(10)["item"].to_list()
    )

    lang_filtered = lang_trend.filter(pl.col("item").is_in(top_langs))

    fig1 = px.line(
        lang_filtered.to_pandas(),
        x="survey_year", y="pct",
        color="item",
        markers=True,
        title="Top 10 Programming Languages Over Time",
        labels={"survey_year": "Year", "pct": "% of Respondents", "item": "Language"}
    )
    fig1.update_layout(height=500)
    st.plotly_chart(fig1, use_container_width=True, config={"responsive": True})

    st.subheader("Top Languages in Latest Year")
    latest_year = max(selected_years)
    top_latest = (
        lang_trend
        .filter(pl.col("survey_year") == latest_year)
        .head(15)
    )
    fig2 = px.bar(
        top_latest.to_pandas(),
        x="pct", y="item",
        orientation="h",
        title=f"Top Languages in {latest_year}",
        labels={"pct": "% of Respondents", "item": "Language"},
        color="pct",
        color_continuous_scale="Blues",
        text="pct"
    )
    fig2.update_traces(texttemplate="%{text}%", textposition="outside")
    fig2.update_layout(height=500, yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True, config={"responsive": True})

# ---- Tab 2 Databases ----
with tab2:
    st.subheader("Database Trends (2020–2025)")

    db_trend = get_trend(df, "database_worked_with")

    top_dbs = (
        db_trend
        .group_by("item")
        .agg(pl.col("count").sum())
        .sort("count", descending=True)
        .head(10)["item"].to_list()
    )

    db_filtered = db_trend.filter(pl.col("item").is_in(top_dbs))

    fig3 = px.line(
        db_filtered.to_pandas(),
        x="survey_year", y="pct",
        color="item",
        markers=True,
        title="Top 10 Databases Over Time",
        labels={"survey_year": "Year", "pct": "% of Respondents", "item": "Database"}
    )
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True, config={"responsive": True})

    st.subheader("Top Databases in Latest Year")
    top_db_latest = (
        db_trend
        .filter(pl.col("survey_year") == latest_year)
        .head(15)
    )
    fig4 = px.bar(
        top_db_latest.to_pandas(),
        x="pct", y="item",
        orientation="h",
        title=f"Top Databases in {latest_year}",
        labels={"pct": "% of Respondents", "item": "Database"},
        color="pct",
        color_continuous_scale="Greens",
        text="pct"
    )
    fig4.update_traces(texttemplate="%{text}%", textposition="outside")
    fig4.update_layout(height=500, yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True, config={"responsive": True})

# ---- Tab 3 Frameworks ----
with tab3:
    st.subheader("Web Framework Trends (2020–2025)")

    web_trend = get_trend(df, "webframe_worked_with")

    top_webs = (
        web_trend
        .group_by("item")
        .agg(pl.col("count").sum())
        .sort("count", descending=True)
        .head(10)["item"].to_list()
    )

    web_filtered = web_trend.filter(pl.col("item").is_in(top_webs))

    fig5 = px.line(
        web_filtered.to_pandas(),
        x="survey_year", y="pct",
        color="item",
        markers=True,
        title="Top 10 Web Frameworks Over Time",
        labels={"survey_year": "Year", "pct": "% of Respondents", "item": "Framework"}
    )
    fig5.update_layout(height=500)
    st.plotly_chart(fig5, use_container_width=True, config={"responsive": True})

    st.subheader("Top Frameworks in Latest Year")
    top_web_latest = (
        web_trend
        .filter(pl.col("survey_year") == latest_year)
        .head(15)
    )
    fig6 = px.bar(
        top_web_latest.to_pandas(),
        x="pct", y="item",
        orientation="h",
        title=f"Top Frameworks in {latest_year}",
        labels={"pct": "% of Respondents", "item": "Framework"},
        color="pct",
        color_continuous_scale="Oranges",
        text="pct"
    )
    fig6.update_traces(texttemplate="%{text}%", textposition="outside")
    fig6.update_layout(height=500, yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True, config={"responsive": True})
