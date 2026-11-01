import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Page config
st.set_page_config(page_title="Student Analysis - Student Enrollment Analytics", layout="wide")

# Theme colors
ACCENT  = "#4F6EF7"
WARNING = "#F59E0B"

# Title
st.title("👨‍🎓 Student Analysis")
st.write("Explore demographic and academic performance patterns across the student body.")

# Load data
df = load_data()

if df.empty:
    st.warning("No dataset loaded.")
else:
    # Filter columns side-by-side
    col_f1, col_f2 = st.columns(2)

    with col_f1:
        departments = ["All Departments"] + sorted(list(df.department.unique()))
        selected_dept = st.selectbox("Select Department", departments)
        
    with col_f2:
        years = ["All Years"] + ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
        selected_year = st.selectbox("Select Year", years)

    # Filtered dataset
    filtered = df.copy()
    if selected_dept != "All Departments":
        filtered = filtered[filtered.department == selected_dept]
    if selected_year != "All Years":
        filtered = filtered[filtered.year == selected_year]

    if filtered.empty:
        st.warning("No records match the current filters.")
    else:
        # Row 1 Charts
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("🎯 GPA by Department")
            fig_gpa = px.box(
                filtered, x="department", y="gpa", color="department",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template="plotly_white",
            )
            fig_gpa.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_tickangle=-30,
                xaxis_title="",
                yaxis_title="GPA",
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_gpa, use_container_width=True)

        with col_right:
            st.subheader("🎂 Age Distribution")
            fig_age = px.histogram(
                filtered, x="age", nbins=20, color_discrete_sequence=[ACCENT],
                template="plotly_white",
            )
            fig_age.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="Age",
                yaxis_title="Students",
                bargap=0.05,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_age, use_container_width=True)

        # Row 2 Charts
        col_left2, col_right2 = st.columns(2)

        with col_left2:
            st.subheader("📈 GPA vs Age (by Gender)")
            # Sample up to 500 for better Plotly rendering speed
            sample_df = filtered.sample(min(len(filtered), 500), random_state=1)
            fig_scatter = px.scatter(
                sample_df, x="age", y="gpa", color="gender",
                color_discrete_sequence=[ACCENT, "#A78BFA", WARNING, "#94A3B8"],
                opacity=0.65, template="plotly_white",
            )
            fig_scatter.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="Age",
                yaxis_title="GPA",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
                legend=dict(orientation="h", y=1.1, title=None),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_right2:
            st.subheader("📅 Students by Year")
            year_order = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
            yc = filtered.year.value_counts().reindex(year_order, fill_value=0).reset_index()
            yc.columns = ["year", "count"]
            
            fig_year = px.bar(
                yc, x="year", y="count", color="count",
                color_continuous_scale=["#C7D2FE", ACCENT], template="plotly_white",
            )
            fig_year.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="",
                yaxis_title="Students",
                coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_year, use_container_width=True)