import pathlib

def verify_directories():
    # Base directory is the parent of the src folder
    base_dir = pathlib.Path(__file__).parent.parent
    
    dirs_to_check = [
        "data/raw/uci_parkinsons",
        "data/raw/italian_dataset",
        "data/raw/neurovoz",
        "data/processed/pd",
        "data/processed/healthy",
        "src"
    ]
    
    print("Verifying project directories:")
    print("-" * 40)
    
    all_exist = True
    for dir_path in dirs_to_check:
        full_path = base_dir / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"[OK] Directory exists: {dir_path}")
        else:
            print(f"[ERROR] Directory missing: {dir_path}")
            all_exist = False
            
    print("-" * 40)
    if all_exist:
        print("All directories are correctly set up!")
    else:
        print("Some directories are missing. Please check the setup.")
        
if __name__ == "__main__":
    verify_directories()
