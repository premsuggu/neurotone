import urllib.request
import pathlib
import sys

def download_uci_dataset():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data"
    
    # Using pathlib to build path safely for Windows
    base_dir = pathlib.Path(__file__).parent.parent
    target_dir = base_dir / "data" / "raw" / "uci_parkinsons"
    target_file = target_dir / "parkinsons.csv"
    
    # Ensure directory exists
    target_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting download from: {url}")
    print(f"Target file location: {target_file}")
    
    try:
        urllib.request.urlretrieve(url, target_file)
        print(f"Successfully downloaded and saved dataset to {target_file}")
    except Exception as e:
        print(f"Failed to download dataset: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_uci_dataset()
