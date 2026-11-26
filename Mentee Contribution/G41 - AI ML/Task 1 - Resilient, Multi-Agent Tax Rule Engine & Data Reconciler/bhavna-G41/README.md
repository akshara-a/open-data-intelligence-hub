# Financial Tax Processing System

## 1. Project Overview
The Financial Tax Processing System is an AI-assisted, rule-based application designed to automate financial asset tax depreciation processing.

It extracts asset information from email inputs, validates the extracted data, identifies applicable tax rules, calculates depreciation, generates reasoning and produces structured tax reports.

## 2. Problem Statement
Manual tax depreciation processing requires significant time and effort. Incorrect asset classification, missing information and inconsistent calculations can lead to errors.

This project aims to automate the initial processing and identify cases that require human verification.

## 3. Objectives
- Extract financial asset information from emails.
- Validate and normalize extracted data.
- Support jurisdiction-based tax rules.
- Calculate asset depreciation.
- Generate explanations for calculation results.
- Identify records requiring manual review.
- Generate JSON reports and audit logs.
- Support batch processing.

## 4. Technologies Used
- Python
- JSON
- Pandas (if used in the implementation)
- Pytest
- VS Code
- Git and GitHub

## 5. Project Architecture

The project consists of the following modules:

1. Ingestion Agent – Extracts asset information.
2. Validation Module – Validates input data.
3. Reasoning Agent – Loads tax rules and performs depreciation calculations.
4. Supervisor Agent – Coordinates the processing workflow.
5. Batch Processor – Processes multiple asset records.
6. Audit Logging – Maintains processing records.

## 6. Supported Tax Processing
- India: Written Down Value (WDV) depreciation for configured assets.
- US: Basic 5-year MACRS half-year calculation structure.

Unsupported or uncertain classifications are sent for manual review.

## 7. How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the main application:

```bash
python main.py
```

Run batch processing:

```bash
python -m supervisor_agent.batch_processor
```

Run automated tests:

```bash
python -m pytest -q
```

## 8. Output
The system generates:
- final_tax_report.json
- batch_tax_report.json
- Audit logs

## 9. Limitations
- Only configured tax rules are supported.
- Advanced tax deductions and exemptions are not implemented.
- Some asset classifications require human verification.
- Tax rules must be independently verified before real-world filing.

## 10. Future Scope
- Add more asset categories.
- Expand jurisdiction-specific tax rules.
- Integrate a database.
- Develop a web-based dashboard.
- Add PDF and Excel report generation.
- Improve automated asset classification.

## 11. Disclaimer
This project is an educational prototype. Its outputs are not a substitute for professional tax advice or verified tax filing calculations.