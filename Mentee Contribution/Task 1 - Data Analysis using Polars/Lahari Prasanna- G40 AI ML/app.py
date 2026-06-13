
import streamlit as st

st.set_page_config(
    page_title="Developer Career Intelligence",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Developer Career Intelligence Warehouse")
st.markdown("### Built from Stack Overflow Developer Survey 2020–2025")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Responses",   "424,980")
col2.metric("Countries",         "196")
col3.metric("Global Median Salary", "$64,630")
col4.metric("Years Covered",     "2020–2025")

st.markdown("---")

st.markdown("""
### About This Dashboard
This dashboard analyzes **424,980 developer responses** from the Stack Overflow
Developer Survey across 6 years (2020–2025).

**Use the sidebar to navigate between pages:**
- 📊 **Overview** — Key metrics and KPIs
- 💰 **Salary Analysis** — Salary by role, country, education, experience
- 🛠️ **Technology Trends** — Languages, databases, frameworks over time
- 👥 **HR Analytics** — Skills, roles, and developer profiles

**Data Source:** [Stack Overflow Developer Survey](https://survey.stackoverflow.co/)
""")
