"""
Apache Parquet Demo Project
============================
A hands-on comparison of Apache Parquet vs. CSV that demonstrates:
  1. Writing the same dataset to CSV and to Parquet (with different codecs)
  2. Comparing resulting file sizes on disk
  3. Comparing write and read speed
  4. Demonstrating "columnar pruning" -- reading only the columns you need
  5. Inspecting Parquet's embedded schema and metadata

Requirements (install once):
    pip install pandas pyarrow

Run:
    python parquet_demo.py

Everything the script measures is printed to the console AND written to
results_summary.csv so it can be pasted into the report.
"""

import os
import time
import numpy as np
import pandas as pd

# pyarrow is the engine pandas uses under the hood to read/write Parquet.
# It also lets us look at low-level Parquet metadata directly.
import pyarrow as pa
import pyarrow.parquet as pq

OUTPUT_DIR = "output"
N_ROWS = 200_000          # size of the synthetic dataset
RANDOM_SEED = 42


def make_dataset(n_rows: int) -> pd.DataFrame:
    """Create a synthetic 'sales records' dataset with a realistic mix
    of column types (int, float, string/category, datetime, bool)."""
    rng = np.random.default_rng(RANDOM_SEED)

    regions = np.array(["North", "South", "East", "West"])
    products = np.array([f"SKU-{i:04d}" for i in range(500)])

    df = pd.DataFrame({
        "order_id": np.arange(1, n_rows + 1),
        "order_date": pd.date_range("2023-01-01", periods=n_rows, freq="min"),
        "region": rng.choice(regions, size=n_rows),
        "product_sku": rng.choice(products, size=n_rows),
        "quantity": rng.integers(1, 50, size=n_rows),
        "unit_price": rng.uniform(2.5, 500.0, size=n_rows).round(2),
        "discount_pct": rng.uniform(0, 0.3, size=n_rows).round(3),
        "is_returned": rng.random(size=n_rows) < 0.04,
    })
    df["total_price"] = (df["quantity"] * df["unit_price"] * (1 - df["discount_pct"])).round(2)
    return df


def timed(fn, *args, **kwargs):
    """Run fn and return (result, elapsed_seconds)."""
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def file_size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Generating synthetic dataset with {N_ROWS:,} rows...")
    df = make_dataset(N_ROWS)
    print(df.head(), "\n")
    print(df.dtypes, "\n")

    paths = {
        "csv": os.path.join(OUTPUT_DIR, "data.csv"),
        "parquet_snappy": os.path.join(OUTPUT_DIR, "data_snappy.parquet"),
        "parquet_gzip": os.path.join(OUTPUT_DIR, "data_gzip.parquet"),
        "parquet_none": os.path.join(OUTPUT_DIR, "data_uncompressed.parquet"),
    }

    results = []

    # ---- 1. WRITE benchmarks -------------------------------------------------
    _, t = timed(df.to_csv, paths["csv"], index=False)
    results.append(("CSV", "n/a", "write", t, file_size_mb(paths["csv"])))

    _, t = timed(df.to_parquet, paths["parquet_snappy"], engine="pyarrow", compression="snappy", index=False)
    results.append(("Parquet", "snappy", "write", t, file_size_mb(paths["parquet_snappy"])))

    _, t = timed(df.to_parquet, paths["parquet_gzip"], engine="pyarrow", compression="gzip", index=False)
    results.append(("Parquet", "gzip", "write", t, file_size_mb(paths["parquet_gzip"])))

    _, t = timed(df.to_parquet, paths["parquet_none"], engine="pyarrow", compression=None, index=False)
    results.append(("Parquet", "none", "write", t, file_size_mb(paths["parquet_none"])))

    # ---- 2. FULL READ benchmarks ----------------------------------------------
    _, t = timed(pd.read_csv, paths["csv"])
    results.append(("CSV", "n/a", "full read", t, file_size_mb(paths["csv"])))

    _, t = timed(pd.read_parquet, paths["parquet_snappy"], engine="pyarrow")
    results.append(("Parquet", "snappy", "full read", t, file_size_mb(paths["parquet_snappy"])))

    # ---- 3. COLUMNAR PRUNING: read only 2 of 9 columns ------------------------
    cols = ["region", "total_price"]

    _, t = timed(lambda: pd.read_csv(paths["csv"], usecols=cols))
    results.append(("CSV", "n/a", f"read {len(cols)} cols", t, file_size_mb(paths["csv"])))

    _, t = timed(pd.read_parquet, paths["parquet_snappy"], engine="pyarrow", columns=cols)
    results.append(("Parquet", "snappy", f"read {len(cols)} cols", t, file_size_mb(paths["parquet_snappy"])))

    # ---- 4. Print results table -------------------------------------------------
    results_df = pd.DataFrame(results, columns=["format", "codec", "operation", "seconds", "file_size_mb"])
    results_df["seconds"] = results_df["seconds"].round(4)
    results_df["file_size_mb"] = results_df["file_size_mb"].round(3)
    print("\n=== RESULTS SUMMARY ===")
    print(results_df.to_string(index=False))
    results_df.to_csv("results_summary.csv", index=False)

    # ---- 5. Inspect Parquet's embedded schema & metadata -----------------------
    print("\n=== PARQUET FILE METADATA (data_snappy.parquet) ===")
    pf = pq.ParquetFile(paths["parquet_snappy"])
    print(pf.schema)
    meta = pf.metadata
    print(f"\nrows: {meta.num_rows}, row groups: {meta.num_row_groups}, "
          f"created_by: {meta.created_by}")
    rg0 = meta.row_group(0)
    print(f"\nRow group 0 has {rg0.num_columns} column chunks. Per-column compressed size:")
    for i in range(rg0.num_columns):
        col = rg0.column(i)
        print(f"  {col.path_in_schema:15s} compression={col.compression:8s} "
              f"compressed={col.total_compressed_size/1024:8.1f} KB")

    # ---- 6. Compression ratio summary ------------------------------------------
    csv_size = file_size_mb(paths["csv"])
    print("\n=== COMPRESSION RATIO vs CSV ===")
    for name, path in [("snappy", paths["parquet_snappy"]),
                        ("gzip", paths["parquet_gzip"]),
                        ("none", paths["parquet_none"])]:
        size = file_size_mb(path)
        print(f"  {name:8s}: {size:7.3f} MB   ({csv_size / size:.2f}x smaller than CSV)")


if __name__ == "__main__":
    main()
