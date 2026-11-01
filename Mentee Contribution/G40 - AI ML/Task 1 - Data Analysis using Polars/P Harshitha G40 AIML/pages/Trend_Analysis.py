import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Page config
st.set_page_config(page_title="Trend Analysis - Student Enrollment Analytics", layout="wide")

# Theme colors
ACCENT  = "#4F6EF7"
SUCCESS = "#22C55E"
DANGER  = "#EF4444"

# Title
st.title("📅 Trend Analysis")
st.write("How enrollment numbers, GPA, and demographics have shifted over time.")

# Load data
df = load_data()

if df.empty:
    st.warning("No dataset loaded.")
else:
    # Filter
    departments = ["All Departments"] + sorted(list(df.department.unique()))
    selected_dept = st.selectbox("Select Department", departments)

    # Filtered dataset
    filtered = df.copy()
    if selected_dept != "All Departments":
        filtered = filtered[filtered.department == selected_dept]

    if filtered.empty:
        st.warning("No records match the current filters.")
    else:
        # Row 1 Charts (Full width for Monthly Enrollment Trend)
        st.subheader("📈 Monthly Enrollment Trend")
        tl = filtered.copy()
        tl["month"] = tl.enrollment_date.dt.to_period("M").astype(str)
        tl_g = tl.groupby("month").size().reset_index(name="count").sort_values("month")
        
        fig_monthly = px.line(
            tl_g, x="month", y="count", markers=True,
            color_discrete_sequence=[ACCENT], template="plotly_white",
        )
        fig_monthly.update_traces(line_width=2.5)
        fig_monthly.update_layout(
            margin=dict(l=10, r=10, t=10, b=40),
            xaxis_title="",
            yaxis_title="New Enrollments",
            xaxis_tickangle=-45,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 2 Charts (Side-by-side)
        col_left2, col_right2 = st.columns(2)

        sem_order = ["Spring 2023", "Fall 2023", "Spring 2024", "Fall 2024", "Spring 2025"]

        with col_left2:
            st.subheader("🎓 Average GPA per Semester")
            gpa_s = (
                filtered.groupby("semester")["gpa"]
                .mean()
                .reindex(sem_order)
                .reset_index()
            )
            gpa_s.columns = ["semester", "avg_gpa"]
            
            fig_gpa_sem = px.line(
                gpa_s, x="semester", y="avg_gpa", markers=True,
                color_discrete_sequence=[SUCCESS], template="plotly_white",
            )
            fig_gpa_sem.update_traces(line_width=2.5)
            fig_gpa_sem.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="",
                yaxis_title="Avg GPA",
                yaxis=dict(range=[2.8, 3.5]),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_gpa_sem, use_container_width=True)

        with col_right2:
            st.subheader("❌ Drop Rate per Semester")
            # Calculate drop rate as percent
            drop = (
                filtered.groupby("semester")
                .apply(lambda x: (x.enrollment_status == "Dropped").mean() * 100)
                .reindex(sem_order, fill_value=0)
                .reset_index()
            )
            drop.columns = ["semester", "drop_rate"]
            
            fig_drop_sem = px.bar(
                drop, x="semester", y="drop_rate",
                color="drop_rate", color_continuous_scale=["#FEF3C7", DANGER],
                template="plotly_white",
            )
            fig_drop_sem.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="",
                yaxis_title="Drop Rate (%)",
                coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_drop_sem, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 3 (Full width for Enrollment by Department per Semester)
        st.subheader("🏢 Enrollment by Department per Semester")
        dept_trend = (
            filtered.groupby(["semester", "department"])
            .size()
            .reset_index(name="count")
        )
        # Ensure correct semester ordering
        dept_trend["semester"] = pd.Categorical(dept_trend["semester"], categories=sem_order, ordered=True)
        dept_trend = dept_trend.sort_values("semester")
        
        fig_dept_sem = px.line(
            dept_trend, x="semester", y="count", color="department",
            markers=True, template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
        fig_dept_sem.update_traces(line_width=2)
        fig_dept_sem.update_layout(
            margin=dict(l=10, r=10, t=10, b=40),
            xaxis_title="",
            yaxis_title="Students",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            legend=dict(orientation="h", y=-0.2, title=None),
        )
        st.plotly_chart(fig_dept_sem, use_container_width=True)