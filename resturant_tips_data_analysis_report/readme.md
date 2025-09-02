# Tips Data Analysis Report

This repository contains a comprehensive analysis of restaurant tipping behavior, including statistical analysis, visualizations, and actionable insights.

## Project Structure
```
tips_data_analysis_report/
├── data/                          # Data files
│   ├── tips.csv                  # Dataset in CSV format
│   └── tips.xlsx                 # Dataset in Excel format
├── scripts/                       # Analysis scripts
│   └── 01_data_analysis.ipynb   # Main analysis notebook
└── README.md                      # Project documentation
```

## Key Findings
- Strong correlation between total bill and tip amounts (r = 0.68)
- Higher tips during dinner and weekends
- Gender and smoking status influence tipping patterns
- Party size affects both bill and tip amounts

## Installation and Setup

1. **Create and activate Python virtual environment**:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/macOS:
source .venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Analysis Contents

The Jupyter notebook (01_data_analysis.ipynb) includes:

1. **Data Composition Analysis**
   - Dataset structure and statistics
   - Missing value analysis
   - Data type verification

2. **Distribution Analysis**
   - Histograms with mean/median indicators
   - Box plots for numerical variables
   - Count plots for categorical variables

3. **Comparative Analysis**
   - Tips by gender, smoking status
   - Day and time comparisons
   - Grouped statistics

4. **Relationship Analysis**
   - Correlation heatmap
   - Pairwise relationships
   - Regression analysis

## Usage

1. Ensure you have activated the virtual environment
2. Launch Jupyter Notebook:
```bash
jupyter notebook scripts/01_data_analysis.ipynb
```

## Technologies Used
- Python 3.x
- Pandas for data manipulation
- Seaborn and Matplotlib for visualization
- NumPy for numerical operations
- Jupyter Notebook for interactive analysis
