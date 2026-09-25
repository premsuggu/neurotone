import pandas as pd
import pathlib

def clean_data():
    base_dir = pathlib.Path(__file__).parent.parent
    raw_file = base_dir / "data" / "raw" / "uci_parkinsons" / "parkinsons.csv"
    processed_dir = base_dir / "data" / "processed"
    processed_file = processed_dir / "uci_cleaned.csv"
    
    print(f"Loading data from {raw_file}")
    df = pd.read_csv(raw_file)
    
    # Drop the 'name' column as it is non-predictive string data
    if 'name' in df.columns:
        df = df.drop(columns=['name'])
        
    # Separate into features matrix 'X' and target vector 'y'
    y = df['status']
    X = df.drop(columns=['status'])
    
    # Print shape of X
    print(f"Shape of features matrix X: {X.shape}")
    
    # Print class distribution of y
    print("Class distribution of target vector y:")
    print(y.value_counts())
    
    # Save combined cleaned data
    combined_df = pd.concat([X, y], axis=1)
    processed_dir.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(processed_file, index=False)
    print(f"Cleaned dataset saved to {processed_file}")

if __name__ == "__main__":
    clean_data()
