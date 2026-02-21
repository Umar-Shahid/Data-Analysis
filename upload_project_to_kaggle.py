#!/usr/bin/env python3
"""Upload the Riksdag thesis project to Kaggle as a Notebook."""

import os
import json
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

def create_notebook_metadata():
    """Create a notebook metadata file for Kaggle."""
    
    notebook_dir = Path('kaggle_notebook_upload')
    notebook_dir.mkdir(exist_ok=True)
    
    # Kaggle notebook metadata
    metadata = {
        "id": "muhammadumarshahid/riksdag-thesis-project",
        "title": "Riksdag Thesis - Swedish Parliament Analysis",
        "code_requirements": {
            "languages": ["python"],
            "packages": []
        },
        "dataset_sources": [
            "muhammadumarshahid/riksdag-speeches-processed-csvs"
        ],
        "kernel_sources": [],
        "isPrivate": False,
        "enableGpu": False,
        "categoryIds": ["data-analysis", "data-cleaning", "nlp"],
        "source_file": "notebook.ipynb"
    }
    
    return notebook_dir, metadata

def create_kernel_file():
    """Create a main kernel/notebook file."""
    
    kernel_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Riksdag Thesis - Swedish Parliament Analysis Project\n",
                    "\n",
                    "## Overview\n",
                    "This project analyzes Swedish Parliament (Riksdag) speeches, debates, and political discourse.\n",
                    "\n",
                    "**Repository:** https://github.com/Umar-Shahid/Data-Analysis\n",
                    "**Datasets:** https://kaggle.com/datasets/muhammadumarshahid/riksdag-speeches-processed-csvs\n",
                    "\n",
                    "## Project Structure\n",
                    "- `scripts/` - Python analysis and processing scripts\n",
                    "- `notebooks/` - Jupyter notebooks for exploration and analysis\n",
                    "- `data/` - Data files and processing pipelines\n",
                    "- `output/` - Analysis results, figures, and tables\n",
                    "\n",
                    "## Key Scripts\n",
                    "1. `01_explore_riksdag.py` - Initial data exploration\n",
                    "2. `02_download_metadata.py` - Download Riksdag debate metadata\n",
                    "3. `03_download_transcripts.py` - Download speech transcripts\n",
                    "4. `04_parse_speeches.py` - Parse and clean transcript data\n",
                    "5. `06_opponent_references.py` - Identify and analyze opponent references\n",
                    "\n",
                    "## Getting Started\n",
                    "```bash\n",
                    "pip install -r requirements.txt\n",
                    "python scripts/01_explore_riksdag.py\n",
                    "```\n",
                    "\n",
                    "## Data\n",
                    "Large processed datasets available on Kaggle:\n",
                    "- `all_speeches.csv` (116.8 MB)\n",
                    "- `speeches_with_opponents.csv` (117.2 MB)\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Import key libraries\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import os\n",
                    "from pathlib import Path\n",
                    "\n",
                    "# Set up paths\n",
                    "project_root = Path('../input/riksdag-speeches-processed-csvs')\n",
                    "\n",
                    "# Check available files\n",
                    "print('Available data files:')\n",
                    "for f in project_root.glob('*.csv'):\n",
                    "    size = f.stat().st_size / (1024*1024)\n",
                    "    print(f'  - {f.name} ({size:.1f} MB)')\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return kernel_content

def upload_project_to_kaggle():
    """Upload project as a Kaggle Notebook."""
    
    print("Preparing Riksdag Thesis project for Kaggle Notebook upload...")
    
    notebook_dir, metadata = create_notebook_metadata()
    kernel_content = create_kernel_file()
    
    # Write metadata
    metadata_path = notebook_dir / 'kernel-metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Created metadata: {metadata_path}")
    
    # Write notebook
    notebook_path = notebook_dir / 'notebook.ipynb'
    with open(notebook_path, 'w') as f:
        json.dump(kernel_content, f, indent=2)
    print(f"✓ Created notebook: {notebook_path}")
    
    # Copy requirements
    req_src = Path('requirements.txt')
    if req_src.exists():
        import shutil
        shutil.copy(req_src, notebook_dir / 'requirements.txt')
        print(f"✓ Copied requirements.txt")
    
    print("\nInitializing Kaggle API...")
    api = KaggleApi()
    api.authenticate()
    print("✓ Authenticated")
    
    print(f"\nUploading to Kaggle as Notebook...")
    try:
        api.kernels_push(folder=str(notebook_dir))
        print("✅ Notebook uploaded successfully!")
        print("View at: https://kaggle.com/code/muhammadumarshahid/riksdag-thesis-project")
        return True
    except Exception as e:
        error_msg = str(e)
        print(f"Upload error: {error_msg[:200]}")
        
        if "already exists" in error_msg.lower():
            print("\nNotebook already exists. Attempting update...")
            try:
                api.kernels_push(folder=str(notebook_dir))
                print("✅ Notebook updated successfully!")
                return True
            except Exception as e2:
                print(f"❌ Update failed: {e2}")
                return False
        else:
            print(f"❌ Upload failed")
            return False

if __name__ == "__main__":
    success = upload_project_to_kaggle()
    exit(0 if success else 1)
