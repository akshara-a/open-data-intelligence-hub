WHAT WAS FIXED
================
The previous training run stayed near 16.67% accuracy, which is random chance for six classes.
This corrected project changes:
1. Automatic NEU-DET dataset discovery.
2. Recreates split CSV files so stale absolute paths cannot be reused.
3. Validates every image and prints class counts.
4. Uses 96x96 images for much faster CPU training.
5. Uses mild augmentation instead of stronger augmentation.
6. Uses a more suitable baseline CNN with Flatten.
7. Uses a lower learning rate (0.0003).
8. Saves the best model using validation accuracy.
9. Stops if a model still stays below 30% validation accuracy.

IMPORTANT BEFORE TRAINING
=========================
Delete old generated files from these folders if they exist:
- models
- results

Do NOT delete:
- data/raw/NEU-DET

Then run:
1. python -m src.train

Expected sanity-check output should show:
- Image batch shape: (32, 96, 96, 3)
- Image range: 0.0 to 1.0
- Labels from 0 to 5

If you still get a dataset error, send the exact output of:
Get-ChildItem -Path .\data -Recurse -Directory | Select-Object FullName
