# US Federal Tax Depreciation Reconciliation Demo

This dependency-free Python demonstration reconciles asset details from labeled
plain-text emails, CSV files, and the first worksheet of `.xlsx` attachments. It
exports a deterministic JSON file and a calculation-by-calculation audit log.

> **Educational use only.** This is not tax advice, filing software, or a full
> implementation of US federal tax law. It must not be used to prepare a return.

## Run

From the project directory:

```powershell
python main.py
```

By default, the engine reads `data/emails/*.txt` and
`data/attachments/*.csv` / `*.xlsx`, then writes
`output/tax_inputs.json` and `output/audit_log.md`. Override directories with
`--data-dir` and `--output-dir`. The included ruleset supports tax year 2025
only; the CLI rejects other tax years.

Each asset needs a matching asset ID, cost, business-use percentage, placed-in-
service date in 2025, explicit method, 5- or 7-year recovery period, and an
explicit special-depreciation percentage. Email and attachment records merge
only by exact asset ID. Conflicting non-empty values stop the run rather than
silently choosing a source. The tool does not guess an asset class from its
description.

The sample data assumes, solely for demonstration, 5- or 7-year classes,
explicit business-use percentages, and 0% special depreciation. These are
fictional example inputs, not claims about eligibility or the correct
treatment of real property. The 101 unique sample assets are combined in the
single `data/attachments/sample_assets.csv` file.

## Supported rule scope

The bundled [`tax_lib/depreciation.py`](tax_lib/depreciation.py) implements the
2025 IRS Publication 946 MACRS GDS percentage schedules (Table A-1) for
explicitly supplied 5- and 7-year property using the 200% declining-balance,
half-year convention. The annual calculation is:

```text
business depreciable basis = cost x business use %
special allowance = basis x explicitly supplied special-depreciation %
MACRS deduction = (basis - special allowance) x applicable Table A-1 rate
```

The rule source is [IRS Publication 946 (2025)](https://www.irs.gov/publications/p946).
The `special_depreciation_pct` must be supplied by a qualified reviewer based
on the acquisition/placed-in-service facts and applicable election. The IRS
2025 rules include special-depreciation changes during the year; this demo
does **not** determine qualification, effective date eligibility, elections,
section 179, listed-property restrictions, or business-use qualification.
It rejects non-zero residual value for MACRS instead of applying an
inappropriate straight-line assumption.

Unsupported items include other recovery periods and conventions, ADS,
straight-line tax elections, section 179, bonus eligibility, mid-quarter
convention, dispositions, listed property rules, state tax, and special asset
classes. The ruleset is fixed and is not automatically updated when tax law or
IRS publications change. A tax professional must independently validate any
inputs and results. The bundled module is a local, inspectable rules adapter;
it is not a substitute for a maintained, externally validated tax library.

Amounts are represented as decimal strings in the JSON output. Displayed
currency values are rounded to cents using round-half-up; actual tax forms may
require different rounding or additional adjustments.

## Input handling

- **Emails:** one asset record per `.txt` file, using labeled fields such as
  `Asset ID: DEMO-001`, `Placed in Service Date: 2025-01-15`, and
  `Special Depreciation %: 0%`.
- **CSV:** common aliases include `Asset No`, `Purchase Price`,
  `Business Use %`, `Depreciation Method`, `Recovery Period Years`, and
  `Special Depreciation %`.
- **Excel:** standard, unencrypted `.xlsx` workbooks; only the first worksheet
  is read. Shared-string and inline-string cells, cached cell values,
  percentage styles, and common date formats are supported. Formula cells use
  only their cached value; the engine does not calculate spreadsheet formulas.
  `.xls`, macros, multiple worksheets, encrypted files, external links, and
  unusual workbook features are not supported. Workbook size is limited to
  20 MB uncompressed and 256 archive entries.

Unknown columns are ignored. Missing required values, malformed data, and
conflicting aliases are reported as errors. Each output asset records its
source file and row.

## LLM resilience and privacy

Reconciliation, tax-table lookup, calculation, and the audit math are
deterministic and do not depend on an LLM. The optional narrative prompt
contains no client asset data. If a cloud request fails, the router tries local
Ollama; if that is unavailable too, the JSON export and deterministic audit
still complete and record the fallback. Model prose is non-authoritative.

Configure an OpenAI-compatible HTTPS endpoint and optional Ollama instance:

```powershell
$env:TAX_CLOUD_BASE_URL = "https://api.example.com/v1"
$env:TAX_CLOUD_API_KEY = "..."
$env:TAX_CLOUD_MODEL = "model-name"
$env:TAX_LOCAL_URL = "http://127.0.0.1:11434"
$env:TAX_LOCAL_MODEL = "llama3"
```

The cloud URL must expose `/chat/completions`; the local URL must expose
Ollama's `/api/generate`. Requests use Python's standard library and a
three-second timeout. Keep credentials in environment variables; never commit
them or send real client data to an unapproved provider.

## Tests

```powershell
python -m unittest discover -s tests -v
```

Tests cover normalization, source reconciliation, `.xlsx` parsing, selected
2025 MACRS calculations, validation, generated outputs, and cloud-to-local
fallback behavior. They do not constitute a complete IRS certification suite.
