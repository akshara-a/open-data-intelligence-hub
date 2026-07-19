Customer Segmentation with Actionable Business Insights
=====================================================

Project: Customer Segmentation with Actionable Business Insights

This mini-project generates a synthetic customer dataset, performs preprocessing, exploratory data analysis (EDA), K-Means clustering, regression (Linear & Ridge), classification (Logistic Regression), hyperparameter tuning, model evaluation, visualizations, and produces business recommendations.

Structure
---------
- `data/` - generated dataset (`customer_data.csv`)
- `models/` - serialized trained models
- `scripts/generate_data.py` - script to generate the synthetic dataset
- `src/` - Python modules: preprocessing, EDA, clustering, regression, classification, utils
- `run_pipeline.py` - orchestrates the full pipeline
- `requirements.txt` - Python dependencies

Quickstart
----------
1. Create and activate a Python environment (Python 3.8+).
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Generate dataset:

```powershell
python scripts/generate_data.py
```

4. Run the pipeline:

```powershell
python run_pipeline.py
```

Files to inspect
- `src/data_processing.py` - data loading and preprocessing
- `src/eda.py` - exploratory analysis and plots
- `src/clustering.py` - K-Means clustering workflow
- `src/regression.py` - Linear & Ridge regression experiments
- `src/classification.py` - Logistic regression classification and tuning

Author: College mini-project style (clean, commented code)


Run (step-by-step)
-------------------
Follow these commands from the project root (`c:\Users\joshi\Downloads\cust recomentation`):

1. Create a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Or (Windows CMD):

```cmd
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Generate the synthetic dataset (if not already present):

```powershell
python scripts/generate_data.py
```

4. Run the full pipeline (preprocessing, EDA, clustering, models):

```powershell
python run_pipeline.py
```

5. Start the Streamlit app for interactive exploration:

```powershell
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

Outputs
-------
- Generated dataset: `data/customer_data.csv`
- EDA plots & summaries: `outputs/plots/`
- Clustered customers: `outputs/clustered_customers.csv`
- Trained models: `models/` (joblib files)

Notes
-----
- Use the virtual environment to avoid dependency conflicts.
- Re-run `python scripts/generate_data.py` to create a fresh synthetic dataset.
- If Streamlit fails to start, ensure the port is free or run with `--server.port <port>`.

