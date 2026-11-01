import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

# Page config
st.set_page_config(page_title="Enrollment Analysis - Student Enrollment Analytics", layout="wide")

# Theme colors
ACCENT  = "#4F6EF7"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER  = "#EF4444"

# Title
st.title("📈 Enrollment Analysis")
st.write("Semester-by-semester enrollment trends, status breakdown, and fee summary.")

# Load data
df = load_data()

if df.empty:
    st.warning("No dataset loaded.")
else:
    # Filter columns side-by-side
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        semesters = ["All Semesters"] + sorted(list(df.semester.unique()))
        selected_sem = st.selectbox("Select Semester", semesters)
        
    with col_f2:
        statuses = ["All Statuses"] + sorted(list(df.enrollment_status.unique()))
        selected_status = st.selectbox("Select Status", statuses)

    # Filtered dataset
    filtered = df.copy()
    if selected_sem != "All Semesters":
        filtered = filtered[filtered.semester == selected_sem]
    if selected_status != "All Statuses":
        filtered = filtered[filtered.enrollment_status == selected_status]

    if filtered.empty:
        st.warning("No records match the current filters.")
    else:
        # Row 1 Charts
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📊 Enrollments per Semester")
            sem_order = ["Spring 2023", "Fall 2023", "Spring 2024", "Fall 2024", "Spring 2025"]
            # To get counts, count across the filtered dataset
            sc = filtered.semester.value_counts().reindex(sem_order, fill_value=0).reset_index()
            sc.columns = ["semester", "count"]
            
            fig_sem = px.bar(
                sc, x="semester", y="count", color="count",
                color_continuous_scale=["#C7D2FE", ACCENT], template="plotly_white",
            )
            fig_sem.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="",
                yaxis_title="Students",
                coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_sem, use_container_width=True)

        with col_right:
            st.subheader("🍕 Status Breakdown")
            sc2 = filtered.enrollment_status.value_counts().reset_index()
            sc2.columns = ["status", "count"]
            cmap = {"Enrolled": ACCENT, "Completed": SUCCESS, "Waitlisted": WARNING, "Dropped": DANGER}
            
            fig_status = px.pie(
                sc2, names="status", values="count", hole=0.55,
                color="status", color_discrete_map=cmap, template="plotly_white",
            )
            fig_status.update_traces(textposition="outside", textinfo="percent+label")
            fig_status.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_status, use_container_width=True)

        # Row 2 Charts
        col_left2, col_right2 = st.columns(2)

        with col_left2:
            st.subheader("💰 Tuition vs Scholarship by Department")
            fee = (
                filtered.groupby("department")
                .agg(tuition=("tuition_fee", "mean"), scholarship=("scholarship_amount", "mean"))
                .reset_index()
                .sort_values("tuition", ascending=False)
            )
            fig_fee = go.Figure([
                go.Bar(name="Avg Tuition",     x=fee.department, y=fee.tuition,     marker_color=ACCENT,   opacity=0.85),
                go.Bar(name="Avg Scholarship", x=fee.department, y=fee.scholarship, marker_color=SUCCESS, opacity=0.85),
            ])
            fig_fee.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                barmode="group",
                xaxis_tickangle=-30,
                yaxis_title="USD ($)",
                legend=dict(orientation="h", y=1.1, title=None),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_fee, use_container_width=True)

        with col_right2:
            st.subheader("📅 Enrollment Timeline")
            tl = filtered.copy()
            tl["month"] = tl.enrollment_date.dt.to_period("M").astype(str)
            tl_g = tl.groupby("month").size().reset_index(name="count").sort_values("month")
            
            fig_time = px.area(
                tl_g, x="month", y="count", color_discrete_sequence=[ACCENT], template="plotly_white",
            )
            fig_time.update_traces(fill="tozeroy", fillcolor="rgba(79,110,247,0.15)")
            fig_time.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                xaxis_title="",
                yaxis_title="Enrollments",
                xaxis_tickangle=-30,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
            )
            st.plotly_chart(fig_time, use_container_width=True)

        # Department Summary Table
        st.markdown("---")
        st.subheader("📋 Department Summary")
        summary = (
            filtered.groupby("department")
            .agg(
                Students=("student_id", "count"),
                Avg_GPA=("gpa", lambda x: round(x.mean(), 2)),
                Avg_Tuition=("tuition_fee", lambda x: f"${x.mean():,.0f}"),
                Avg_Scholarship=("scholarship_amount", lambda x: f"${x.mean():,.0f}"),
            )
            .reset_index()
            .rename(columns={"department": "Department"})
        )
        st.dataframe(summary, use_container_width=True)
