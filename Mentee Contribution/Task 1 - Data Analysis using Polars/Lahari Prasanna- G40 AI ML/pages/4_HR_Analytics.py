
import streamlit as st
import polars as pl
import plotly.express as px

st.set_page_config(page_title="HR Analytics", page_icon="👥", layout="wide")
st.title("👥 HR Analytics Platform")
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
        "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
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

# ---- Tab Layout ----
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Geography",
    "🎓 Education",
    "💼 Employment",
    "📈 Developer Profiles"
])

# ---- Tab 1 Geography ----
with tab1:
    st.subheader("Developer Distribution by Country")

    country_dist = (
        df
        .filter(pl.col("country").is_not_null())
        .group_by("country")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )

    fig1 = px.choropleth(
        country_dist.to_pandas(),
        locations="country",
        locationmode="country names",
        color="count",
        title="Global Developer Distribution",
        color_continuous_scale="Blues",
        labels={"count": "Respondents"}
    )
    fig1.update_layout(height=500)
    st.plotly_chart(fig1, use_container_width=True, config={"responsive": True})

    st.subheader("Top 20 Countries by Developer Count")
    top_countries = country_dist.head(20)
    fig2 = px.bar(
        top_countries.to_pandas(),
        x="count", y="country",
        orientation="h",
        title="Top 20 Countries",
        labels={"count": "Respondents", "country": "Country"},
        color="count",
        color_continuous_scale="Blues",
        text="count"
    )
    fig2.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig2.update_layout(height=600, yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True, config={"responsive": True})

# ---- Tab 2 Education ----
with tab2:
    st.subheader("Education Level Distribution")

    ed_dist = (
        df
        .filter(pl.col("ed_level").is_not_null())
        .group_by("ed_level")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )

    fig3 = px.pie(
        ed_dist.to_pandas(),
        names="ed_level",
        values="count",
        title="Education Level Distribution",
        hole=0.4
    )
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True, config={"responsive": True})

    fig4 = px.bar(
        ed_dist.to_pandas(),
        x="count", y="ed_level",
        orientation="h",
        title="Education Level Counts",
        labels={"count": "Respondents", "ed_level": "Education"},
        color="count",
        color_continuous_scale="Purples",
        text="count"
    )
    fig4.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig4.update_layout(height=450, yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True, config={"responsive": True})

# ---- Tab 3 Employment ----
with tab3:
    st.subheader("Employment Type Distribution")

    emp_dist = (
        df
        .filter(pl.col("employment").is_not_null())
        .with_columns(pl.col("employment").str.split(";"))
        .explode("employment")
        .with_columns(pl.col("employment").str.strip_chars())
        .filter(pl.col("employment") != "")
        .group_by("employment")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )

    fig5 = px.pie(
        emp_dist.to_pandas(),
        names="employment",
        values="count",
        title="Employment Type Distribution",
        hole=0.4
    )
    fig5.update_layout(height=500)
    st.plotly_chart(fig5, use_container_width=True, config={"responsive": True})

    if "remote_work" in df.columns:
        st.subheader("Remote Work Distribution")
        remote_dist = (
            df
            .filter(pl.col("remote_work").is_not_null())
            .group_by("remote_work")
            .agg(pl.len().alias("count"))
            .sort("count", descending=True)
        )
        fig6 = px.bar(
            remote_dist.to_pandas(),
            x="remote_work", y="count",
            title="Remote Work Preferences",
            labels={"remote_work": "Work Style", "count": "Respondents"},
            color="count",
            color_continuous_scale="Greens",
            text="count"
        )
        fig6.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig6.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig6, use_container_width=True, config={"responsive": True})

# ---- Tab 4 Developer Profiles ----
with tab4:
    st.subheader("Developer Role Distribution")

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
        .head(20)
    )

    fig7 = px.bar(
        role_dist.to_pandas(),
        x="count", y="dev_type",
        orientation="h",
        title="Top 20 Developer Roles",
        labels={"count": "Respondents", "dev_type": "Role"},
        color="count",
        color_continuous_scale="Reds",
        text="count"
    )
    fig7.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig7.update_layout(height=600, yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig7, use_container_width=True, config={"responsive": True})

    st.subheader("Organisation Size Distribution")
    org_dist = (
        df
        .filter(pl.col("org_size").is_not_null())
        .group_by("org_size")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )
    fig8 = px.pie(
        org_dist.to_pandas(),
        names="org_size",
        values="count",
        title="Organisation Size Distribution",
        hole=0.4
    )
    fig8.update_layout(height=500)
    st.plotly_chart(fig8, use_container_width=True, config={"responsive": True})
