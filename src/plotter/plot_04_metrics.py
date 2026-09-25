import sys
import pathlib

# Ensure root is in path
base_dir = pathlib.Path(__file__).parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc

def generate_metrics_plots():
    # Define paths
    processed_file = base_dir / "data" / "processed" / "uci_cleaned.csv"
    viz_dir = base_dir / "visualizations"
    out_file = viz_dir / "04_metrics_roc.png"
    
    # Ensure visualizations directory exists
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    # Load dataset
    df = pd.read_csv(processed_file)
    X = df.drop(columns=['status'])
    y = df['status']
    
    # Split data stratifying on y
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )
    
    # Calculate scale weight based on training set
    scale_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    # Train model
    model = xgb.XGBClassifier(
        scale_pos_weight=scale_weight,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    
    # Generate predictions and probabilities
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Professional Styling
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except:
        pass
        
    # Set up a side-by-side figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Healthy', 'At-Risk'])
    disp.plot(ax=ax1, cmap='Blues')
    ax1.set_title('Model Confusion Matrix', fontsize=14, pad=15)
    
    # Disable grid on confusion matrix for cleaner look
    ax1.grid(False)
    
    # Subplot 2: ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    
    ax2.plot(fpr, tpr, color='#007acc', lw=2, label=f'AUC = {roc_auc:.3f}')
    ax2.plot([0, 1], [0, 1], color='gray', linestyle='--')
    ax2.set_xlim([-0.02, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('False Positive Rate', fontsize=12)
    ax2.set_ylabel('True Positive Rate', fontsize=12)
    ax2.set_title('Receiver Operating Characteristic (ROC)', fontsize=14, pad=15)
    ax2.legend(loc="lower right", fontsize=12)
    
    # Save combined figure
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Successfully generated and saved Metrics and ROC plot to {out_file}")

if __name__ == "__main__":
    generate_metrics_plots()
