"""
Casting Quality Inspection package.

This package contains the production-style source code for the
Automated Casting Defect Detection project:

- config.py        : centralized configuration
- utils.py          : logging, validation, reproducibility helpers
- data_loader.py     : dataset loading + tf.data pipeline
- data_analysis.py   : dataset exploration helpers (used by the notebook)
- model.py           : CNN architecture definition
- train.py           : training pipeline (entry point: python -m src.train)
- evaluate.py        : test-set evaluation + threshold analysis
- predict.py         : single-image prediction (CastingDefectPredictor)
"""

__version__ = "1.0.0"
