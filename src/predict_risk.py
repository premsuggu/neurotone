import sys
import pathlib

# Ensure root is in path
base_dir = pathlib.Path(__file__).parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import pandas as pd
import xgboost as xgb
from src.plotter.feature_mapping import CLINICAL_NAMES


def get_trained_model(X, y):
    """
    Fits our champion XGBoost classifier with dynamic imbalance weighting.
    """
    scale_weight = (y == 0).sum() / (y == 1).sum()
    model = xgb.XGBClassifier(
        scale_pos_weight=scale_weight,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X, y)
    return model


def assess_vocal_risk(patient_sample, model, feature_names=None):
    """
    Takes a single patient's acoustic features (pandas Series or 1D array)
    and outputs a continuous probability, risk category, and clinical recommendations.
    """
    if isinstance(patient_sample, pd.Series):
        if feature_names is None:
            feature_names = patient_sample.index
        sample_df = pd.DataFrame([patient_sample.values], columns=feature_names)
    elif isinstance(patient_sample, pd.DataFrame):
        sample_df = patient_sample
    else:
        sample_df = pd.DataFrame([patient_sample], columns=feature_names)

    # Predict continuous probability of Parkinson's Disease (Class 1)
    probabilities = model.predict_proba(sample_df)[0]
    healthy_prob = float(probabilities[0])
    risk_prob = float(probabilities[1])
    risk_percentage = risk_prob * 100.0

    # Three-Tier Clinical Stratification
    if risk_percentage <= 30.0:
        tier = "Low Risk"
        tier_code = "LOW"
        recommendation = (
            "Vocal acoustic dynamics are consistent with healthy laryngeal function. "
            "No immediate clinical follow-up required. Routine annual screening recommended."
        )
    elif risk_percentage <= 65.0:
        tier = "Moderate / Inconclusive Risk"
        tier_code = "MODERATE"
        recommendation = (
            "Mild micro-instability or irregular vocal dynamics detected. "
            "Advise re-recording in a quiet environment in 3–5 days to rule out vocal fatigue "
            "or temporary laryngitis."
        )
    else:
        tier = "Elevated Risk"
        tier_code = "ELEVATED"
        recommendation = (
            "Significant vocal tremor, incomplete closure, or chaotic signal entropy detected. "
            "A comprehensive neurological examination and UPDRS motor evaluation are advised."
        )

    return {
        "risk_percentage": risk_percentage,
        "healthy_percentage": healthy_prob * 100.0,
        "tier": tier,
        "tier_code": tier_code,
        "recommendation": recommendation,
        "probabilities": (healthy_prob, risk_prob)
    }


def format_patient_report(patient_id, assessment):
    """
    Formats the assessment into a clean, human-readable patient report.
    """
    report = []
    report.append("=" * 65)
    report.append(f"  NEUROTONE CLINICAL SCREENING REPORT — PATIENT: {patient_id}")
    report.append("=" * 65)
    report.append(f"  Parkinson's Disease Risk Score: {assessment['risk_percentage']:.1f}%")
    report.append(f"  Triage Category:                [{assessment['tier_code']}] {assessment['tier']}")
    report.append("-" * 65)
    report.append("  Clinical Recommendation:")
    report.append(f"  {assessment['recommendation']}")
    report.append("=" * 65)
    return "\n".join(report)


def demo_risk_scoring():
    processed_file = base_dir / "data" / "processed" / "uci_cleaned.csv"
    df = pd.read_csv(processed_file)
    
    X = df.drop(columns=['status'])
    y = df['status']
    
    # Train champion model
    print("Training NeuroTone champion model on benchmark cohort...")
    model = get_trained_model(X, y)
    
    # Select sample cases: A true healthy control, a borderline case, and an at-risk case
    healthy_idx = (y == 0).to_numpy().nonzero()[0][0]
    risk_idx = (y == 1).to_numpy().nonzero()[0][0]
    
    print("\nSimulating patient voice screening tests:\n")
    
    # Patient 1: Healthy Control
    sample_healthy = X.iloc[healthy_idx]
    assessment_h = assess_vocal_risk(sample_healthy, model)
    print(format_patient_report("HC-01 (Healthy Control Sample)", assessment_h))
    print()
    
    # Patient 2: Parkinson's Patient
    sample_risk = X.iloc[risk_idx]
    assessment_r = assess_vocal_risk(sample_risk, model)
    print(format_patient_report("PD-01 (Parkinson's Phonation Sample)", assessment_r))
    print()


if __name__ == "__main__":
    demo_risk_scoring()
