import streamlit as st
from utils import load_data

# Page configuration
st.set_page_config(
    page_title="Student Enrollment Analytics Portal",
    page_icon="🎓",
    layout="wide"
)

# Premium styling
st.markdown("""
<style>
    .welcome-container {
        background: linear-gradient(135deg, #4F6EF7 0%, #3B54C4 100%);
        color: white;
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .welcome-title {
        font-family: 'Outfit', sans-serif;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .welcome-subtitle {
        font-size: 16px;
        opacity: 0.9;
    }
    .feature-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 24px;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 110, 247, 0.1);
        border-color: #C7D2FE;
    }
    .feature-icon {
        font-size: 28px;
        margin-bottom: 12px;
    }
    .feature-title {
        font-size: 18px;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 8px;
    }
    .feature-desc {
        font-size: 14px;
        color: #64748B;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="welcome-container">
    <div class="welcome-title">🎓 Student Enrollment Analytics Dashboard</div>
    <div class="welcome-subtitle">Welcome to the central analytics portal. Use the sidebar to navigate to specialized reports and interactive data explorations.</div>
</div>
""", unsafe_allow_html=True)

# Load data
df = load_data()

# Summary Metrics in Columns
st.subheader("📊 High-Level Insights")
col1, col2, col3, col4 = st.columns(4)

total_students = df.student_id.nunique()
total_courses = df.course.nunique()
avg_gpa = df.gpa.mean()
avg_tuition = df.tuition_fee.mean()

col1.metric("Total Unique Students", f"{total_students:,}")
col2.metric("Courses Offered", f"{total_courses}")
col3.metric("Average Student GPA", f"{avg_gpa:.2f}")
col4.metric("Average Tuition Fee", f"${avg_tuition:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Cards
st.subheader("📂 Dashboard Sections")
card_col1, card_col2, card_col3 = st.columns(3)

with card_col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Dashboard Overview</div>
        <div class="feature-desc">Get a high-level snapshot of overall student numbers, currently enrolled counts, average GPA, drop rates, and key gender/department breakdowns.</div>
    </div>
    """, unsafe_allow_html=True)

with card_col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Course Analysis</div>
        <div class="feature-desc">Examine course popularity, student distribution across credits, average GPA performance per course, and enrollment status breakdown.</div>
    </div>
    """, unsafe_allow_html=True)

with card_col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Enrollment Analysis</div>
        <div class="feature-desc">Track enrollment numbers semester-by-semester, explore tuition vs scholarship funds by department, and see active timeline details.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
card_col4, card_col5, card_col6 = st.columns(3)

with card_col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👨‍🎓</div>
        <div class="feature-title">Student Analysis</div>
        <div class="feature-desc">Analyze demographic splits, age distributions, GPA distributions, and correlations between student age and academic performance.</div>
    </div>
    """, unsafe_allow_html=True)

with card_col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📅</div>
        <div class="feature-title">Trend Analysis</div>
        <div class="feature-desc">Explore time-series trends, monthly enrollment rates, historical drop rate variations, and individual department growth metrics.</div>
    </div>
    """, unsafe_allow_html=True)

with card_col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚙️</div>
        <div class="feature-title">Multipage Navigation</div>
        <div class="feature-desc">To navigate between pages, expand the sidebar on the left side of the screen and select any analysis page.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>---", unsafe_allow_html=True)

# Dataset overview preview
st.subheader("📋 Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)