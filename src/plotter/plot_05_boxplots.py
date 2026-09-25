import sys
import pathlib

# Ensure root is in path
base_dir = pathlib.Path(__file__).parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import the feature mapping
from src.plotter.feature_mapping import CLINICAL_NAMES

def generate_boxplots():
    # Define paths
    processed_file = base_dir / "data" / "processed" / "uci_cleaned.csv"
    viz_dir = base_dir / "visualizations"
    out_file = viz_dir / "05_raw_signal_boxplots.png"
    
    # Load dataset
    df = pd.read_csv(processed_file)
    
    # Rename columns to clinical names
    df = df.rename(columns=CLINICAL_NAMES)
    
    # Add human-readable 'Diagnosis' column
    df['Diagnosis'] = df['status'].map({0: 'Healthy', 1: 'At-Risk'})
    
    # Select key biomarkers
    features = [
        'Pitch Irregularity (PPE)',
        'Frequency Instability (Jitter %)',
        'Amplitude Instability (Shimmer)',
        'Harmonics-to-Noise Ratio'
    ]
    
    # Setup modern styling
    sns.set_theme(style="whitegrid", rc={"grid.color": "#f1f2f6", "axes.edgecolor": "#dcdde1"})
    
    # Setup 2x2 grid
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    # Professional modern palette
    # Healthy: Soft Modern Blue, At-Risk: Warm Coral
    palette = {'Healthy': '#3498db', 'At-Risk': '#e74c3c'}
    
    for i, feature in enumerate(features):
        ax = axes[i]
        
        # Boxplot with stylized elements
        sns.boxplot(
            data=df, 
            x='Diagnosis', 
            y=feature, 
            ax=ax, 
            hue='Diagnosis',
            palette=palette,
            dodge=False,
            legend=False,
            boxprops={'alpha': 0.7, 'edgecolor': '#2f3640', 'linewidth': 1.5},
            medianprops={'color': '#2f3640', 'linewidth': 2},
            flierprops={'marker': 'o', 'markersize': 0} # Hide fliers as they overlap with stripplot
        )
        
        # Overlay stripplot to show actual distributions securely
        sns.stripplot(
            data=df, 
            x='Diagnosis', 
            y=feature, 
            ax=ax, 
            jitter=0.25, 
            alpha=0.6, 
            size=4.5,
            color='#2f3640',
            dodge=False
        )
        
        # Subplot Titles and Labels with custom colors
        ax.set_title(f"{feature}", fontsize=13, pad=12, fontweight='bold', color='#2f3640')
        ax.set_xlabel("")
        ax.set_ylabel("Measured Value", fontsize=11, color='#718093')
        ax.tick_params(colors='#718093', labelsize=10)
        sns.despine(ax=ax, left=True)
        
    fig.suptitle("Raw Signal Distribution: Healthy vs At-Risk", fontsize=18, y=1.02, fontweight='bold', color='#2f3640')
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Successfully generated and saved updated box plots to {out_file}")

if __name__ == "__main__":
    generate_boxplots()
