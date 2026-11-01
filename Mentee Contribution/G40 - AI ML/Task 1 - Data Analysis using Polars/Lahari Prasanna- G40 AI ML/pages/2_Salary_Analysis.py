
import streamlit as st
import polars as pl
import plotly.express as px

st.set_page_config(page_title="Salary Analysis", page_icon="💰", layout="wide")
st.title("💰 Salary Analysis")
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
    df = df.filter(
        pl.col("salary_usd").is_not_null() &
        (pl.col("salary_usd") >= 1000) &
        (pl.col("salary_usd") <= 500000)
    )
    country_fix = {
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "Russian Federation": "Russia",
        "Iran, Islamic Republic of...": "Iran",
        "Hong Kong (S.A.R.)": "Hong Kong",
        "Republic of Korea": "South Korea",
    }
    ed_fix = {
        "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "Professional degree (JD, MD, etc.)",
        "Other doctoral degree (Ph.D., Ed.D., etc.)": "Doctoral degree (Ph.D., Ed.D., etc.)",
        "Master\u2019s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
        "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
        "Bachelor\u2019s degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
        "Bachelor's degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
        "Associate degree (A.A., A.S., etc.)": "Associate degree",
        "Some college/university study without earning a degree": "Some college, no degree",
        "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "Secondary school",
        "Primary/elementary school": "Primary school",
    }
    df = df.with_columns([
        pl.col("country").replace(country_fix),
        pl.col("ed_level").replace(ed_fix),
    ])
    return df

df = load_data()

# ---- Filters ----
st.sidebar.header("Filters")
years = sorted(df["survey_year"].unique().to_list())
selected_years = st.sidebar.multiselect("Select Years", years, default=years)
df = df.filter(pl.col("survey_year").is_in(selected_years))

# ---- Salary by Role ----
st.subheader("Median Salary by Developer Role")

role_salary = (
    df
    .filter(pl.col("dev_type").is_not_null())
    .select(["dev_type", "salary_usd"])
    .with_columns(pl.col("dev_type").str.split(";"))
    .explode("dev_type")
    .with_columns(pl.col("dev_type").str.strip_chars())
    .filter(pl.col("dev_type") != "")
    .group_by("dev_type")
    .agg([
        pl.col("salary_usd").median().alias("median_salary"),
        pl.col("salary_usd").count().alias("count")
    ])
    .filter(pl.col("count") >= 200)
    .sort("median_salary", descending=True)
    .head(15)
)

fig1 = px.bar(
    role_salary.to_pandas(),
    x="median_salary", y="dev_type",
    orientation="h",
    title="Median Salary by Developer Role (USD)",
    labels={"median_salary": "Median Salary (USD)", "dev_type": "Role"},
    color="median_salary",
    color_continuous_scale="Blues",
    text="median_salary"
)
fig1.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig1.update_layout(height=550, yaxis={"categoryorder": "total ascending"}, showlegend=False)
st.plotly_chart(fig1, use_container_width=True, config={"responsive": True})

# ---- Salary by Country ----
st.subheader("Median Salary by Country")

country_salary = (
    df
    .filter(pl.col("country").is_not_null())
    .group_by("country")
    .agg([
        pl.col("salary_usd").median().alias("median_salary"),
        pl.col("salary_usd").count().alias("count")
    ])
    .filter(pl.col("count") >= 200)
    .sort("median_salary", descending=True)
    .head(20)
)

fig2 = px.bar(
    country_salary.to_pandas(),
    x="median_salary", y="country",
    orientation="h",
    title="Median Salary by Country (USD)",
    labels={"median_salary": "Median Salary (USD)", "country": "Country"},
    color="median_salary",
    color_continuous_scale="Greens",
    text="median_salary"
)
fig2.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig2.update_layout(height=600, yaxis={"categoryorder": "total ascending"}, showlegend=False)
st.plotly_chart(fig2, use_container_width=True, config={"responsive": True})

# ---- Salary by Education ----
st.subheader("Median Salary by Education Level")

ed_salary = (
    df
    .filter(pl.col("ed_level").is_not_null())
    .group_by("ed_level")
    .agg([
        pl.col("salary_usd").median().alias("median_salary"),
        pl.col("salary_usd").count().alias("count")
    ])
    .filter(pl.col("count") >= 200)
    .sort("median_salary", descending=True)
)

fig3 = px.bar(
    ed_salary.to_pandas(),
    x="median_salary", y="ed_level",
    orientation="h",
    title="Median Salary by Education Level (USD)",
    labels={"median_salary": "Median Salary (USD)", "ed_level": "Education"},
    color="median_salary",
    color_continuous_scale="Purples",
    text="median_salary"
)
fig3.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig3.update_layout(height=450, yaxis={"categoryorder": "total ascending"}, showlegend=False)
st.plotly_chart(fig3, use_container_width=True, config={"responsive": True})

# ---- Salary by Experience ----
st.subheader("Median Salary by Experience Level")

exp_df = (
    df
    .with_columns(
        pl.col("years_code_pro")
        .str.replace("More than 50 years", "51")
        .str.replace("Less than 1 year", "0")
        .cast(pl.Float64, strict=False)
        .alias("experience")
    )
    .filter(
        pl.col("experience").is_not_null() &
        (pl.col("experience") >= 0) &
        (pl.col("experience") <= 50)
    )
    .with_columns(
        pl.when(pl.col("experience") < 1).then(pl.lit("Less than 1 year"))
        .when(pl.col("experience") < 3).then(pl.lit("1-2 years"))
        .when(pl.col("experience") < 6).then(pl.lit("3-5 years"))
        .when(pl.col("experience") < 11).then(pl.lit("6-10 years"))
        .when(pl.col("experience") < 21).then(pl.lit("11-20 years"))
        .otherwise(pl.lit("20+ years"))
        .alias("experience_band")
    )
    .group_by("experience_band")
    .agg([
        pl.col("salary_usd").median().alias("median_salary"),
        pl.col("salary_usd").count().alias("count")
    ])
)

band_order = ["Less than 1 year","1-2 years","3-5 years","6-10 years","11-20 years","20+ years"]
exp_df = exp_df.with_columns(
    pl.col("experience_band").cast(pl.Enum(band_order))
).sort("experience_band")

fig4 = px.bar(
    exp_df.to_pandas(),
    x="experience_band", y="median_salary",
    title="Salary Progression by Experience",
    labels={"experience_band": "Experience", "median_salary": "Median Salary (USD)"},
    color="median_salary",
    color_continuous_scale="Oranges",
    text="median_salary"
)
fig4.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig4.update_layout(height=450, showlegend=False)
st.plotly_chart(fig4, use_container_width=True, config={"responsive": True})
