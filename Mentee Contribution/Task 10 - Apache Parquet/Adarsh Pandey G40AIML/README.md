# Apache Parquet Demo Project

A small, self-contained project that demonstrates why Apache Parquet is used
in modern data engineering, by directly comparing it against CSV.

## Files

| File | Purpose |
|---|---|
| `parquet_demo.py` | Main script: generates data, writes CSV + Parquet (3 codecs), benchmarks read/write, inspects Parquet metadata |
| `requirements.txt` | Python dependencies |
| `Apache_Parquet_Report.docx` | Written report explaining the concepts and the experiment |

## Setup

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python parquet_demo.py
```

This will:
1. Generate a synthetic 200,000-row "sales order" dataset
2. Write it to `output/data.csv` and to three Parquet variants (snappy /
   gzip / uncompressed) in `output/`
3. Print write time, read time, and file size for each format
4. Show that reading only 2 of 9 columns from Parquet is much faster than
   from CSV (columnar pruning)
5. Print Parquet's internal schema and per-column compressed sizes
6. Save everything to `results_summary.csv`

Paste your own numbers from `results_summary.csv` into the "Results" section
of the report — exact timings/sizes depend on your machine.
