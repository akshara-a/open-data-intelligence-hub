# Setup Guide — Image Recognition System for Quality Control

## What's in this package
- `Image_Recognition_QC.ipynb` — the full notebook (EDA, baseline CNN, transfer learning, evaluation, export)
- `Business_Report.pdf` — non-technical summary for the case write-up
- `SETUP_GUIDE.md` — this file

## Option 1: Run in Google Colab (recommended, no installation needed)

1. Go to https://colab.research.google.com
2. File → Upload notebook → select `Image_Recognition_QC.ipynb`
3. Runtime → Change runtime type → select **GPU** (T4 is fine) for faster training
4. Run cells from top to bottom
5. When you reach the dataset download cell, you'll need a Kaggle API key:
   - Go to kaggle.com → click your profile picture → **Account**
   - Scroll to **API** → click **Create New Token** → this downloads `kaggle.json`
   - When the notebook prompts you to upload a file, upload `kaggle.json`
6. Everything else runs automatically — the notebook downloads the dataset, trains both models, evaluates them, and saves the final model.

## Option 2: Run locally (Jupyter/VS Code)

1. Install Python 3.10+ if you don't already have it
2. Create a virtual environment and install requirements:
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)
   source venv/bin/activate     (Mac/Linux)
   pip install -r requirements.txt
   ```
3. Install the Kaggle CLI and place your `kaggle.json` API key in the correct folder:
   - Windows: `C:\Users\<you>\.kaggle\kaggle.json`
   - Mac/Linux: `~/.kaggle/kaggle.json`
4. Launch Jupyter: `jupyter notebook` and open `Image_Recognition_QC.ipynb`
5. Run all cells (Cell → Run All)

## Option 3: Skip the Kaggle API — manual download

1. Go to https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product
2. Click **Download** (you'll need a free Kaggle account)
3. Rename the downloaded file to `casting_data.zip` and place it in the same folder as the notebook
4. Skip the "Kaggle API download" cell and run the "unzip" cell directly — it automatically checks for `casting_data.zip` if the Kaggle-named file isn't found

## requirements.txt

Save this as `requirements.txt` if running locally:

```
tensorflow>=2.15
numpy
pandas
matplotlib
seaborn
scikit-learn
kaggle
```

## Common issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: tensorflow` | Run `pip install tensorflow` (or use Colab, which has it pre-installed) |
| Kaggle download fails with 401 error | Your `kaggle.json` is missing or in the wrong folder — recheck step 3 above |
| Training is very slow | Switch to a GPU runtime in Colab (Runtime → Change runtime type → GPU) |
| Folder structure doesn't match `TRAIN_DIR`/`TEST_DIR` | Run the "os.walk" cell in Section 3 to print the real folder layout, then update the paths |
| Out of memory during training | Lower `BATCH_SIZE` from 32 to 16 in the preprocessing cell |

## Estimated run time
- On Colab GPU (T4): ~10–15 minutes for both models combined
- On CPU only: ~45–60 minutes
