"""
Main analysis pipeline for Species Distribution Pattern Analysis.

Run: python analyze.py
"""

import json
from pathlib import Path

from src.data_cleaning import clean_occurrence_data, get_cleaning_summary, load_raw_data
from src.eda import eda_summary
from src.hotspot import create_hotspot_map, detect_hotspots, summarize_hotspots
from src.mapping import create_occurrence_map, save_map
from src.richness_map import create_richness_map
from src.visualizations import generate_all_visualizations


DATA_PATH = Path("occurrence.csv")
OUTPUT_DIR = Path("outputs")
CLEAN_DATA_PATH = OUTPUT_DIR / "cleaned_occurrence.csv"
SUMMARY_PATH = OUTPUT_DIR / "analysis_summary.json"


def run_analysis() -> dict:
    """Execute the full analysis workflow and save outputs."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "maps").mkdir(exist_ok=True)
    (OUTPUT_DIR / "figures").mkdir(exist_ok=True)

    print("Loading data...")
    raw_df = load_raw_data(DATA_PATH)

    print("Cleaning data...")
    clean_df = clean_occurrence_data(raw_df)
    clean_df.to_csv(CLEAN_DATA_PATH, index=False)
    cleaning = get_cleaning_summary(raw_df, clean_df)

    print("Running EDA...")
    eda = eda_summary(clean_df)

    print("Generating visualizations...")
    figure_paths = generate_all_visualizations(clean_df)

    print("Creating occurrence map...")
    occurrence_map = create_occurrence_map(clean_df, sample_size=5000, with_popups=False)
    save_map(occurrence_map, OUTPUT_DIR / "maps" / "occurrence_map.html")

    print("Creating richness map...")
    richness_map = create_richness_map(clean_df)
    save_map(richness_map, OUTPUT_DIR / "maps" / "richness_map.html")

    print("Detecting hotspots (DBSCAN)...")
    clustered = detect_hotspots(clean_df)
    hotspot_summary = summarize_hotspots(clustered)
    hotspot_map = create_hotspot_map(clustered, hotspot_summary)
    save_map(hotspot_map, OUTPUT_DIR / "maps" / "hotspot_map.html")

    summary = {
        "cleaning": cleaning,
        "eda": {
            "total_records": eda["total_records"],
            "total_unique_species": eda["total_unique_species"],
            "top_10_species": eda["top_10_species"],
            "taxonomic_summary": eda["taxonomic_summary"],
        },
        "hotspots": hotspot_summary.head(10).to_dict(orient="records"),
        "outputs": {
            "cleaned_data": str(CLEAN_DATA_PATH),
            "figures": [str(p) for p in figure_paths],
            "maps": [
                str(OUTPUT_DIR / "maps" / "occurrence_map.html"),
                str(OUTPUT_DIR / "maps" / "richness_map.html"),
                str(OUTPUT_DIR / "maps" / "hotspot_map.html"),
            ],
        },
    }

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    clustered.to_csv(OUTPUT_DIR / "clustered_occurrence.csv", index=False)
    hotspot_summary.to_csv(OUTPUT_DIR / "hotspot_summary.csv", index=False)

    print("\n=== Analysis Complete ===")
    print(f"Records (clean): {cleaning['clean_records']:,}")
    print(f"Unique species: {eda['total_unique_species']:,}")
    print(f"Hotspot clusters: {len(hotspot_summary)}")
    print(f"Summary saved to: {SUMMARY_PATH}")

    return summary


if __name__ == "__main__":
    run_analysis()
