import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import os
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, r2_score

base = r'c:\Users\Harshitha\OneDrive\Desktop\Task-8-Customer-Segmentation'

print("=== OUTPUT FILES ===")
for f in sorted(os.listdir(os.path.join(base, 'outputs'))):
    fpath = os.path.join(base, 'outputs', f)
    size = os.path.getsize(fpath)
    print(f"  {f:45s} {size:>8,} bytes")

print()
print("=== IMAGE FILES ===")
for f in sorted(os.listdir(os.path.join(base, 'images'))):
    fpath = os.path.join(base, 'images', f)
    size = os.path.getsize(fpath)
    print(f"  {f:40s} {size:>8,} bytes")

print()
print("=== QUICK STATS ===")
df = pd.read_csv(os.path.join(base, 'outputs', 'clustered_customers.csv'))
print(f"  Clustered customers: {len(df)} rows")
print(f"  Clusters found: {sorted(df['Cluster'].unique())}")
counts = df['Cluster'].value_counts().sort_index().to_dict()
print(f"  Cluster distribution: {counts}")

seg = pd.read_csv(os.path.join(base, 'outputs', 'customer_segments.csv'), index_col=0)
if 'SegmentName' in seg.columns:
    print(f"  Segments: {seg['SegmentName'].tolist()}")

cls = pd.read_csv(os.path.join(base, 'outputs', 'classification_predictions.csv'))
print(f"  Classification predictions: {len(cls)} rows")
acc = accuracy_score(cls['Actual'], cls['Predicted'])
f1  = f1_score(cls['Actual'], cls['Predicted'], zero_division=0)
auc = roc_auc_score(cls['Actual'], cls['Probability'])
print(f"  Accuracy={acc:.4f} | F1={f1:.4f} | ROC-AUC={auc:.4f}")

reg = pd.read_csv(os.path.join(base, 'outputs', 'regression_predictions.csv'))
print(f"  Regression predictions: {len(reg)} rows")
r2_lr    = r2_score(reg['Actual_TotalSpending'], reg['LinearRegression_Predicted'])
r2_ridge = r2_score(reg['Actual_TotalSpending'], reg['Ridge_Predicted'])
print(f"  Linear Regression R2={r2_lr:.4f} | Ridge R2={r2_ridge:.4f}")

print()
print("All outputs verified successfully!")
