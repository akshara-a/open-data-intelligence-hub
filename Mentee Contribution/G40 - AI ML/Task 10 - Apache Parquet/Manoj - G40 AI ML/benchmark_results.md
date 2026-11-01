# Task 10: Apache Parquet Performance & Compression Benchmark Report

## 1. File Size & Speed Comparison

| Format/Codec     |   File Size (MB) | Write Time (s)   | Read Time (s)   |   Space Saving vs CSV (%) |
|:-----------------|-----------------:|:-----------------|:----------------|--------------------------:|
| Raw CSV          |             3.44 | N/A              | N/A             |                      0    |
| Parquet (snappy) |             1.26 | 0.0553           | 0.0212          |                     63.36 |
| Parquet (gzip)   |             0.92 | 0.1967           | 0.0203          |                     73.42 |
| Parquet (zstd)   |             0.89 | 0.0561           | 0.0193          |                     74.26 |
| Parquet (none)   |             1.81 | 0.0499           | 0.0165          |                     47.48 |

## 2. Key Findings
- **Column Pruning Speedup:** Parquet loaded selected columns **6.40x faster** than CSV.
- **Best Compression Codec:** `zstd` provided optimal balance between storage savings and read/write speed.
