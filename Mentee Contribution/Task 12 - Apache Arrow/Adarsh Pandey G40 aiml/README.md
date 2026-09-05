# Apache Arrow Project

A small, self-contained PyArrow project demonstrating core Arrow workflows:
building an in-memory table, writing it to Arrow IPC (`.arrow`) and
Parquet (`.parquet`) formats, filtering, and aggregation.

## Project structure

```
apache-arrow-project/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── arrow_ops.py    # core Arrow logic (build/read/write/filter/aggregate)
│   └── main.py         # pipeline entrypoint
├── data/                # generated .arrow / .parquet files land here
└── tests/
    └── test_arrow_ops.py
```

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

This will:
1. Build a sample `employees` table (10 rows, 6 columns).
2. Write `data/employees.arrow` (Arrow IPC / Feather format).
3. Write `data/employees.parquet`.
4. Filter the `IT` department and write `data/it_employees.parquet`.
5. Read all three files back and print a verification report, including
   average salary and headcount per department.

## Test

```bash
pytest tests/
```

## What each format is for

| File | Format | Use case |
|---|---|---|
| `employees.arrow` | Arrow IPC (Feather v2) | Fast, zero-copy reads; ideal for passing data between processes or languages |
| `employees.parquet` | Apache Parquet | Columnar, compressed, disk-efficient storage for analytics |
| `it_employees.parquet` | Apache Parquet | Filtered subset — demonstrates `pyarrow.compute` filtering |

## Extending this project

- Swap the hard-coded sample data in `build_employees_table()` for a real
  CSV/database source.
- Add more compute transforms in `arrow_ops.py` (sorting, joins, window functions).
- Use `pyarrow.dataset` if you need to scale to multi-file, partitioned datasets.
