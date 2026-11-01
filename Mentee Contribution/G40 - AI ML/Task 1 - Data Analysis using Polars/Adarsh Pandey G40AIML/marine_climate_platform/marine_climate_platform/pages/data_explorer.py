"""
Data Explorer Page – Marine Climate Intelligence Platform
Allows CSV upload, filtering, and interactive chart generation.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import load_default_data, load_uploaded_data, apply_theme, compute_stats


def render(df_default: pd.DataFrame = None):
    if df_default is None:
        df_default = load_default_data()

    st.markdown("""
    <div class="page-header">
        <h1>🔬 Data Explorer</h1>
        <p>Upload your own marine dataset or explore the bundled sample. Filter, visualise, and interrogate the data interactively.</p>
    </div>""", unsafe_allow_html=True)

    # ── Upload Panel ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>📂 Data Source</h3></div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload a CSV file (optional — leave empty to use the built-in sample dataset)",
        type=["csv"],
        help="Your file should have a date column and numeric columns."
    )

    if uploaded:
        try:
            df = load_uploaded_data(uploaded)
            st.markdown("""<div class="info-panel">
                ✅ <strong>Custom dataset loaded</strong> — using your uploaded file.
            </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not parse file: {e}")
            df = df_default
    else:
        df = df_default
        st.markdown("""<div class="info-panel">
            📊 Using the <strong>built-in sample dataset</strong> (1 500 records, 5 ocean regions, 2000–2024).
        </div>""", unsafe_allow_html=True)

    # ── Identify columns ──────────────────────────────────────────────────────
    date_cols    = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols     = df.select_dtypes(include="object").columns.tolist()

    # ── Filters ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>🎛️ Filters</h3></div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns([1, 1, 1])

    filtered_df = df.copy()

    with f1:
        if date_cols:
            date_col = date_cols[0]
            min_d = df[date_col].min().date()
            max_d = df[date_col].max().date()
            date_range = st.date_input(
                "Date Range",
                value=(min_d, max_d),
                min_value=min_d, max_value=max_d
            )
            if len(date_range) == 2:
                filtered_df = filtered_df[
                    (filtered_df[date_col].dt.date >= date_range[0]) &
                    (filtered_df[date_col].dt.date <= date_range[1])
                ]
        else:
            st.info("No date column detected.")

    with f2:
        if cat_cols:
            region_col = st.selectbox("Filter by Category", ["(all)"] + cat_cols)
            if region_col != "(all)":
                unique_vals = sorted(df[region_col].dropna().unique().tolist())
                selected_vals = st.multiselect(f"Select {region_col} values", unique_vals, default=unique_vals)
                if selected_vals:
                    filtered_df = filtered_df[filtered_df[region_col].isin(selected_vals)]

    with f3:
        if numeric_cols:
            filter_col = st.selectbox("Numeric Range Filter", ["(none)"] + numeric_cols)
            if filter_col != "(none)":
                col_min = float(df[filter_col].min())
                col_max = float(df[filter_col].max())
                val_range = st.slider(f"{filter_col} range", col_min, col_max, (col_min, col_max), step=(col_max - col_min) / 100)
                filtered_df = filtered_df[
                    (filtered_df[filter_col] >= val_range[0]) &
                    (filtered_df[filter_col] <= val_range[1])
                ]

    st.caption(f"Showing **{len(filtered_df):,}** of **{len(df):,}** records after filtering.")

    # ── Data Preview ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>📋 Data Preview</h3></div>
    """, unsafe_allow_html=True)

    tab_preview, tab_stats = st.tabs(["📄 Raw Data", "📊 Summary Statistics"])

    with tab_preview:
        rows = st.slider("Rows to display", 5, min(200, len(filtered_df)), 20, key="preview_rows")
        st.dataframe(
            filtered_df.head(rows),
            use_container_width=True,
            height=350
        )
        st.download_button(
            "⬇️ Download Filtered CSV",
            filtered_df.to_csv(index=False),
            file_name="marine_filtered.csv",
            mime="text/csv"
        )

    with tab_stats:
        if numeric_cols:
            stats = compute_stats(filtered_df, numeric_cols)
            st.dataframe(stats, use_container_width=True)

    # ── Interactive Charts ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>📈 Interactive Charts</h3></div>
    """, unsafe_allow_html=True)

    chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter", "Box", "Histogram", "Heatmap"])

    c1, c2, c3 = st.columns(3)
    with c1:
        x_axis = st.selectbox("X Axis", (date_cols + numeric_cols + cat_cols), index=0)
    with c2:
        y_axis = st.selectbox("Y Axis", numeric_cols, index=0 if numeric_cols else 0)
    with c3:
        color_by = st.selectbox("Color By", ["(none)"] + cat_cols + numeric_cols)

    color_arg = None if color_by == "(none)" else color_by

    if st.button("🔄 Generate Chart", type="primary"):
        try:
            if chart_type == "Line":
                fig = px.line(filtered_df, x=x_axis, y=y_axis, color=color_arg,
                              title=f"{y_axis} over {x_axis}")
            elif chart_type == "Bar":
                plot_df = filtered_df.groupby(x_axis)[y_axis].mean().reset_index()
                fig = px.bar(plot_df, x=x_axis, y=y_axis, title=f"Avg {y_axis} by {x_axis}")
            elif chart_type == "Scatter":
                fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=color_arg,
                                 title=f"{y_axis} vs {x_axis}", opacity=0.65)
            elif chart_type == "Box":
                fig = px.box(filtered_df, x=color_arg or x_axis, y=y_axis,
                             title=f"{y_axis} Distribution")
            elif chart_type == "Histogram":
                fig = px.histogram(filtered_df, x=y_axis, color=color_arg,
                                   title=f"Distribution of {y_axis}", nbins=40, opacity=0.8)
            elif chart_type == "Heatmap":
                if cat_cols and date_cols:
                    hm = filtered_df.copy()
                    hm["Year"] = hm[date_cols[0]].dt.year
                    pivot = hm.pivot_table(values=y_axis, index=cat_cols[0], columns="Year", aggfunc="mean")
                    fig = px.imshow(pivot, title=f"{y_axis} Heatmap",
                                    color_continuous_scale=[[0, "#00BFA5"], [0.5, "#FFB300"], [1, "#E53935"]])
                else:
                    st.warning("Heatmap needs a date column and at least one category column.")
                    return

            fig = apply_theme(fig)
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Could not render chart: {e}")

    # ── Correlation Matrix ─────────────────────────────────────────────────────
    if len(numeric_cols) >= 2:
        with st.expander("🔗 Correlation Matrix"):
            corr = filtered_df[numeric_cols].corr().round(2)
            fig_corr = px.imshow(
                corr, text_auto=True,
                color_continuous_scale=[[0, "#E53935"], [0.5, "#061E3C"], [1, "#00BFA5"]],
                title="Pearson Correlation Matrix"
            )
            fig_corr = apply_theme(fig_corr)
            fig_corr.update_layout(height=420)
            st.plotly_chart(fig_corr, use_container_width=True)
