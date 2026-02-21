"""
Debug why 452 files are "empty" (no speeches found)
"""

import os
import re
from bs4 import BeautifulSoup
import random

def check_file_content(filepath):
    """Check what's actually in a file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for HTML
    has_html = '<html>' in content.lower()
    
    # Extract text
    if has_html:
        html_match = re.search(r'<html>(.*?)(?:</html>|$)', content, re.DOTALL | re.IGNORECASE)
        if html_match:
            soup = BeautifulSoup(html_match.group(1), 'html.parser')
            text = soup.get_text()
        else:
            text = content
    else:
        text = content
    
    # Check for key indicators
    indicators = {
        'length': len(text),
        'has_html': has_html,
        'party_codes': len(re.findall(r'\(([SMVCLKD]{1,2})\)', text)),
        'anf_markers': text.count('Anf.'),
        'talman': text.count('talman'),
        'anförande_word': text.lower().count('anförande'),
        'has_names': len(re.findall(r'[A-ZÅÄÖ][a-zåäö]+\s+[A-ZÅÄÖ][a-zåäö]+', text[:10000])),
    }
    
    return indicators

def analyze_empty_files():
    """Analyze files that parser marked as empty"""
    
    print("=" * 70)
    print("ANALYZING 'EMPTY' FILES")
    print("=" * 70)
    
    transcript_dir = 'data/raw/transcripts'
    
    # Load parsing stats to see which files were empty
    import pandas as pd
    stats = pd.read_csv('data/processed/parsing_stats.csv')
    
    empty_files = stats[stats['speeches'] == 0]['file'].tolist()
    non_empty_files = stats[stats['speeches'] > 0]['file'].tolist()
    
    print(f"\nEmpty files: {len(empty_files)}")
    print(f"Non-empty files: {len(non_empty_files)}")
    
    # Sample 10 random empty files
    sample_empty = random.sample(empty_files, min(10, len(empty_files)))
    
    print("\n" + "=" * 70)
    print("SAMPLING 10 'EMPTY' FILES")
    print("=" * 70)
    
    for filename in sample_empty:
        filepath = os.path.join(transcript_dir, filename)
        
        print(f"\n📄 {filename}")
        
        indicators = check_file_content(filepath)
        
        print(f"   Length: {indicators['length']:,} chars")
        print(f"   Has HTML: {indicators['has_html']}")
        print(f"   Party codes: {indicators['party_codes']}")
        print(f"   'Anf.' markers: {indicators['anf_markers']}")
        print(f"   'talman' mentions: {indicators['talman']}")
        print(f"   'anförande' word: {indicators['anförande_word']}")
        print(f"   Name patterns: {indicators['has_names']}")
        
        # If it has content, show sample
        if indicators['length'] > 10000 and indicators['party_codes'] > 5:
            print(f"   ⚠️ This file HAS content but parser missed it!")
            
            # Show a sample
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find first party code occurrence
            match = re.search(r'.{200}(\([SMVCLKD]+\)).{500}', content, re.DOTALL)
            if match:
                print(f"\n   Sample around first party code:")
                print("   " + "-" * 66)
                print("   " + match.group(0)[:500])
                print("   " + "-" * 66)
    
    # Compare with non-empty files
    print("\n\n" + "=" * 70)
    print("COMPARING WITH NON-EMPTY FILES")
    print("=" * 70)
    
    sample_non_empty = random.sample(non_empty_files, min(5, len(non_empty_files)))
    
    for filename in sample_non_empty:
        filepath = os.path.join(transcript_dir, filename)
        
        print(f"\n📄 {filename} (HAS SPEECHES)")
        
        indicators = check_file_content(filepath)
        
        print(f"   Length: {indicators['length']:,} chars")
        print(f"   Party codes: {indicators['party_codes']}")
        print(f"   'Anf.' markers: {indicators['anf_markers']}")
        print(f"   'talman' mentions: {indicators['talman']}")
    
    # Statistical comparison
    print("\n\n" + "=" * 70)
    print("STATISTICAL COMPARISON")
    print("=" * 70)
    
    empty_indicators = []
    for filename in random.sample(empty_files, min(50, len(empty_files))):
        filepath = os.path.join(transcript_dir, filename)
        empty_indicators.append(check_file_content(filepath))
    
    non_empty_indicators = []
    for filename in non_empty_files:
        filepath = os.path.join(transcript_dir, filename)
        non_empty_indicators.append(check_file_content(filepath))
    
    import pandas as pd
    
    df_empty = pd.DataFrame(empty_indicators)
    df_non_empty = pd.DataFrame(non_empty_indicators)
    
    print("\nEMPTY FILES (sample of 50):")
    print(df_empty.describe())
    
    print("\n\nNON-EMPTY FILES (all):")
    print(df_non_empty.describe())
    
    print("\n\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    print("""
The issue is likely one of:

1. Parser regex is too strict (only matches specific format)
2. Files have different formats (some debates vs. other doc types)
3. Speech markers vary (not always "Anf.")
4. Party code placement is different in most files

Next: Examine the samples above to see which is the issue.
    """)

if __name__ == "__main__":
    analyze_empty_files()