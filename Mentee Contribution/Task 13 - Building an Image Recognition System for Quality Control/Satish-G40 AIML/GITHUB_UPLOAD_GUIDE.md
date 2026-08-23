# GitHub Upload Guide - Reduced File Size

This guide explains how to upload this project to GitHub with minimal file size.

## 📦 File Size Reduction

### What's Excluded (in `.gitignore`)
- `data/` folder (6,633 images - users download from Kaggle)
- `models/` folder (generated after training)
- `reports/` folder (generated during training)
- Jupyter cache files
- Python cache files

### GitHub Upload Size
- ✅ Source code only: **~100 KB**
- ✅ Notebooks: **~200-300 KB**
- ✅ README & docs: **~50 KB**
- **Total: ~500 KB** (instead of 1+ GB!)

---

## 🚀 Steps to Upload to GitHub

### 1. Initialize Git Repository
```bash
cd c:\Users\USER\Downloads\imageRecog
git init
git config user.name "Your Name"
git config user.email "your.email@gmail.com"
```

### 2. Add Files (Excluding Large Folders)
```bash
git add .
git status  # Should NOT show data/, models/, reports/
```

### 3. Create First Commit
```bash
git commit -m "Initial commit: Casting defect detection CNN project"
```

### 4. Create GitHub Repository
- Go to: https://github.com/new
- Create repository: `casting-defect-detection`
- Do NOT add README, .gitignore, license (you already have these locally)

### 5. Push to GitHub
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/casting-defect-detection.git
git push -u origin main
```

---

## 📋 Project Structure on GitHub

After upload, users will see:
```
casting-defect-detection/
├── .gitignore                  # Excludes large folders
├── README.md                   # Setup instructions
├── requirements.txt            # Dependencies
├── notebooks/
│   ├── casting_defect_detection.ipynb        # Full version (with outputs)
│   └── casting_defect_detection_clean.ipynb  # Clean version (no outputs) ⭐
├── demo.py                     # Test dataset structure
├── quick_start.py              # Validate dataset
├── run_on_colab.py            # Launch on Google Colab
└── (data/, models/, reports/ folders - empty or excluded)
```

---

## 👨‍💻 Instructions for Users Cloning from GitHub

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/casting-defect-detection.git
cd casting-defect-detection
```

### 2. Download Dataset
1. Go to: https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product
2. Extract to:
   ```
   data/train/ok_front/
   data/train/def_front/
   data/test/ok_front/
   data/test/def_front/
   ```

### 3. Install Dependencies
```bash
# For Python 3.11/3.12:
pip install -r requirements.txt

# For Python 3.14:
pip install numpy matplotlib scikit-learn seaborn Pillow jupyter ipykernel
```

### 4. Run Notebook
**Option A: Google Colab (Recommended)**
```
1. Go to: https://colab.research.google.com
2. Upload: notebooks/casting_defect_detection_clean.ipynb
3. Run cells
```

**Option B: Local Jupyter**
```bash
python -m jupyter notebook notebooks/casting_defect_detection_clean.ipynb
```

---

## 📊 File Size Comparison

| Scenario | Size |
|----------|------|
| Full project with data | ~1-2 GB |
| **GitHub upload (with .gitignore)** | **~500 KB** ✅ |
| Notebook with outputs | ~50-100 MB |
| **Clean notebook (no outputs)** | **~500 KB** ✅ |

---

## ✅ Optimization Tips

### Already Done:
- ✅ `.gitignore` excludes data/, models/, reports/
- ✅ Clean notebook (`casting_defect_detection_clean.ipynb`) - No cell outputs
- ✅ Small Python helper scripts
- ✅ Comprehensive README with setup instructions

### Optional Further Optimization:
```bash
# Remove original large notebook if needed
rm notebooks/casting_defect_detection.ipynb

# Keep only clean version
git add notebooks/casting_defect_detection_clean.ipynb
git commit -m "Use lightweight clean notebook version"
git push
```

---

## 🎯 GitHub Repository Structure

```
GitHub Repo (500 KB)
│
├── README.md (500 KB section on setup)
├── requirements.txt 
├── .gitignore ← KEY: Excludes large files
│
├── notebooks/
│   └── casting_defect_detection_clean.ipynb ← Use this!
│
├── demo.py
├── quick_start.py
└── GitHub_UPLOAD_GUIDE.md ← This file
```

---

## 🚀 Next Steps

1. **Remove large notebook** (optional):
   ```bash
   git rm notebooks/casting_defect_detection.ipynb
   ```

2. **Commit cleaned-up version**:
   ```bash
   git add -A
   git commit -m "Cleanup: remove large notebook outputs"
   git push origin main
   ```

3. **Users download** → Get ~500 KB repo
4. **Users add dataset** → Their storage, not GitHub
5. **Users run training** → On their machine or Google Colab

---

## 💾 Summary

- **GitHub Size**: 500 KB (optimal!)
- **User Experience**: Clear setup instructions
- **No Data Loss**: All code & docs preserved
- **Scalable**: Users add their own data from Kaggle

Ready to upload! 🎉
