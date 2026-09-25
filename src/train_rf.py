import sys
import pathlib

# Ensure we can import from src when script is run directly
base_dir = pathlib.Path(__file__).parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.evaluation import evaluate_clinical_model

def train():
    processed_file = base_dir / "data" / "processed" / "uci_cleaned.csv"
    
    # Load the cleaned dataset
    df = pd.read_csv(processed_file)
    
    # Separate into features 'X' and target 'y'
    X = df.drop(columns=['status'])
    y = df['status']
    
    # Initialize Random Forest with balanced weights and specific random state
    model = RandomForestClassifier(class_weight="balanced", random_state=42)
    
    # Evaluate model
    evaluate_clinical_model(model, X, y)

if __name__ == "__main__":
    train()
