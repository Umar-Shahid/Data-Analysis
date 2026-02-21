# Uploading Riksdag Thesis Project to Kaggle

## Option 1: Upload as Kaggle Notebook (Recommended for Code)

1. Go to https://kaggle.com/code and click **"New Notebook"**
2. Choose **"File"** upload and select the files from this project:
   - Select all Python scripts from `scripts/`
   - Include notebooks from `notebooks/`
   - Include `requirements.txt`

3. Set up the notebook:
   - **Title:** "Riksdag Thesis - Swedish Parliament Analysis"
   - **Subtitle:** "Swedish Parliament speeches and political discourse analysis"
   - **Add dataset:** Link to [Riksdag Speeches Dataset](https://kaggle.com/datasets/muhammadumarshahid/riksdag-speeches-processed-csvs)
   - **Category:** Data Analysis, NLP, Data Cleaning
   - **License:** CC0: Public Domain

## Option 2: Create a Kaggle Competition Notebook

You can also create an analysis notebook that uses your published dataset:

```python
import pandas as pd
import os

# Load data from Kaggle dataset
all_speeches = pd.read_csv('/kaggle/input/riksdag-speeches-processed-csvs/all_speeches.csv')
opponent_speeches = pd.read_csv('/kaggle/input/riksdag-speeches-processed-csvs/speeches_with_opponents.csv')

print(f"Loaded {len(all_speeches)} speeches")
print(f"Loaded {len(opponent_speeches)} opponent references")
```

## Option 3: Upload as a Kaggle Dataset with Code

Add your scripts to the dataset upload:

1. Go to https://kaggle.com/settings/datasets
2. Click **"Create New Dataset"** (or edit existing)
3. Upload all project files as supplementary files
4. Add a README explaining how to use the code

## Direct Repository Link

Your project is already on GitHub:
**Repository:** https://github.com/Umar-Shahid/Data-Analysis

Users can clone and run the project locally with:
```bash
git clone https://github.com/Umar-Shahid/Data-Analysis.git
cd Data-Analysis
pip install -r requirements.txt
python scripts/01_explore_riksdag.py
```

## What's Available

- 📊 **Processed Data:** [Kaggle Dataset](https://kaggle.com/datasets/muhammadumarshahid/riksdag-speeches-processed-csvs) (CSVs)
- 🐍 **Code & Scripts:** [GitHub Repository](https://github.com/Umar-Shahid/Data-Analysis)
- 📓 **Notebooks:** Available in the `notebooks/` folder
