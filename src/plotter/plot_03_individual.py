import sys
import pathlib

# Ensure root is in path
base_dir = pathlib.Path(__file__).parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import pandas as pd
import xgboost as xgb
import shap
import matplotlib.pyplot as plt

# Import the feature mapping
from src.plotter.feature_mapping import CLINICAL_NAMES

def generate_individual_plots():
    # Define paths
    processed_file = base_dir / "data" / "processed" / "uci_cleaned.csv"
    viz_dir = base_dir / "visualizations"
    out_healthy = viz_dir / "03_case_healthy.png"
    out_risk = viz_dir / "03_case_risk.png"
    
    # Ensure visualizations directory exists
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    # Load dataset
    df = pd.read_csv(processed_file)
    X = df.drop(columns=['status'])
    y = df['status']
    
    # Rename columns to clinical names
    X = X.rename(columns=CLINICAL_NAMES)
    
    # Calculate scale weight
    scale_weight = (y == 0).sum() / (y == 1).sum()
    
    # Initialize and fit model
    model = xgb.XGBClassifier(
        scale_pos_weight=scale_weight,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X, y)
    
    # Generate predictions
    preds = model.predict(X)
    
    # Find True Negative (Healthy) and True Positive (At-Risk) indices
    # Convert to boolean masks and find the first positional index
    tn_mask = (y == 0) & (preds == 0)
    tp_mask = (y == 1) & (preds == 1)
    
    healthy_idx = tn_mask.to_numpy().nonzero()[0][0]
    risk_idx = tp_mask.to_numpy().nonzero()[0][0]
    
    # Initialize Explainer and calculate SHAP values
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    
    # Generate Healthy Patient Plot
    plt.figure()
    shap.plots.waterfall(shap_values[healthy_idx], show=False)
    plt.savefig(out_healthy, dpi=300, bbox_inches='tight')
    plt.clf()
    
    # Generate At-Risk Patient Plot
    plt.figure()
    shap.plots.waterfall(shap_values[risk_idx], show=False)
    plt.savefig(out_risk, dpi=300, bbox_inches='tight')
    plt.clf()
    
    print(f"Successfully generated and saved Healthy Patient plot to {out_healthy}")
    print(f"Successfully generated and saved At-Risk Patient plot to {out_risk}")

if __name__ == "__main__":
    generate_individual_plots()
