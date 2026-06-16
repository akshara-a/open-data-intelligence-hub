import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Page config
st.set_page_config(page_title="Course Analysis - Student Enrollment Analytics", layout="wide")

# Title
st.title("📚 Course Analysis")
st.write("Popularity, GPA performance, and credit load across all courses.")

# Load data
df = load_data()

if df.empty:
    st.warning("No dataset loaded.")
else:
    # Filter
    dept_options = ["All Departments"] + sorted(list(df.department.unique()))
    selected_dept = st.selectbox("Select Department", dept_options)

    # Filtered dataset
    filtered = df.copy()
    if selected_dept != "All Departments":
        filtered = filtered[filtered.department == selected_dept]

    if filtered.empty:
        st.warning(f"No records found for department: {selected_dept}")
    else:
        # Row 1 Charts
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("🏆 Top 15 Most Popular Courses")
            top_courses = filtered.course.value_counts().head(15).reset_index()
            top_courses.columns = ["course", "count"]
            top_courses = top_courses.sort_values("count", ascending=True)
            fig_top = px.bar(
                top_courses, x="count", y="course", orientation="h",
                color="count", color_continuous_scale=["#C7D2FE", "#4F6EF7"],
                template="plotly_white",
            )
            fig_top.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                coloraxis_showscale=False,
                xaxis_title="Enrollments",
                yaxis_title="",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_top, use_container_width=True)

        with col_right:
            st.subheader("💳 Credits Distribution")
            credits_counts = filtered.credits.value_counts().reset_index()
            credits_counts.columns = ["credits", "count"]
            fig_credits = px.pie(
                credits_counts, names="credits", values="count", hole=0.5,
                color_discrete_sequence=["#4F6EF7", "#22C55E", "#F59E0B", "#EF4444", "#A78BFA"],
                template="plotly_white",
            )
            fig_credits.update_traces(textposition="outside", textinfo="percent+label")
            fig_credits.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
                annotations=[dict(text="Credits", x=0.5, y=0.5, font_size=14, showarrow=False)],
            )
            st.plotly_chart(fig_credits, use_container_width=True)

        # Row 2 Charts
        col_left2, col_right2 = st.columns(2)

        with col_left2:
            st.subheader("🎯 Average GPA per Course (Top 15)")
            top_course_names = filtered.course.value_counts().head(15).index
            gpa_c = (
                filtered[filtered.course.isin(top_course_names)]
                .groupby("course")["gpa"]
                .mean()
                .reset_index()
                .sort_values("gpa", ascending=True)
            )
            fig_gpa = px.bar(
                gpa_c, x="gpa", y="course", orientation="h",
                color="gpa", color_continuous_scale=["#FEF3C7", "#F59E0B", "#22C55E"],
                range_color=[2.5, 4.0], template="plotly_white",
            )
            fig_gpa.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                coloraxis_showscale=False,
                xaxis_title="Avg GPA",
                yaxis_title="",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_gpa, use_container_width=True)

        with col_right2:
            st.subheader("🏢 Enrollment Status by Department")
            # If the user filtered by a single department, grouping by department will just show one.
            # That's fine, it shows the status stack for that department.
            sd = (
                filtered.groupby(["department", "enrollment_status"])
                .size()
                .reset_index(name="count")
            )
            color_map = {"Enrolled": "#4F6EF7", "Completed": "#22C55E", "Waitlisted": "#F59E0B", "Dropped": "#EF4444"}
            fig_status = px.bar(
                sd, x="department", y="count", color="enrollment_status",
                color_discrete_map=color_map, barmode="stack", template="plotly_white",
            )
            fig_status.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="",
                yaxis_title="Students",
                xaxis_tickangle=-30,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
                legend=dict(orientation="h", y=1.1, title=None),
            )
            st.plotly_chart(fig_status, use_container_width=True)
