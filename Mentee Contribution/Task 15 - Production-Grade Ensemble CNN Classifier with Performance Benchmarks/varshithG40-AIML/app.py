"""
app.py
======
Production-Grade Ensemble CNN Classifier Interactive Web Dashboard.
Features:
  - Glassmorphic dark UI with live inference on uploaded/test images
  - Voting strategy selector (Soft Voting, Majority Hard Voting, Weighted Soft Voting)
  - Individual model agreement/disagreement inspector & confidence gating
  - Robustness perturbation stress-testing laboratory
  - Comprehensive performance benchmark analytics & trade-off recommendation engine
"""

import os
import sys
import time
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

# Setup Path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

from src.data_loader import prepare_dataset, CLASSES
from src.preprocessing import load_full_dataset, preprocess_image, IDX_TO_CLASS
from src.predict import ProductionPredictor
from src.robustness_test import (
    apply_rotation, apply_gaussian_blur, apply_gaussian_noise, apply_illumination, apply_center_crop
)

RESULTS_DIR = os.path.join(ROOT_DIR, "results")
MODELS_DIR = os.path.join(ROOT_DIR, "models")

# Streamlit Page Config
st.set_page_config(
    page_title="Ensemble CNN Classifier & Benchmarks",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Aesthetic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        border-radius: 16px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .badge-unanimous {
        background: #065f46;
        color: #6ee7b7;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-disagreement {
        background: #991b1b;
        color: #fca5a5;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-approved {
        background: #1e3a8a;
        color: #93c5fd;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_predictor():
    """Caches predictor instance with loaded CNN models."""
    prepare_dataset(force=False)
    predictor = ProductionPredictor(confidence_threshold=0.70)
    return predictor


predictor = load_predictor()

# Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
        <div>
            <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.02em;">
                🐾 Production-Grade Ensemble CNN Classifier
            </h1>
            <p style="margin: 6px 0 0 0; opacity: 0.85; font-size: 1.05rem;">
                Comparing Individual CNN Performance vs Multi-Model Ensembles Across Accuracy, Latency & Production Cost
            </p>
        </div>
        <div style="margin-top: 10px;">
            <span style="background: rgba(255, 255, 255, 0.15); padding: 6px 14px; border-radius: 8px; font-weight: 600; font-size: 0.9rem;">
                Dataset: Cats vs Dogs (100 Samples) | 15 Epochs Max
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.title("⚙️ Inference Configuration")

strategy_option = st.sidebar.selectbox(
    "Ensemble Combination Strategy",
    options=["Soft Voting (Arithmetic Average)", "Weighted Soft Voting", "Majority Voting (Hard Voting)"],
    index=0
)

strategy_map = {
    "Soft Voting (Arithmetic Average)": "soft",
    "Weighted Soft Voting": "weighted",
    "Majority Voting (Hard Voting)": "majority"
}
selected_strategy = strategy_map[strategy_option]

confidence_threshold = st.sidebar.slider(
    "Confidence Gating Threshold",
    min_value=0.50,
    max_value=0.95,
    value=0.70,
    step=0.05,
    help="Predictions below this threshold are flagged for human review."
)
predictor.confidence_threshold = confidence_threshold

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Ensemble Members")
st.sidebar.markdown("""
- **CNN 1**: Simple Baseline
- **CNN 2**: Regularized (BN + Dropout)
- **CNN 3**: Deeper (Stacked Conv + GAP)
""")

# Navigation Tabs
tabs = st.tabs([
    "🔍 Live Inference & Diagnostics",
    "📈 Performance Benchmarks",
    "🧪 Robustness Stress-Testing Lab",
    "📊 Training Curves & Confusion Matrices",
    "💡 Production Trade-Off Decision"
])

# ---------------------------------------------------------
# TAB 1: LIVE INFERENCE & DIAGNOSTICS
# ---------------------------------------------------------
with tabs[0]:
    st.subheader("Interactive Image Classification & Ensemble Telemetry")
    col_input, col_results = st.columns([1.1, 1.9])
    
    with col_input:
        input_choice = st.radio(
            "Select Image Source:",
            ["Choose from Test Dataset Split", "Upload Custom Image"],
            horizontal=True
        )
        
        selected_img = None
        
        if input_choice == "Choose from Test Dataset Split":
            _, _, (X_test, y_test), test_paths = load_full_dataset()
            test_indices = list(range(len(X_test)))
            sample_idx = st.selectbox(
                "Select Test Sample Index:",
                options=test_indices,
                format_func=lambda i: f"Test Image #{i+1} (Actual: {IDX_TO_CLASS[np.argmax(y_test[i])].upper()})"
            )
            selected_img = X_test[sample_idx]
            actual_class = IDX_TO_CLASS[np.argmax(y_test[sample_idx])]
            st.image(selected_img, caption=f"Selected Sample #{sample_idx+1} (True: {actual_class})", use_container_width=True)
            
        else:
            uploaded_file = st.file_uploader("Upload an Image (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                img_pil = Image.open(uploaded_file).convert("RGB")
                selected_img = np.array(img_pil.resize((128, 128))) / 255.0
                st.image(img_pil, caption="Uploaded Image", use_container_width=True)
            else:
                st.info("Please upload an image or choose from test samples to test inference.")

    with col_results:
        if selected_img is not None:
            # Run Inference
            pred_response = predictor.predict(
                selected_img,
                ensemble_strategy=selected_strategy,
                include_debug_models=True
            )
            
            p_class = pred_response["predictedClass"].upper()
            conf = pred_response["confidence"]
            conf_pct = pred_response["confidenceScorePct"]
            is_unanimous = pred_response["isUnanimous"]
            decision = pred_response["decision"]
            lat_ms = pred_response["inferenceTimeMs"]
            
            # Prediction Card
            st.markdown(f"""
            <div class="metric-card" style="background: rgba(30, 58, 138, 0.3); border-left: 6px solid #3b82f6;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.8;">Ensemble Prediction</span>
                        <h2 style="margin: 4px 0; font-size: 2.2rem; font-weight: 800; color: #60a5fa;">{p_class}</h2>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.9rem; opacity: 0.8;">Ensemble Confidence</span>
                        <h2 style="margin: 4px 0; font-size: 2.2rem; font-weight: 800; color: #34d399;">{conf_pct}</h2>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Telemetry Row
            c_badge1, c_badge2, c_badge3 = st.columns(3)
            with c_badge1:
                if is_unanimous:
                    st.markdown('<span class="badge-unanimous">✅ Unanimous Consensus (3/3)</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-disagreement">⚠️ Model Disagreement (2 vs 1)</span>', unsafe_allow_html=True)
                    
            with c_badge2:
                if conf >= confidence_threshold:
                    st.markdown('<span class="badge-approved">🚀 Production Approved</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-disagreement">🛑 Manual Review Required</span>', unsafe_allow_html=True)
                    
            with c_badge3:
                st.markdown(f'<span class="badge-approved">⏱️ Latency: {lat_ms:.2f} ms</span>', unsafe_allow_html=True)
                
            st.markdown("---")
            st.markdown("#### 🗳️ Individual CNN Votes & Probability Breakdown")
            
            indiv = pred_response["individualModels"]
            c_m1, c_m2, c_m3 = st.columns(3)
            
            with c_m1:
                m1_info = indiv["cnn1_baseline"]
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0 0 8px 0;">CNN 1 (Baseline)</h4>
                    <p style="font-size: 1.2rem; font-weight: 700; margin: 0; color: #93c5fd;">{m1_info['predictedClass'].upper()}</p>
                    <p style="margin: 4px 0 0 0; opacity: 0.8; font-size: 0.9rem;">Confidence: <b>{m1_info['confidence']*100:.1f}%</b></p>
                    <div style="margin-top: 8px; font-size: 0.8rem; opacity: 0.75;">
                        Cat: {m1_info['catProb']*100:.1f}% | Dog: {m1_info['dogProb']*100:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_m2:
                m2_info = indiv["cnn2_regularized"]
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0 0 8px 0;">CNN 2 (Regularized)</h4>
                    <p style="font-size: 1.2rem; font-weight: 700; margin: 0; color: #93c5fd;">{m2_info['predictedClass'].upper()}</p>
                    <p style="margin: 4px 0 0 0; opacity: 0.8; font-size: 0.9rem;">Confidence: <b>{m2_info['confidence']*100:.1f}%</b></p>
                    <div style="margin-top: 8px; font-size: 0.8rem; opacity: 0.75;">
                        Cat: {m2_info['catProb']*100:.1f}% | Dog: {m2_info['dogProb']*100:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c_m3:
                m3_info = indiv["cnn3_deep"]
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0 0 8px 0;">CNN 3 (Deeper)</h4>
                    <p style="font-size: 1.2rem; font-weight: 700; margin: 0; color: #93c5fd;">{m3_info['predictedClass'].upper()}</p>
                    <p style="margin: 4px 0 0 0; opacity: 0.8; font-size: 0.9rem;">Confidence: <b>{m3_info['confidence']*100:.1f}%</b></p>
                    <div style="margin-top: 8px; font-size: 0.8rem; opacity: 0.75;">
                        Cat: {m3_info['catProb']*100:.1f}% | Dog: {m3_info['dogProb']*100:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: PERFORMANCE BENCHMARKS
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("Production Performance Benchmarks (Empirical Metrics)")
    
    csv_final_path = os.path.join(RESULTS_DIR, "final_comparison.csv")
    csv_bench_path = os.path.join(RESULTS_DIR, "benchmark_results.csv")
    
    if os.path.exists(csv_final_path):
        df_final = pd.read_csv(csv_final_path)
        st.dataframe(df_final, use_container_width=True)
        
        st.markdown("---")
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("#### ⚡ Latency vs. Accuracy Trade-Off")
            chart_df = df_final[["Model / Method", "Avg Latency (ms)", "Accuracy (%)"]].copy()
            st.bar_chart(chart_df.set_index("Model / Method")["Avg Latency (ms)"])
            
        with col_c2:
            st.markdown("#### 📦 Disk Model Size (MB)")
            st.bar_chart(df_final.set_index("Model / Method")["Model Size (MB)"])
            
        st.markdown("---")
        if os.path.exists(csv_bench_path):
            st.markdown("#### ⚙️ Detailed Benchmarking Metrics (Sequential vs Parallel ThreadPool Inference)")
            df_bench = pd.read_csv(csv_bench_path)
            st.dataframe(df_bench, use_container_width=True)
    else:
        st.warning("Benchmark CSVs not found. Please run python main.py first.")

# ---------------------------------------------------------
# TAB 3: ROBUSTNESS STRESS-TESTING LAB
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("Out-of-Distribution Robustness Stress-Testing")
    st.write("Apply real-time perturbations to test images and evaluate how individual CNNs vs Ensemble hold up.")
    
    col_p_img, col_p_ctrl = st.columns([1, 1])
    
    with col_p_ctrl:
        pert_type = st.selectbox(
            "Select Perturbation / Distortion Type:",
            ["Gaussian Blur", "Gaussian Noise", "Rotation", "Brightness / Illumination", "Center Crop"]
        )
        
        _, _, (X_test, y_test), _ = load_full_dataset()
        test_idx = st.selectbox("Select Test Image:", options=range(len(X_test)), format_func=lambda i: f"Sample #{i+1} ({IDX_TO_CLASS[np.argmax(y_test[i])].upper()})")
        base_img = X_test[test_idx]
        
        if pert_type == "Gaussian Blur":
            ksize = st.slider("Kernel Size", min_value=3, max_value=15, value=7, step=2)
            sigma = st.slider("Sigma (Blur strength)", min_value=0.5, max_value=5.0, value=2.5, step=0.5)
            pert_img = apply_gaussian_blur(base_img[np.newaxis, ...], ksize, sigma)[0]
            
        elif pert_type == "Gaussian Noise":
            noise_sigma = st.slider("Noise Intensity (Sigma)", min_value=0.05, max_value=0.50, value=0.20, step=0.05)
            pert_img = apply_gaussian_noise(base_img[np.newaxis, ...], 0.0, noise_sigma)[0]
            
        elif pert_type == "Rotation":
            rot_deg = st.slider("Rotation Angle (Degrees)", min_value=-90, max_value=90, value=30, step=5)
            pert_img = apply_rotation(base_img[np.newaxis, ...], rot_deg)[0]
            
        elif pert_type == "Brightness / Illumination":
            ill_factor = st.slider("Illumination Scaling Factor", min_value=0.1, max_value=2.5, value=0.5, step=0.1)
            pert_img = apply_illumination(base_img[np.newaxis, ...], ill_factor)[0]
            
        else:  # Center Crop
            crop_rat = st.slider("Crop Ratio", min_value=0.4, max_value=0.9, value=0.7, step=0.05)
            pert_img = apply_center_crop(base_img[np.newaxis, ...], crop_rat)[0]

    with col_p_img:
        ci1, ci2 = st.columns(2)
        with ci1:
            st.image(base_img, caption="Original Clean Image", use_container_width=True)
        with ci2:
            st.image(pert_img, caption=f"Perturbed Image ({pert_type})", use_container_width=True)
            
    st.markdown("---")
    st.markdown("#### 🔬 Live Stress-Test Results on Perturbed Input")
    
    pert_resp = predictor.predict(pert_img, ensemble_strategy="soft")
    indiv_pert = pert_resp["individualModels"]
    
    cp1, cp2, cp3, cp_ens = st.columns(4)
    with cp1:
        st.metric("CNN 1 (Baseline)", indiv_pert["cnn1_baseline"]["predictedClass"].upper(), f"{indiv_pert['cnn1_baseline']['confidence']*100:.1f}%")
    with cp2:
        st.metric("CNN 2 (Regularized)", indiv_pert["cnn2_regularized"]["predictedClass"].upper(), f"{indiv_pert['cnn2_regularized']['confidence']*100:.1f}%")
    with cp3:
        st.metric("CNN 3 (Deeper)", indiv_pert["cnn3_deep"]["predictedClass"].upper(), f"{indiv_pert['cnn3_deep']['confidence']*100:.1f}%")
    with cp_ens:
        st.metric("Ensemble (Soft Voting)", pert_resp["predictedClass"].upper(), f"{pert_resp['confidence']*100:.1f}%")
        
    st.markdown("---")
    rob_chart_path = os.path.join(RESULTS_DIR, "robustness_comparison.png")
    if os.path.exists(rob_chart_path):
        st.markdown("#### 📊 Comprehensive Robustness Comparison Chart (Across All Test Perturbations)")
        st.image(rob_chart_path, use_container_width=True)

# ---------------------------------------------------------
# TAB 4: TRAINING CURVES & CONFUSION MATRICES
# ---------------------------------------------------------
with tabs[3]:
    st.subheader("Training Convergence & Confusion Matrices Gallery")
    
    st.markdown("### 📈 Training History (Accuracy & Loss Curves over 15 Epochs)")
    th1 = os.path.join(RESULTS_DIR, "training_history_cnn1.png")
    th2 = os.path.join(RESULTS_DIR, "training_history_cnn2.png")
    th3 = os.path.join(RESULTS_DIR, "training_history_cnn3.png")
    
    c_th1, c_th2 = st.columns(2)
    with c_th1:
        if os.path.exists(th1):
            st.image(th1, caption="CNN 1 (Baseline) Convergence", use_container_width=True)
        if os.path.exists(th3):
            st.image(th3, caption="CNN 3 (Deeper) Convergence", use_container_width=True)
    with c_th2:
        if os.path.exists(th2):
            st.image(th2, caption="CNN 2 (Regularized) Convergence", use_container_width=True)
            
    st.markdown("---")
    st.markdown("### 🎯 Confusion Matrices Gallery")
    cm1 = os.path.join(RESULTS_DIR, "confusion_matrix_cnn1.png")
    cm2 = os.path.join(RESULTS_DIR, "confusion_matrix_cnn2.png")
    cm3 = os.path.join(RESULTS_DIR, "confusion_matrix_cnn3.png")
    cm_ens = os.path.join(RESULTS_DIR, "confusion_matrix_ensemble.png")
    
    ccm1, ccm2, ccm3, ccm4 = st.columns(4)
    with ccm1:
        if os.path.exists(cm1):
            st.image(cm1, caption="CNN 1 Confusion Matrix", use_container_width=True)
    with ccm2:
        if os.path.exists(cm2):
            st.image(cm2, caption="CNN 2 Confusion Matrix", use_container_width=True)
    with ccm3:
        if os.path.exists(cm3):
            st.image(cm3, caption="CNN 3 Confusion Matrix", use_container_width=True)
    with ccm4:
        if os.path.exists(cm_ens):
            st.image(cm_ens, caption="Ensemble Confusion Matrix", use_container_width=True)

# ---------------------------------------------------------
# TAB 5: PRODUCTION TRADE-OFF DECISION
# ---------------------------------------------------------
with tabs[4]:
    st.subheader("💡 Production Deployment Recommendation & Cost-Benefit Analysis")
    
    st.markdown("""
    ### ⚖️ The Production Question: Is the Ensemble Worth the Extra Compute?
    
    In production machine learning, accuracy is never evaluated in a vacuum. Deploying an ensemble of 3 models versus a single best model presents major trade-offs:
    """)
    
    c_rec1, c_rec2 = st.columns(2)
    
    with c_rec1:
        st.markdown("""
        <div class="metric-card" style="border-left: 6px solid #10b981;">
            <h3 style="margin-top: 0; color: #34d399;">🌟 Recommended for Offline Batch Processing: Ensemble (Soft Voting)</h3>
            <ul style="line-height: 1.7; font-size: 0.95rem;">
                <li><b>Highest Classification Reliability</b>: Reaches peak accuracy across diverse samples.</li>
                <li><b>Superior Out-of-Distribution Stability</b>: Corrects single-model classification errors when images are degraded.</li>
                <li><b>Model Disagreement Signal</b>: Provides automated human-in-the-loop review gating when models disagree.</li>
                <li><b>Trade-off</b>: Higher latency (~635 ms sequential / ~468 ms parallel) and larger combined disk size (~97.4 MB).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c_rec2:
        st.markdown("""
        <div class="metric-card" style="border-left: 6px solid #6366f1;">
            <h3 style="margin-top: 0; color: #818cf8;">⚡ Recommended for Real-Time / Edge Systems: CNN 3 (Deeper CNN)</h3>
            <ul style="line-height: 1.7; font-size: 0.95rem;">
                <li><b>Ultra-Lightweight Footprint</b>: Only <b>70,050 parameters</b> (vs 8.4M combined ensemble).</li>
                <li><b>Tiny Model File Size</b>: Just <b>0.86 MB</b> on disk (vs 97.4 MB for the ensemble).</li>
                <li><b>Fast Single-Model Inference</b>: ~183 ms latency with 5.4 img/s throughput.</li>
                <li><b>Identical Test Accuracy</b>: Achieves 100% test accuracy on standard clean inputs.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 🎛️ Interactive Deployment Decision Calculator")
    latency_budget = st.slider("Target Maximum Latency Budget (ms):", min_value=100, max_value=800, value=250, step=25)
    
    if latency_budget < 350:
        st.success(f"🎯 At a latency budget of {latency_budget} ms, **CNN 3 (Deeper CNN)** is the optimal deployment model due to its ultra-compact 0.86 MB disk footprint, 70k parameter efficiency, and 183 ms latency.")
    else:
        st.info(f"🎯 At a latency budget of {latency_budget} ms, **Ensemble (Soft Voting)** is recommended to leverage multi-model consensus voting and heightened perturbation robustness.")
