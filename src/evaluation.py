import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, recall_score

def evaluate_clinical_model(model, X, y):
    # Initialize Stratified 5-Fold Cross-Validation
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    auc_scores = []
    sensitivities = []
    specificities = []
    
    # Print the model's name dynamically
    print(f"Evaluating model: {type(model).__name__}")
    
    # Iterate through folds
    for train_index, test_index in skf.split(X, y):
        # Handle pandas structures safely
        if hasattr(X, 'iloc'):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        else:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        if hasattr(model, 'predict_proba'):
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, y_pred_proba)
        else:
            auc = roc_auc_score(y_test, y_pred)
            
        # Sensitivity (Recall for class 1)
        sensitivity = recall_score(y_test, y_pred, pos_label=1)
        
        # Specificity (Recall for class 0)
        specificity = recall_score(y_test, y_pred, pos_label=0)
        
        auc_scores.append(auc)
        sensitivities.append(sensitivity)
        specificities.append(specificity)
        
    mean_auc = np.mean(auc_scores)
    mean_sens = np.mean(sensitivities)
    mean_spec = np.mean(specificities)
    
    print(f"Average AUC: {mean_auc:.4f}")
    print(f"Average Sensitivity: {mean_sens:.4f}")
    print(f"Average Specificity: {mean_spec:.4f}")
    
    return {
        "auc": mean_auc,
        "sensitivity": mean_sens,
        "specificity": mean_spec
    }
