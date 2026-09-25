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
  - `clean_uci_data.py`
  - `download_uci.py`
  - `evaluation.py`
  - `train_rf.py`
  - `train_xgb.py`
  - `predict_risk.py`
  - `generate_report.py`
  - `plotter/`
- `requirements.txt`

## Current Status
Phase 3.5: Continuous Probability Risk Scoring & 3-Tier Clinical Stratification Implemented (`src/predict_risk.py`). All 5 Visual Pitch Assets Completed. Comprehensive Project Report updated and compiled to `docs/report.pdf`.

## Data Insights
- **UCI Parkinson's Dataset**: 
  - **Feature Matrix Shape**: (195, 22)
  - **Class Imbalance**: The target variable `status` has a significant imbalance: 147 positive cases (PD) vs 48 negative cases (Healthy).
  - **Baseline Random Forest Performance**: Average AUC: 0.9622, Average Sensitivity: 0.9522, Average Specificity: 0.6933.
  - **XGBoost Performance**: Average AUC: 0.9738, Average Sensitivity: 0.9524, Average Specificity: 0.8356.
  - **Continuous Risk Scoring Paradigm**: Rather than static binary labels (0 or 1), the system now outputs continuous posterior probabilities mapped to a 3-tier clinical triage structure:
    - **Low Risk (0% – 30%)**: Normal acoustic biomarkers. Routine annual check-up recommended.
    - **Moderate / Inconclusive Risk (31% – 65%)**: Borderline instability. Advise re-recording in 3–5 days in quiet surroundings.
    - **Elevated Risk (66% – 100%)**: Significant vocal micro-tremors and entropy. Formal neurological consultation recommended.
