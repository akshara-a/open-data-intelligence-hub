**Student:** Samiksha G  
**Batch:** G41 AI/ML  
**Task:** Task 3 - Legal Clause Classification and Entity Extraction  
**Submission folder:** C:\Users\HP\Downloads\legal-clause-ai (1)\legal-clause-ai  
**What I completed:** A CUAD-based NLP pipeline (BPE, Word2Vec, CRF) that extracts ORG, DATE and MONEY spans with exact offsets and classifies risk clauses, with a Flask backend and web frontend.  
**Testing:** Evaluated on 102 held-out contracts and ran the API on sample contracts. Limitations: some labels are keyword- or rule-based, and a CRF is used instead of a BiLSTM.  
**How to run:** Python 3.10-3.12. In a PowerShell terminal, from the folder that contains `requirements.txt`:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    cd backend
    python app.py

Then open http://127.0.0.1:5000 in a browser. The trained models are included, so no training is needed. If activation is blocked, run `Set-ExecutionPolicy -Scope Process Bypass` first.
