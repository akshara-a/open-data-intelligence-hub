# Neural Network Implementation with Documented Design Choices

## Overview
Binary image classification CNN that detects defective vs non-defective metal castings, with each architecture and training decision explicitly documented and justified.

## Dataset
Kaggle: Casting Product Image Data for Quality Inspection
- Non-defective (ok_front) = 0
- Defective (def_front) = 1

## How to Run
1. Install dependencies: pip install tensorflow numpy matplotlib scikit-learn pandas
2. Download the dataset from Kaggle and place it as casting_data/train and casting_data/test
3. Open notebooks/neural_network_design_choices.ipynb
4. Run all cells in order (Colab with GPU runtime recommended)

## Results
Original design (dropout=0.40): 95.7% test accuracy.
Bonus experiment (dropout=0.20): 98.3% test accuracy - see the notebook's Design Decision Table and Bonus Experiment section for full reasoning and comparison.

## Folder Structure
- notebooks/ - the full notebook with CNN implementation, documented design choices, training results, and bonus experiment
