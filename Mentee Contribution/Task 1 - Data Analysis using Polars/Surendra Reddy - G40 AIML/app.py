import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# ─── Page Setup ───────────────────────────
st.set_page_config(
    page_title="Repo Intelligence Engine",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Most Active Repository Intelligence Engine")
st.markdown("**Dataset:** GitHub Archive | **Stack:** Polars · Pandas · NumPy · Matplotlib")
st.markdown("---")

# ─── Load Data ────────────────────────────
@st.cache_data
def load_data():
    rows = []

    with open("gharchive_small.json", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            rows.append({
                "event_type" : event.get("type", ""),
                "actor"      : event.get("actor", {}).get("login", ""),
                "repo_name"  : event.get("repo",  {}).get("name",  ""),
                "created_at" : event.get("created_at", "")
            })

    df = pl.DataFrame(rows)
    return df

# ─── Score Repos ──────────────────────────
@st.cache_data
def compute_scores(_df):
    repo_counts = (
        _df
        .group_by("repo_name")
        .agg([
            pl.len().alias("total_events"),
            pl.col("actor").n_unique().alias("unique_contributors"),
            (pl.col("event_type") == "WatchEvent").sum().alias("stars"),
            (pl.col("event_type") == "ForkEvent").sum().alias("forks"),
            (pl.col("event_type") == "PushEvent").sum().alias("pushes"),
            (pl.col("event_type") == "PullRequestEvent").sum().alias("pull_requests"),
        ])
        .sort("total_events", descending=True)
    )

    repo_df = repo_counts.to_pandas()

    def normalize(column):
        col = column.to_numpy(dtype=float)
        min_val = col.min()
        max_val = col.max()
        if max_val == min_val:
            return np.zeros_like(col)
        return (col - min_val) / (max_val - min_val) * 100

    n_events       = normalize(repo_df["total_events"])
    n_contributors = normalize(repo_df["unique_contributors"])
    n_stars        = normalize(repo_df["stars"])
    n_forks        = normalize(repo_df["forks"])

    score = (
        0.40 * n_events       +
        0.30 * n_contributors +
        0.20 * n_stars        +
        0.10 * n_forks
    )

    repo_df["score"] = np.round(score, 2)
    repo_df = repo_df.sort_values("score", ascending=False).reset_index(drop=True)
    repo_df.index += 1
    return repo_df

# ─── Load ─────────────────────────────────
with st.spinner("Loading GitHub Archive data..."):
    df = load_data()
    repo_df = compute_scores(df)

# ─── Metric Cards ─────────────────────────
st.subheader("📊 Dataset Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Events",  f"{len(df):,}")
col2.metric("Unique Repos",  f"{df['repo_name'].n_unique():,}")
col3.metric("Unique Users",  f"{df['actor'].n_unique():,}")
col4.metric("Event Types",   f"{df['event_type'].n_unique()}")
st.markdown("---")

# ─── Slider + Table ───────────────────────
st.subheader("🏆 Most Active Repositories")
top_n  = st.slider("How many top repos to show?", 5, 30, 10)
top_df = repo_df.head(top_n)
st.dataframe(
    top_df[["repo_name","score","total_events","unique_contributors","stars","forks","pull_requests"]],
    use_container_width=True
)
st.markdown("---")

# ─── Charts Row 1 ─────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Repos by Score")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_df["repo_name"][::-1], top_df["score"][::-1], color="steelblue")
    ax.set_xlabel("Composite Score")
    ax.set_title(f"Top {top_n} Most Active Repositories")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Event Types Distribution")
    event_counts = df.group_by("event_type").len().to_pandas()
    event_counts = event_counts.sort_values("len", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(
        event_counts["len"],
        labels=event_counts["event_type"],
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.75,
        labeldistance=1.15
    )
    ax.set_title("GitHub Event Types", fontsize=14, pad=20)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ─── Charts Row 2 ─────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Stars vs Forks")
    # Filter to repos with at least some activity
    scatter_df = repo_df[(repo_df["stars"] > 0) | (repo_df["forks"] > 0)]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(scatter_df["stars"], scatter_df["forks"], alpha=0.6, color="coral", s=60)
    ax.set_xlabel("Stars (WatchEvents)")
    ax.set_ylabel("Forks")
    ax.set_title("Stars vs Forks per Repository")
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Top Repos by Contributors")
    fig, ax = plt.subplots(figsize=(8, 5))
    top_contrib = repo_df.head(10)
    ax.bar(
        range(len(top_contrib)),
        top_contrib["unique_contributors"],
        color="mediumseagreen"
    )
    ax.set_xticks(range(len(top_contrib)))
    ax.set_xticklabels(
        [r.split("/")[1][:12] for r in top_contrib["repo_name"]],
        rotation=45, ha="right"
    )
    ax.set_ylabel("Unique Contributors")
    ax.set_title("Community Size — Top 10 Repos")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ─── Search Box ───────────────────────────
st.subheader("Search a Repository")
search = st.text_input("Type a repo name to search:")
if search:
    result = repo_df[repo_df["repo_name"].str.contains(search, case=False, na=False)]
    if len(result) > 0:
        st.dataframe(result[["repo_name","score","total_events","unique_contributors","stars","forks"]])
    else:
        st.warning("No repository found with that name.")

st.markdown("---")

# ─── Download Button ──────────────────────
st.subheader("Download Results")
csv = repo_df.to_csv(index=True)
st.download_button(
    label="Download repo_scores.csv",
    data=csv,
    file_name="repo_scores.csv",
    mime="text/csv"
)

st.markdown("---")
st.markdown("**Project:** Most Active Repository Intelligence Engine | **Dataset:** GH Archive | **Stack:** Polars · Pandas · NumPy · Matplotlib")
