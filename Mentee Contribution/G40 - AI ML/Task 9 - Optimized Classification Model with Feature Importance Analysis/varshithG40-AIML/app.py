"""
E-Commerce Purchase Prediction - Modern Web Interface
Beautiful, interactive dashboard for the ML model
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Purchase Prediction AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Streamlit
st.markdown("""
<style>
            
                section[data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label p {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
            
    /* Global styles */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4) !important;
    }
    
    .main-header p {
        color: white !important;
        font-size: 1.3rem !important;
        margin-top: 1rem !important;
        font-weight: 500 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        opacity: 1 !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.8rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        color: #667eea !important;
        margin: 0.5rem 0 !important;
    }
    
    .metric-label {
        font-size: 0.9rem !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        font-weight: 700 !important;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem 2rem;
        border-radius: 12px;
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2.5rem !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #2d5a7b 100%) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p {
        color: rgba(255,255,255,0.8) !important;
    }
                /* Fix sidebar text visibility */
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        color: white !important;
    }
            /* Streamlit 1.50 Sidebar Toggle Button */
button[data-testid="stBaseButton-headerNoPadding"] {
    color: #ffffff !important;
    background: transparent !important;
}

button[data-testid="stBaseButton-headerNoPadding"] svg {
    stroke: #ffffff !important;
    fill: none !important;
    color: #ffffff !important;
    opacity: 1 !important;
}

button[data-testid="stBaseButton-headerNoPadding"]:hover {
    background: rgba(255,255,255,0.15) !important;
}
            
</style>
""", unsafe_allow_html=True)

# Load model and data
@st.cache_resource
def load_model():
    model_path = Path("models/purchase_prediction_model.pkl")
    metadata_path = Path("models/model_metadata.json")
    
    if model_path.exists():
        try:
            model = joblib.load(model_path)
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            return model, metadata
        except Exception:
            pass
    
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from train_model import train_model
        model = train_model()
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        return model, metadata
    except Exception:
        return None, None

@st.cache_data
def load_data():
    data_path = Path("data/ecommerce_customer_data.csv")
    if data_path.exists():
        return pd.read_csv(data_path)
    return None

# Initialize
model, metadata = load_model()
df = load_data()

# Sidebar navigation
st.sidebar.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <div style='font-size: 3rem;'>🛒</div>
    <h2 style='color: white; margin: 0.5rem 0;'>Purchase Prediction AI</h2>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "🎯 Predict Purchase", "📊 Model Performance", "🔍 Feature Analysis", " Business Insights"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='color: rgba(255,255,255,0.8); text-align: center; padding: 1rem;'>
    <p style='font-size: 0.9rem;'>Powered by Machine Learning</p>
    <p style='font-size: 0.8rem; opacity: 0.7;'>Logistic Regression</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
if page == "🏠 Dashboard":
    # Header
    st.markdown("""
    <div class='main-header'>
        <h1>🛒 E-Commerce Purchase Prediction</h1>
        <p>AI-Powered Customer Behavior Analysis & Prediction System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Model Accuracy</div>
            <div class='metric-value'>{metadata['metrics']['Accuracy']:.1%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>F1 Score</div>
            <div class='metric-value'>{metadata['metrics']['F1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>ROC-AUC</div>
            <div class='metric-value'>{metadata['metrics']['ROC-AUC']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Customers Analyzed</div>
            <div class='metric-value'>5,000</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two columns for overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Dataset Overview")
        
        if df is not None:
            # Purchase distribution
            purchase_rate = df['Purchase'].mean()
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Purchase Distribution', 'Purchase Rate'),
                specs=[[{"type": "bar"}, {"type": "pie"}]]
            )
            
            # Bar chart
            counts = df['Purchase'].value_counts()
            fig.add_trace(
                go.Bar(
                    x=['No Purchase', 'Purchase'],
                    y=[counts[0], counts[1]],
                    marker_color=['#4facfe', '#38ef7d'],
                    text=[f"{counts[0]:,}", f"{counts[1]:,}"],
                    textposition='auto'
                ),
                row=1, col=1
            )
            
            # Pie chart
            fig.add_trace(
                go.Pie(
                    labels=['Non-Purchasers', 'Purchasers'],
                    values=[counts[0], counts[1]],
                    marker_colors=['#4facfe', '#38ef7d'],
                    hole=0.4
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Key Statistics")
        
        if df is not None:
            stats_df = pd.DataFrame({
                'Metric': [
                    'Total Customers',
                    'Purchasers',
                    'Non-Purchasers',
                    'Purchase Rate',
                    'Avg Cart Items',
                    'Avg Time on Site',
                    'Avg Previous Purchases'
                ],
                'Value': [
                    f"{len(df):,}",
                    f"{df['Purchase'].sum():,}",
                    f"{(len(df) - df['Purchase'].sum()):,}",
                    f"{df['Purchase'].mean():.1%}",
                    f"{df['CartItems'].mean():.2f}",
                    f"{df['TimeOnSite'].mean():.1f} min",
                    f"{df['PreviousPurchases'].mean():.1f}"
                ]
            })
            
            st.dataframe(
                stats_df,
                hide_index=True,
                use_container_width=True
            )
    
    # Project highlights
    st.markdown("### ✨ Project Highlights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>🤖 Smart Predictions</h4>
            <p>Advanced ML model predicts purchase likelihood with 83% accuracy using customer behavior patterns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>📊 Data-Driven Insights</h4>
            <p>Comprehensive analysis of 18 features identifying key purchase drivers and customer segments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>💡 Actionable Recommendations</h4>
            <p>8 evidence-based business strategies to increase conversion rates and customer engagement</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PREDICT PAGE
# ============================================================================
elif page == "🎯 Predict Purchase":
    st.markdown("""
    <div class='main-header'>
        <h1>🎯 Predict Purchase Likelihood</h1>
        <p>Enter customer details to predict purchase probability</p>
    </div>
    """, unsafe_allow_html=True)
    
    if model is not None:
        # Input form
        st.markdown("### 📝 Customer Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Demographics**")
            age = st.slider("Age", 18, 75, 35)
            gender = st.selectbox("Gender", ["Male", "Female"])
            location = st.selectbox("Location", ["Urban", "Suburban", "Rural"])
        
        with col2:
            st.markdown("**Browsing Behavior**")
            pages_viewed = st.slider("Pages Viewed", 1, 20, 7)
            time_on_site = st.slider("Time on Site (min)", 1.0, 120.0, 15.0)
            products_viewed = st.slider("Products Viewed", 1, 30, 8)
            cart_items = st.slider("Cart Items", 0, 7, 1)
        
        with col3:
            st.markdown("**History & Engagement**")
            previous_purchases = st.slider("Previous Purchases", 0, 15, 3)
            avg_order_value = st.slider("Avg Order Value ($)", 10, 2000, 100)
            discount_used = st.selectbox("Discount Used", ["No", "Yes"])
            email_clicked = st.selectbox("Email Clicked", ["No", "Yes"])
            ad_clicked = st.selectbox("Ad Clicked", ["No", "Yes"])
            review_score = st.slider("Review Score Viewed", 1.0, 5.0, 4.0)
            days_since_visit = st.slider("Days Since Last Visit", 0, 365, 20)
            session_count = st.slider("Session Count", 1, 20, 5)
        
        # Device and traffic source
        col1, col2 = st.columns(2)
        with col1:
            device_type = st.selectbox("Device Type", ["Desktop", "Mobile", "Tablet"])
        with col2:
            traffic_source = st.selectbox("Traffic Source", 
                                         ["Organic Search", "Paid Search", "Social Media", 
                                          "Email", "Direct", "Referral"])
        
        st.markdown("---")
        
        # Predict button
        if st.button("🔮 Predict Purchase Likelihood", use_container_width=True):
            # Prepare input data
            input_data = pd.DataFrame({
                'Age': [age],
                'Gender': [gender],
                'Location': [location],
                'DeviceType': [device_type],
                'TrafficSource': [traffic_source],
                'PagesViewed': [pages_viewed],
                'TimeOnSite': [time_on_site],
                'ProductsViewed': [products_viewed],
                'CartItems': [cart_items],
                'PreviousPurchases': [previous_purchases],
                'AverageOrderValue': [avg_order_value],
                'DiscountUsed': [1 if discount_used == "Yes" else 0],
                'EmailClicked': [1 if email_clicked == "Yes" else 0],
                'AdClicked': [1 if ad_clicked == "Yes" else 0],
                'ReviewScoreViewed': [review_score],
                'DaysSinceLastVisit': [days_since_visit],
                'SessionCount': [session_count]
            })
            
            # Make prediction
            try:
                prediction_prob = model.predict_proba(input_data)[0][1]
                prediction_class = model.predict(input_data)[0]
                
                # Determine segment
                if prediction_prob >= 0.6:
                    segment = "High"
                    icon = ""
                elif prediction_prob >= 0.3:
                    segment = "Medium"
                    icon = "🟡"
                else:
                    segment = "Low"
                    icon = "🔵"
                
                # Display result
                st.success(f"{icon} **Purchase Probability: {prediction_prob:.1%}** - {segment} Likelihood Customer")
                
                # Additional insights
                st.markdown("### 📊 Prediction Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gauge chart
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=prediction_prob * 100,
                        title={'text': "Purchase Probability"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#667eea"},
                            'steps': [
                                {'range': [0, 30], 'color': '#4facfe'},
                                {'range': [30, 60], 'color': '#f59e0b'},
                                {'range': [60, 100], 'color': '#38ef7d'}
                            ]
                        }
                    ))
                    
                    fig_gauge.update_layout(height=300)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                with col2:
                    st.markdown("**Key Factors Influencing This Prediction:**")
                    
                    factors = []
                    if cart_items > 0:
                        factors.append(f"✅ {cart_items} item(s) in cart")
                    if time_on_site > 15:
                        factors.append(f"✅ High engagement ({time_on_site:.0f} min)")
                    if previous_purchases > 3:
                        factors.append(f"✅ Repeat customer ({previous_purchases} purchases)")
                    if email_clicked == "Yes":
                        factors.append("✅ Email engagement")
                    if discount_used == "Yes":
                        factors.append("✅ Discount incentive used")
                    if days_since_visit > 60:
                        factors.append(f"⚠️ Long absence ({days_since_visit} days)")
                    if cart_items == 0:
                        factors.append("❌ Empty cart")
                    if time_on_site < 5:
                        factors.append(f"❌ Low engagement ({time_on_site:.0f} min)")
                    
                    for factor in factors:
                        st.markdown(factor)
                
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")

# ============================================================================
# MODEL PERFORMANCE PAGE
# ============================================================================
elif page == "📊 Model Performance":
    st.markdown("""
    <div class='main-header'>
        <h1>📊 Model Performance Dashboard</h1>
        <p>Comprehensive evaluation metrics and comparisons</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model info
    st.markdown("### 🤖 Model Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Model Type</div>
            <div style='font-size: 1.5rem; color: #667eea; font-weight: 600; margin: 1rem 0;'>
                {metadata['model_type']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Training Samples</div>
            <div style='font-size: 1.5rem; color: #667eea; font-weight: 600; margin: 1rem 0;'>
                {metadata['training_info']['train_size']:,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Test Samples</div>
            <div style='font-size: 1.5rem; color: #667eea; font-weight: 600; margin: 1rem 0;'>
                {metadata['training_info']['test_size']:,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Performance metrics
    st.markdown("### 🎯 Performance Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = metadata['metrics']
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Accuracy</div>
            <div class='metric-value'>{metrics['Accuracy']:.1%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Precision</div>
            <div class='metric-value'>{metrics['Precision']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Recall</div>
            <div class='metric-value'>{metrics['Recall']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>F1-Score</div>
            <div class='metric-value'>{metrics['F1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>ROC-AUC</div>
            <div class='metric-value'>{metrics['ROC-AUC']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model comparison
    st.markdown("###  Model Comparison")
    
    comparison_data = pd.DataFrame({
        'Model': ['LR (Baseline)', 'DT (Baseline)', 'RF (Baseline)',
                  'LR (Optimized)', 'DT (Optimized)', 'RF (Optimized)'],
        'F1-Score': [0.627, 0.514, 0.581, 0.650, 0.526, 0.566],
        'ROC-AUC': [0.830, 0.641, 0.814, 0.830, 0.736, 0.808]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_f1 = px.bar(
            comparison_data,
            x='Model',
            y='F1-Score',
            title='F1-Score Comparison',
            color='F1-Score',
            color_continuous_scale='Viridis'
        )
        fig_f1.update_layout(height=400)
        st.plotly_chart(fig_f1, use_container_width=True)
    
    with col2:
        fig_auc = px.bar(
            comparison_data,
            x='Model',
            y='ROC-AUC',
            title='ROC-AUC Comparison',
            color='ROC-AUC',
            color_continuous_scale='Plasma'
        )
        fig_auc.update_layout(height=400)
        st.plotly_chart(fig_auc, use_container_width=True)
    
    # Hyperparameters
    st.markdown("### ⚙️ Optimal Hyperparameters")
    
    hyperparams = metadata['hyperparameters']
    key_params = {
        'C (Regularization)': hyperparams.get('C', 'N/A'),
        'Class Weight': hyperparams.get('class_weight', 'N/A'),
        'Solver': hyperparams.get('solver', 'N/A'),
        'Max Iterations': hyperparams.get('max_iter', 'N/A'),
        'Penalty': hyperparams.get('penalty', 'N/A')
    }
    
    params_df = pd.DataFrame(list(key_params.items()), columns=['Parameter', 'Value'])
    st.dataframe(params_df, hide_index=True, use_container_width=True)

# ============================================================================
# FEATURE ANALYSIS PAGE
# ============================================================================
elif page == "🔍 Feature Analysis":
    st.markdown("""
    <div class='main-header'>
        <h1>🔍 Feature Importance Analysis</h1>
        <p>Understanding what drives purchase decisions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature importance data
    feature_data = pd.DataFrame({
        'Feature': ['CartItems', 'TimeOnSite', 'DiscountUsed', 'EmailClicked', 
                    'PreviousPurchases', 'ProductsViewed', 'PagesViewed', 
                    'DaysSinceLastVisit'],
        'Importance': [0.1895, 0.1396, 0.1281, 0.1254, 0.1038, 0.0499, 
                      0.0405, 0.0324]
    })
    
    # Top features visualization
    st.markdown("### 🏆 Top 10 Most Important Features")
    
    fig = px.bar(
        feature_data.head(8),
        x='Importance',
        y='Feature',
        orientation='h',
        title='Feature Importance',
        color='Importance',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Feature categories
    st.markdown("### 📊 Feature Categories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>🛒 Cart & Engagement</h4>
            <p>• Cart Items (18.95%)</p>
            <p>• Time on Site (13.96%)</p>
            <p>• Products Viewed (4.99%)</p>
            <p>• Pages Viewed (4.05%)</p>
            <p style='margin-top: 1rem; color: #667eea; font-weight: 700;'>Total Impact: 41.95%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>📧 Marketing & History</h4>
            <p>• Discount Used (12.81%)</p>
            <p>• Email Clicked (12.54%)</p>
            <p>• Previous Purchases (10.38%)</p>
            <p style='margin-top: 1rem; color: #667eea; font-weight: 700;'>Total Impact: 35.73%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>🌐 Traffic & Recency</h4>
            <p>• Days Since Visit (-3.24%)</p>
            <p style='margin-top: 1rem; color: #667eea; font-weight: 700;'>Negative Impact</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Correlation analysis
    if df is not None:
        st.markdown("### 🔗 Feature Correlations with Purchase")
        
        numeric_df = df.select_dtypes(include=[np.number])
        if 'Purchase' in numeric_df.columns:
            correlations = numeric_df.corr()['Purchase'].drop('Purchase').sort_values(ascending=False)
            
            fig_corr = px.bar(
                x=correlations.index,
                y=correlations.values,
                title='Correlation with Purchase (Top 10)',
                labels={'x': 'Feature', 'y': 'Correlation'},
                color=correlations.values,
                color_continuous_scale='RdBu_r'
            )
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)

# ============================================================================
# BUSINESS INSIGHTS PAGE
# ============================================================================
# BUSINESS INSIGHTS
elif page == " Business Insights":
    st.markdown("""
    <div class='main-header'>
        <h1>💡 Business Recommendations</h1>
        <p>Data-driven strategies to increase conversion rates</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Strategic Recommendations")
    
    recommendations = [
        {
            "title": "🛒 Abandoned Cart Recovery",
            "finding": "Cart items is the #1 predictor (importance: 0.1895)",
            "action": "Deploy automated cart recovery emails at 1hr, 24hr, 72hr with time-limited discounts",
            "benefit": "15-25% recovery rate, 8-12% conversion increase",
            "priority": "High"
        },
        {
            "title": "⏱️ Engagement Optimization",
            "finding": "Time on site is the #2 predictor (importance: 0.1396)",
            "action": "Personalized recommendations after 10+ min browsing, live chat support",
            "benefit": "10-15% conversion increase among high-engagement users",
            "priority": "High"
        },
        {
            "title": "📧 Email Marketing",
            "finding": "Email engagement has importance of 0.1254",
            "action": "Behavioral triggers, personalized recommendations, A/B testing",
            "benefit": "25-35% increase in email-driven conversions",
            "priority": "High"
        },
        {
            "title": "🎯 Discount Targeting",
            "finding": "Discount usage is the #3 predictor (importance: 0.1281)",
            "action": "Dynamic discounting based on purchase probability segments",
            "benefit": "10-15% conversion increase with 20-25% less discount spend",
            "priority": "Medium"
        },
        {
            "title": "⭐ Loyalty Program",
            "finding": "Previous purchases have importance of 0.1038",
            "action": "Points-based rewards with tiered benefits (Silver/Gold/Platinum)",
            "benefit": "20-30% increase in repeat purchase rate",
            "priority": "Medium"
        },
        {
            "title": "🔄 Win-Back Campaigns",
            "finding": "Days since last visit negatively impacts purchase (-0.0324)",
            "action": "Escalating re-engagement at 30/60/90 days with increasing offers",
            "benefit": "8-12% reactivation rate, 5-8% revenue recovery",
            "priority": "Medium"
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"{rec['title']} - {rec['priority']} Priority", expanded=True):
            st.markdown(f"**🔍 Finding:** {rec['finding']}")
            st.markdown(f"**🎯 Action:** {rec['action']}")
            st.markdown(f"**✅ Expected Benefit:** {rec['benefit']}")
            
            if rec['priority'] == 'High':
                st.success("HIGH PRIORITY - Quick Win")
            else:
                st.info("MEDIUM PRIORITY - High Impact")
    
    st.markdown("---")
    st.markdown("### 📈 Success Metrics & KPIs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>Conversion Rate</h4>
            <div style='font-size: 1.2rem; color: #10b981; font-weight: 600;'>
                Target: +15-20%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>Customer LTV</h4>
            <div style='font-size: 1.2rem; color: #10b981; font-weight: 600;'>
                Target: +15-20%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #667eea;'>Cart Recovery</h4>
            <div style='font-size: 1.2rem; color: #10b981; font-weight: 600;'>
                Target: 15-25%
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #64748b;'>
    <p>Built with ❤️ using Streamlit & Machine Learning</p>
    <p style='font-size: 0.9rem;'>© 2024 E-Commerce Purchase Prediction System</p>
</div>
""", unsafe_allow_html=True)
