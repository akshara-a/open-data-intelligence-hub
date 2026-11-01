
import streamlit as st
import polars as pl
import plotly.express as px

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
st.title("📊 Overview — Key Metrics")
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
    df = df.with_columns(
        pl.col("salary_usd").cast(pl.Float64, strict=False)
    )
    return df

df = load_data()

# ---- Filters ----
st.sidebar.header("Filters")
years = sorted(df["survey_year"].unique().to_list())
selected_years = st.sidebar.multiselect("Select Years", years, default=years)
df = df.filter(pl.col("survey_year").is_in(selected_years))

# ---- KPI Cards ----
salary_df = df.filter(
    pl.col("salary_usd").is_not_null() &
    (pl.col("salary_usd") >= 1000) &
    (pl.col("salary_usd") <= 500000)
)

total_responses  = df.shape[0]
total_countries  = df.filter(pl.col("country").is_not_null())["country"].n_unique()
median_salary    = salary_df["salary_usd"].median()
total_roles      = (
    df.filter(pl.col("dev_type").is_not_null())
    .select(pl.col("dev_type").str.split(";").explode())
    .unique().shape[0]
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Responses",    f"{total_responses:,}")
col2.metric("Countries",          f"{total_countries}")
col3.metric("Median Salary",      f"${median_salary:,.0f}")
col4.metric("Unique Roles",       f"{total_roles}")

st.markdown("---")

# ---- Responses Per Year ----
st.subheader("Survey Responses Per Year")

yearly_counts = (
    df
    .group_by("survey_year")
    .agg(pl.len().alias("count"))
    .sort("survey_year")
)

fig1 = px.bar(
    yearly_counts.to_pandas(),
    x="survey_year", y="count",
    title="Total Respondents Per Year",
    labels={"survey_year": "Year", "count": "Respondents"},
    color="count",
    color_continuous_scale="Blues",
    text="count"
)
fig1.update_traces(texttemplate="%{text:,}", textposition="outside")
fig1.update_layout(height=400, showlegend=False)
st.plotly_chart(fig1, use_container_width=True, config={"responsive": True})

# ---- Median Salary Per Year ----
st.subheader("Global Median Salary Trend")

salary_trend = (
    salary_df
    .group_by("survey_year")
    .agg(pl.col("salary_usd").median().alias("median_salary"))
    .sort("survey_year")
)

fig2 = px.line(
    salary_trend.to_pandas(),
    x="survey_year", y="median_salary",
    title="Global Median Salary Over Time",
    labels={"survey_year": "Year", "median_salary": "Median Salary (USD)"},
    markers=True
)
fig2.update_layout(height=400)
st.plotly_chart(fig2, use_container_width=True, config={"responsive": True})

# ---- Top 10 Countries by Respondents ----
st.subheader("Top 10 Countries by Respondents")

top_countries = (
    df
    .filter(pl.col("country").is_not_null())
    .group_by("country")
    .agg(pl.len().alias("count"))
    .sort("count", descending=True)
    .head(10)
)

fig3 = px.bar(
    top_countries.to_pandas(),
    x="count", y="country",
    orientation="h",
    title="Top 10 Countries",
    labels={"count": "Respondents", "country": "Country"},
    color="count",
    color_continuous_scale="Greens",
    text="count"
)
fig3.update_traces(texttemplate="%{text:,}", textposition="outside")
fig3.update_layout(height=450, yaxis={"categoryorder": "total ascending"}, showlegend=False)
st.plotly_chart(fig3, use_container_width=True, config={"responsive": True})

# ---- Top 10 Roles ----
st.subheader("Top 10 Developer Roles")

role_dist = (
    df
    .filter(pl.col("dev_type").is_not_null())
    .select("dev_type")
    .with_columns(pl.col("dev_type").str.split(";"))
    .explode("dev_type")
    .with_columns(pl.col("dev_type").str.strip_chars())
    .filter(pl.col("dev_type") != "")
    .group_by("dev_type")
    .agg(pl.len().alias("count"))
    .sort("count", descending=True)
    .head(10)
)

fig4 = px.bar(
    role_dist.to_pandas(),
    x="count", y="dev_type",
    orientation="h",
    title="Top 10 Developer Roles",
    labels={"count": "Respondents", "dev_type": "Role"},
    color="count",
    color_continuous_scale="Reds",
    text="count"
)
fig4.update_traces(texttemplate="%{text:,}", textposition="outside")
fig4.update_layout(height=450, yaxis={"categoryorder": "total ascending"}, showlegend=False)
st.plotly_chart(fig4, use_container_width=True, config={"responsive": True})
