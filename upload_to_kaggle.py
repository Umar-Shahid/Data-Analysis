#!/usr/bin/env python3
"""Upload large CSV files to Kaggle dataset."""

import os
import json
import shutil
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

def upload_to_kaggle():
    # Initialize Kaggle API
    api = KaggleApi()
    api.authenticate()
    
    # Dataset configuration
    dataset_dir = Path("kaggle_upload")
    dataset_slug = "riksdag_speeches"  # This becomes muhammadumarshahid/riksdag_speeches
    
    # Ensure directory exists
    if not dataset_dir.exists():
        print(f"Creating {dataset_dir}")
        dataset_dir.mkdir(exist_ok=True)
    
    # Check that CSV files exist in upload directory
    expected_files = [
        "all_speeches.csv",
        "speeches_with_opponents.csv"
    ]
    
    print("Checking for CSV files in upload directory...")
    for csv_file in expected_files:
        file_path = dataset_dir / csv_file
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"  ✓ {csv_file} ({size_mb:.1f} MB)")
        else:
            print(f"  ✗ {csv_file} NOT FOUND")
    
    # Create/update dataset metadata
    metadata = {
        "title": "Riksdag Speeches (Processed CSVs)",
        "id": f"muhammadumarshahid/{dataset_slug}",
        "licenses": [{"name": "CC0: Public Domain"}],
        "description": "Processed Swedish Parliament (Riksdag) speeches and transcripts with opponent references"
    }
    
    metadata_path = dataset_dir / "dataset-metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nMetadata written to {metadata_path}")
    
    # Check if dataset exists and needs update or if it's new
    print(f"\nAttempting to upload dataset: {metadata['id']}")
    print("This may take several minutes due to file sizes...\n")
    
    try:
        # Try to create new dataset - use default parameters
        api.dataset_create_new(dataset_dir)
        print("✅ Dataset created successfully!")
    except Exception as e:
        error_msg = str(e)
        print(f"Create attempt result: {error_msg[:100]}")
        # If dataset already exists, try to update it
        if "already exists" in error_msg.lower() or "403" in error_msg or "400" in error_msg:
            print(f"\nDataset may already exist. Attempting update...")
            try:
                api.dataset_create_version(dataset_dir)
                print("✅ Dataset version updated successfully!")
            except Exception as e2:
                print(f"❌ Update failed: {e2}")
                return False
        else:
            print(f"❌ Upload failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = upload_to_kaggle()
    exit(0 if success else 1)
