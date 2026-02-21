"""
Download Full Transcripts of Riksdag Debates
This is the heavy lifting - will take 2-3 hours
"""
import requests
import pandas as pd 
from bs4 import BeautifulSoup
import time 
from tqdm import tqdm
import json
import os

def download_debate_text(dok_id):
    """Download full text for a single debate"""
    
    # Riksdag provides text in both HTML and plain text
    text_url = f"https://data.riksdagen.se/dokument/{dok_id}.txt"
    html_url = f"https://data.riksdagen.se/dokument/{dok_id}.html"
    
    try:
        # Try plain text first (cleaner)
        response = requests.get(text_url, timeout=30)
        
        if response.status_code == 200:
            return response.text
        
        # Fallback to HTML
        response = requests.get(html_url, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text from HTML
            text = soup.get_text(separator='\n', strip=True)
            return text
        
        return None
        
    except Exception as e:
        print(f"Error downloading {dok_id}: {e}")
        return None
    
def download_all_transcripts(metadata_file='data/raw/riksdag_debates_metadata.csv',
                            output_dir='data/raw/transcripts',
                            sample_size=None):
    """Download all debate transcripts"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load metadata
    debates = pd.read_csv(metadata_file)
    
    if sample_size:
        print(f"⚠️  Sampling {sample_size} debates for testing")
        debates = debates.sample(n=sample_size, random_state=42)
    
    print(f"\n📥 Downloading {len(debates)} debate transcripts...")
    print("This will take 2-3 hours. Get some coffee! ☕\n")
    
    successful = 0
    failed = []

    for idx, row in tqdm(debates.iterrows(), total=len(debates)):
        dok_id = row['dok_id']
        
        # Check if already downloaded
        output_file = os.path.join(output_dir, f"{dok_id}.txt")

        if os.path.exists(output_file):
            successful += 1
            continue

        # Download text
        text = download_debate_text(dok_id)
        
        if text:
            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            successful += 1
        else:
            failed.append(dok_id)
        
        # Be polite to the server
        time.sleep(0.5)

        # Save Progress Every 50 Documents
        if (idx + 1) % 50 == 0:
            print(f"\n  Progress: {successful}/{len(debates)} successful")

    print(f"\n\n✅ COMPLETE:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(failed)}")    
    
    if failed:
        print(f"\n  Failed IDs saved to: {output_dir}/failed_downloads.txt")
        with open(f"{output_dir}/failed_downloads.txt", 'w') as f:
                f.write('\n'.join(failed))

    return successful,failed

if __name__ == "__main__":
    print("=" * 60)
    print("DOWNLOAD RIKSDAG DEBATE TRANSCRIPTS")
    print("=" * 60)

    # First do a small test
    print("\n🧪 Running test with 5 debates...")
    test_success, test_failed = download_all_transcripts(sample_size=5)

    if test_success > 0:
        print("\n✅ Test successful! Ready for full download.")

        proceed = input("\n⚠️  Download ALL debates? This takes 2-3 hours. (y/n): ")

        if proceed.lower() == 'y':
            successful, failed = download_all_transcripts()

            print("\n\n🎉 DOWNLOAD COMPLETE!")
            print(f"Transcripts saved to: data/raw/transcripts/")
        
    else:
        print("\n❌ Test failed. Check your internet connection and API access.")