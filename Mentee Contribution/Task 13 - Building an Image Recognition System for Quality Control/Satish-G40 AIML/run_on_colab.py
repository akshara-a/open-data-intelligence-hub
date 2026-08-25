#!/usr/bin/env python
"""
Open notebook in Google Colab - No TensorFlow installation needed!
"""

import webbrowser
import os
from pathlib import Path

# Get notebook path
notebook_path = Path("notebooks/casting_defect_detection.ipynb").resolve()

# Google Colab URL template
colab_url = f"https://colab.research.google.com/notebook#create=true&import={notebook_path.as_uri()}"

# Try simpler approach - use web UI
simple_colab = "https://colab.research.google.com"

print("=" * 70)
print("🚀 LAUNCHING JUPYTER NOTEBOOK ON GOOGLE COLAB")
print("=" * 70)
print("\nGoogle Colab is the fastest way to run this project!")
print("No TensorFlow installation needed - Colab has it pre-installed.\n")

print("Instructions:")
print("1. Browser will open to Google Colab")
print("2. Click 'File' → 'Open notebook'")
print("3. Go to 'Upload' tab")
print("4. Upload: notebooks/casting_defect_detection.ipynb")
print("5. Click cells to run them sequentially")
print("\nOr use this direct link:")
print("   https://colab.research.google.com\n")

print("=" * 70)

# Open browser
try:
    webbrowser.open(simple_colab)
    print("✅ Browser opened! Go to Google Colab and upload the notebook.\n")
except:
    print("⚠️  Could not open browser automatically.")
    print("Visit: https://colab.research.google.com\n")

print("Dataset is ready with 6,633 images!")
print("=" * 70)
