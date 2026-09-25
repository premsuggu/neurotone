import sys
import pathlib

# Ensure we can import from src when script is run directly
base_dir = pathlib.Path(__file__).parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import pandas as pd
import xgboost as xgb
from src.evaluation import evaluate_clinical_model

def train():
    processed_file = base_dir / "data" / "processed" / "uci_cleaned.csv"
    
    # Load the cleaned dataset
    df = pd.read_csv(processed_file)
    
    # Separate into features 'X' and target 'y'
    X = df.drop(columns=['status'])
    y = df['status']
    
    # Dynamically calculate the imbalance ratio for 'scale_pos_weight'
    # Formula: (count of y == 0) / (count of y == 1)
    count_0 = (y == 0).sum()
    count_1 = (y == 1).sum()
    scale_weight = count_0 / count_1
    
    # Initialize XGBoost model
    model = xgb.XGBClassifier(
        scale_pos_weight=scale_weight,
        random_state=42,
        eval_metric="logloss"
    )
    
    # Evaluate model
    evaluate_clinical_model(model, X, y)

if __name__ == "__main__":
    train()
