"""
copy_artifacts.py — Automatically copy pre-trained model files and metadata
from Downloads into the churn_prediction project folder.
"""
import os
import shutil

SOURCE_DIR = r"C:\Users\ganes\Downloads\ChurnPrediction _01\ChurnPrediction"
DEST_DIR = os.path.dirname(os.path.abspath(__file__))

FILES_TO_COPY = [
    ("models/random_forest_baseline.pkl", "models/random_forest_baseline.pkl"),
    ("models/scaler.pkl", "models/scaler.pkl"),
    ("models/ohe.pkl", "models/ohe.pkl"),
    ("data/processed/dataset_metadata.json", "data/processed/dataset_metadata.json"),
]

def main():
    print("Checking source files in Downloads...")
    for src_rel, dest_rel in FILES_TO_COPY:
        src = os.path.join(SOURCE_DIR, src_rel.replace('/', os.sep))
        dest = os.path.join(DEST_DIR, dest_rel.replace('/', os.sep))
        
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"✅ Copied: {src_rel} -> {dest_rel}")
        else:
            print(f"⚠️ Source missing: {src}")

    print("\nDone! All available model artifacts are prepared.")

if __name__ == "__main__":
    main()
