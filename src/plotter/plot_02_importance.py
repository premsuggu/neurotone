import sys
import pathlib

# Ensure root is in path
base_dir = pathlib.Path(__file__).parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt

# Import the feature mapping
from src.plotter.feature_mapping import CLINICAL_NAMES

def generate_importance_plot():
    # Define paths
    processed_file = base_dir / "data" / "processed" / "uci_cleaned.csv"
    viz_dir = base_dir / "visualizations"
    out_file = viz_dir / "02_feature_importance.png"
    
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
    
    # Extract feature importances
    importances = pd.Series(model.feature_importances_, index=X.columns)
    
    # Sort and select top 10 features
    top_10 = importances.sort_values(ascending=True).tail(10)
    
    # Generate Plot
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except:
        pass # Fallback
        
    plt.figure(figsize=(10, 6))
    
    # Create horizontal bar chart with professional color
    top_10.plot(kind='barh', color='#007acc')
    
    # Finalize and save
    plt.title('Top 10 Acoustic Features Driving the NeuroTone Screening Model', fontsize=14, pad=15)
    plt.xlabel('Relative Importance (Gain)', fontsize=12)
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"Successfully generated and saved feature importance plot to {out_file}")

if __name__ == "__main__":
    generate_importance_plot()
