# Project NeuroTone

> **A Non-Invasive, Smartphone-Compatible Voice Acoustic Screening Prototype for Parkinson's Disease**

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Phase 3](https://img.shields.io/badge/Status-Phase%203%20Completed-green.svg)]()
[![Model: XGBoost](https://img.shields.io/badge/Model-XGBoost%201.7.6-orange.svg)]()

---

## 1. Overview & Clinical Mission

Parkinson's Disease (PD) is among the fastest-growing neurodegenerative disorders globally. Currently, formal diagnosis heavily depends on observable motor symptoms such as resting tremors, muscle rigidity, and balance loss. Unfortunately, by the time these overt signs emerge, an estimated **60% to 80%** of dopamine-producing neurons in the substantia nigra have already degenerated.

**Project NeuroTone** bridges this diagnostic window by turning everyday smartphones into non-invasive, objective neurological screening tools. Up to **90%** of Parkinson's patients exhibit early vocal degradation (*hypophonia*, vocal tremor, and incomplete laryngeal closure). By recording a patient sustaining a simple vowel sound (`/a/`) into a standard smartphone microphone, NeuroTone analyzes 22 micro-acoustic biomarkers of vocal fold tension and neurological stability to deliver an instant, accessible risk assessment.

---

## 2. Key Performance Highlights

Evaluated using rigorous **Stratified 5-Fold Cross-Validation** on the benchmark dataset:

| Clinical Metric | Baseline Random Forest | Champion XGBoost Model | Real-World Clinical Impact |
| :--- | :---: | :---: | :--- |
| **ROC AUC** | `0.9622` | **`0.9738`** *(+1.2%)* | Outstanding cohort discriminative separation across all thresholds |
| **Sensitivity (Recall PD)** | `0.9522` | **`0.9524`** *(Stable)* | Catches over 95 out of every 100 individuals exhibiting vocal signs |
| **Specificity (Recall Healthy)** | `0.6933` | **`0.8356`** *(+14.2%)* | Dramatic reduction in false positive alarms, avoiding patient distress |
| **Derived Overall Accuracy** | `88.8%` | **`92.3%`** *(+3.5%)* | Correctly categorizes ~180 out of the 195 total phonation samples |

> **The Imbalance Breakthrough:** The initial Random Forest model had a high false positive rate on healthy participants (~30.7%). By transitioning to Extreme Gradient Boosting (XGBoost) and dynamically configuring `scale_pos_weight = 48 / 147 = 0.3265`, we penalized errors on the minority healthy cohort, boosting specificity by **+14.2%** without degrading sensitivity.

---

## 3. Project Architecture

The codebase adheres to professional software engineering standards, ensuring strict separation of concerns, reproducibility, and prevention of training data leakage:

```text
neurotone/
├── data/
│   ├── raw/
│   │   ├── uci_parkinsons/       # Benchmark UCI tabular dataset (parkinsons.csv)
│   │   ├── italian_dataset/      # Reserved for Italian multi-speaker audio recordings
│   │   └── neurovoz/             # Reserved for NeuroVoz clinical speech recordings
│   └── processed/
│       ├── uci_cleaned.csv       # Cleaned, standardized tabular dataset (195x23)
│       ├── healthy/              # Segmented healthy control data
│       └── pd/                   # Segmented Parkinson's Disease data
├── docs/
│   ├── project_context.md        # Comprehensive milestone & context retention log
│   └── report.pdf                # Formal 4-page executive, clinical, and technical report
├── src/
│   ├── __init__.py               # Core source package marker
│   ├── setup_dirs.py             # Pathlib-based directory integrity verification
│   ├── download_uci.py           # Automated UCI dataset downloader
│   ├── clean_uci_data.py         # Tabular data cleansing & feature separation
│   ├── evaluation.py             # Modular Stratified 5-Fold Cross-Validation engine
│   ├── train_rf.py               # Baseline Random Forest training & evaluation
│   ├── train_xgb.py              # Champion XGBoost training with imbalance reweighting
│   ├── generate_report.py        # Automated ReportLab formal PDF generation engine
│   └── plotter/
│       ├── __init__.py           # Plotter package marker
│       ├── feature_mapping.py    # Clinical feature name mapping dictionary (CLINICAL_NAMES)
│       ├── plot_01_shap.py       # SHAP beeswarm summary plot generator
│       ├── plot_02_importance.py # Top 10 feature importance horizontal bar chart
│       ├── plot_03_individual.py # Patient case-study waterfall breakdown plots
│       ├── plot_04_metrics.py    # Confusion matrix & ROC curve dual-panel visual
│       └── plot_05_boxplots.py   # Raw signal 2x2 boxplots with stripplot overlay
├── visualizations/               # High-resolution (300 DPI) publication-ready visual assets
│   ├── 01_shap_summary.png       # Global feature impact beeswarm plot
│   ├── 02_feature_importance.png # Top 10 relative gain bar chart
│   ├── 03_case_healthy.png       # Individual true negative waterfall explanation
│   ├── 03_case_risk.png          # Individual true positive waterfall explanation
│   ├── 04_metrics_roc.png        # Confusion matrix & ROC curve panel
│   └── 05_raw_signal_boxplots.png# Key biomarker distribution comparisons
├── .gitignore                    # Python, IDE, and temporary archive exclusion rules
├── requirements.txt              # Pinned package dependencies
└── README.md                     # Comprehensive project documentation
```

---

## 4. Dataset Profile & Clinical Biomarkers

### 4.1 Cohort Breakdown
* **Benchmark Corpus:** UCI Parkinson's Disease Dataset (Max Little et al., Oxford University / NCVS Denver).
* **Subjects:** 31 individuals (23 medically diagnosed with Parkinson's Disease, 8 healthy control subjects).
* **Samples:** 195 sustained `/a/` vowel phonations (~6 takes per participant).
* **Class Balance:** 147 PD samples (75.4%) vs. 48 Healthy samples (24.6%).

### 4.2 The 22 Extracted Vocal Biomarkers
1. **Fundamental Frequency / Pitch (`MDVP:Fo`, `MDVP:Fhi`, `MDVP:Flo`):** Average, maximum, and minimum vocal frequency in Hz.
2. **Frequency Instability / Jitter (`MDVP:Jitter(%)`, `RAP`, `PPQ`, `DDP`):** Cycle-to-cycle pitch fluctuations caused by laryngeal micro-tremors.
3. **Amplitude Instability / Shimmer (`MDVP:Shimmer`, `APQ`, `DDA`):** Cycle-to-cycle volume fluctuations resulting from incomplete vocal cord sealing.
4. **Noise Ratios (`HNR`, `NHR`):** Ratio of pure tonal energy to turbulent airflow; lower HNR reflects breathiness and hoarseness.
5. **Nonlinear Dynamical Biomarkers (`PPE`, `RPDE`, `DFA`, `spread1`, `spread2`):** Quantify physical chaos and turbulence in the vocal sound wave.
   * *Pitch Period Entropy (PPE)* and *Spread1* consistently emerge as the highest-ranking predictors in our model.

---

## 5. Visual Pitch Deck Portfolio

The project includes five high-resolution, explainable visual assets located in `visualizations/`:

1. **`01_shap_summary.png` — Global SHAP Beeswarm Plot:** Demonstrates how feature values pull patient risk toward Parkinson's or Healthy classifications.
2. **`02_feature_importance.png` — Top 10 Feature Importance:** Ranks the most influential vocal biomarkers by XGBoost gain.
3. **`03_case_healthy.png` & `03_case_risk.png` — Patient Waterfall Plots:** Explainable step-by-step audit showing why a specific individual was classified as healthy or at-risk.
4. **`04_metrics_roc.png` — Confusion Matrix & ROC Curve:** Diagnostic validation panel verifying 0.97+ AUC and minimal misclassification on unseen data.
5. **`05_raw_signal_boxplots.png` — 2x2 Biomarker Comparison:** Box plots with raw stripplot overlays in modern blue/coral, contrasting PPE, Jitter, Shimmer, and HNR between cohorts.

---

## 6. Installation & Quickstart

### 6.1 Prerequisites
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/)
* Git

### 6.2 Setup Environment
```bash
# Clone the repository
git clone https://github.com/<your-username>/neurotone.git
cd neurotone

# Create and activate the conda environment
conda create -n neurotone python=3.10 -y
conda activate neurotone

# Install required dependencies
pip install -r requirements.txt
```

### 6.3 Run the Pipeline
```bash
# 1. Verify directory hierarchy
python src/setup_dirs.py

# 2. Download raw UCI dataset
python src/download_uci.py

# 3. Clean and process data
python src/clean_uci_data.py

# 4. Train and evaluate baseline Random Forest
python src/train_rf.py

# 5. Train and evaluate champion XGBoost model
python src/train_xgb.py

# 6. Generate the visual pitch deck assets
python src/plotter/plot_01_shap.py
python src/plotter/plot_02_importance.py
python src/plotter/plot_03_individual.py
python src/plotter/plot_04_metrics.py
python src/plotter/plot_05_boxplots.py

# 7. Compile the formal PDF report
python src/generate_report.py
```

---

## 7. Project Roadmap

* [x] **Phase 1: Environment Setup & Acquisition** — Modular directory hierarchy and UCI benchmark data acquisition.
* [x] **Phase 2: Exploratory Data Analysis & Cleansing** — Imbalance identification, feature extraction, and validation schema.
* [x] **Phase 3: Baseline & Advanced Tabular Modeling** — Cross-validated Random Forest and XGBoost with clinical metrics.
* [x] **Phase 3.5: Explainability & Pitch Assets** — SHAP explanations, visual pitch deck, and comprehensive stakeholder PDF report.
* [ ] **Phase 4: Raw Audio Ingestion & Acoustic Extraction** — Process multi-lingual audio files (`.wav`) from Italian and NeuroVoz datasets using `praat-parselmouth`, `opensmile`, and `librosa`.
* [ ] **Phase 5: Mobile Edge Deployment** — Export the optimized classifier to ONNX/Flask microservice for sub-second, on-device mobile phone screening.

---

## 8. License & Acknowledgments

* **License:** Distributed under the MIT License.
* **Dataset Attribution:** Max Little, Patrick McSharry, Stephen Roberts, Declan Costello, Irene Moroz (2007). *Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection*, BioMedical Engineering OnLine.
* **Research & Development:** NeuroTone Interdisciplinary Research Team.
