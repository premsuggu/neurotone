# Project NeuroTone
A smartphone-based screening tool for Parkinson's Disease using voice acoustics (Jitter, Shimmer, HNR).

## Current Architecture
- `data/`
  - `processed/`
    - `healthy/`
    - `pd/`
  - `raw/`
    - `italian_dataset/`
    - `neurovoz/`
    - `uci_parkinsons/`
- `src/`
  - `setup_dirs.py`
- `requirements.txt`

## Current Status
Phase 3: XGBoost Model Trained and Evaluated. Item 2: Feature Importance Bar Chart generated. Item 3: Individual Patient Score Breakdowns (Waterfall Plots) generated. Item 4: Confusion Matrix and ROC Curve generated. Item 5: Raw Signal Comparison Box Plots generated. All 5 Visual Pitch Assets Completed! Comprehensive Project Report compiled to docs/report.pdf.

## Data Insights
- **UCI Parkinson's Dataset**: 
  - **Feature Matrix Shape**: (195, 22)
  - **Class Imbalance**: The target variable `status` has a significant imbalance: 147 positive cases (PD) vs 48 negative cases (Healthy).
  - **Baseline Random Forest Performance**: Average AUC: 0.9622, Average Sensitivity: 0.9522, Average Specificity: 0.6933.
  - **XGBoost Performance**: Average AUC: 0.9738, Average Sensitivity: 0.9524, Average Specificity: 0.8356.
