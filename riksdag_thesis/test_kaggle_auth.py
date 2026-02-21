#!/usr/bin/env python3
"""Test Kaggle API credentials."""

from kaggle.api.kaggle_api_extended import KaggleApi
import json
from pathlib import Path

# Read the credentials directly
kaggle_cfg = Path.home() / '.kaggle' / 'kaggle.json'
if kaggle_cfg.exists():
    with open(kaggle_cfg) as f:
        creds = json.load(f)
    print(f"Username from file: {creds.get('username')}")
    print(f"API Key from file: {creds.get('key')[:20]}...")

try:
    api = KaggleApi()
    api.authenticate()
    print("✓ Authenticated successfully via API")
    
    # Try a simple call
    try:
        # Just try to get datasets for the user
        result = api.dataset_list(user=creds.get('username'), max_size=1)
        print(f"✓ API call successful - can list user datasets")
    except Exception as e:
        print(f"⚠ API call error: {str(e)[:150]}")
        
except Exception as e:
    print(f"✗ Authentication failed: {e}")
