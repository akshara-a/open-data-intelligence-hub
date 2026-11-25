# Legal Clause Classification and Entity Extraction

A beginner-friendly NLP project that analyzes contract text without using generative AI.

The project:

1. **Classifies legal clauses:** Indemnification, Limitation of Liability, Force Majeure, and Other.
2. **Extracts named entities:** Organizations (ORG), Dates (DATE), and Money (MONEY), including their character positions.
3. **Generates structured JSON output** containing clause classifications and extracted entities.

**Pipeline:**

Contract Text → Clause Splitting → Text Preprocessing → BERT Tokenization → BERT Embeddings → BiLSTM Classification → spaCy NER → JSON Output

## 1. Technologies Used

- Python 3.12.10
- PyTorch
- Hugging Face Transformers
- BERT (`bert-base-uncased`)
- BiLSTM
- spaCy
- Pandas and NumPy
- Scikit-learn
- Matplotlib and Seaborn

## 2. Project Structure

```text
legal_clause_project/
│
├── README.md
├── requirements.txt
├── common.py
├── model_tools.py
├── pipeline.py
│
├── 01_prepare_data.py
├── 02_explore_data.py
├── 03_preprocess_tokenize_embed.py
├── 04_train_and_evaluate.py
├── 05_named_entity_recognition.py
├── 06_pipeline_and_testing.py
├── 07_analyze_your_contract.py
│
├── data/
│   ├── dataset.csv
│   ├── synthetic_clauses.csv
│   └── sample_contract.txt
│
└── outputs/
    ├── metrics_report.txt
    ├── confusion_matrix.png
    ├── training_loss.png
    ├── class_balance.png
    ├── clause_length.png
    ├── sample_output.json
    └── your_contract_output.json
```

Additional intermediate datasets and generated files may also be created when the scripts are executed.

## 3. Installation and Setup

1. Install Python 3.9 to 3.12 and Visual Studio Code.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

4. Install the required libraries:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

5. Select the virtual environment as the Python interpreter in VS Code.

Internet access is required initially to download the BERT model and, if enabled, the LEDGAR dataset.

## 4. How to Run the Project

Execute the scripts in the following order:

```bash
python 01_prepare_data.py
python 02_explore_data.py
python 03_preprocess_tokenize_embed.py
python 04_train_and_evaluate.py
python 05_named_entity_recognition.py
python 06_pipeline_and_testing.py
python 07_analyze_your_contract.py
```

The seventh script can also accept a custom contract text file.

## 5. Dataset Description

The project uses a combination of real and synthetic contract clauses.

| Clause Category | Data Source |
|---|---|
| Indemnification | LEDGAR and synthetic data |
| Limitation of Liability | Synthetic data |
| Force Majeure | Synthetic data |
| Other | LEDGAR and synthetic data |

LEDGAR is a public dataset containing legal contract paragraphs. Synthetic examples are generated using templates and are not real contracts.

## 6. Results and Outputs

The project generates:

- Dataset exploration visualizations.
- BERT embeddings.
- A trained BiLSTM classification model.
- Classification evaluation metrics.
- A confusion matrix and training loss graph.
- Named entity extraction results.
- Structured JSON contract analysis output.

Refer to `outputs/metrics_report.txt` for the actual evaluation metrics.

## 7. Limitations

- Some clause categories rely on synthetic data.
- High scores on synthetic data do not guarantee performance on real-world contracts.
- NER accuracy has not been independently measured using a manually labelled entity dataset.
- OCR functionality is simulated rather than implemented using a real OCR engine.
- Clause segmentation uses a simple blank-line separation rule.
- The project is an educational prototype and is not a replacement for professional legal review.

## 8. Project Status

The project was executed and tested locally using Windows, Python 3.12.10, and a virtual environment.

All seven Python scripts were executed successfully.

The contract analysis script was tested using a sample contract. One execution checked five clauses and flagged three based on the model's confidence threshold.

Generated datasets, model files, evaluation reports, visualizations, and JSON outputs were produced during execution.

For actual model performance, refer to the generated evaluation report rather than assuming that successful execution indicates high real-world accuracy.
The contract analysis script was tested using a sample contract. One execution checked five clauses and flagged three based on the model's confidence threshold.

Generated datasets, model files, evaluation reports, visualizations, and JSON outputs were produced during execution.

For actual model performance, refer to the generated evaluation report rather than assuming that successful execution indicates high real-world accuracy.
