"""
Download all debate metadata from the Riksdag API for 2018-2024
This will be used to get the list of all debates and their IDs
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from tqdm import tqdm
import json

BASE_URL = "https://data.riksdagen.se/dokumentlista/"

def get_debates_for_period(start_date, end_date):
    """Get all debate documents for a date range"""
    
    params = {
        'doktyp': 'prot',
        'from': start_date,
        'tom': end_date,
        'utformat': 'json',
        'sort': 'datum'
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'dokumentlista' in data and 'dokument' in data['dokumentlista']:
                return data['dokumentlista']['dokument']
        
        return []
        
    except Exception as e:
        print(f"Error fetching {start_date} to {end_date}: {e}")
        return []

def download_all_metadata(start_year=2018, end_year=2024):
    """Download metadata for all debates in date range"""
    
    all_debates = []
    
    # Download year by year to avoid timeouts
    for year in range(start_year, end_year + 1):
        print(f"\n📅 Downloading {year}...")
        
        # Split year into quarters to avoid API limits
        quarters = [
            (f"{year}-01-01", f"{year}-03-31"),
            (f"{year}-04-01", f"{year}-06-30"),
            (f"{year}-07-01", f"{year}-09-30"),
            (f"{year}-10-01", f"{year}-12-31")
        ]
        
        for start, end in tqdm(quarters, desc=f"Year {year}"):
            debates = get_debates_for_period(start, end)
            all_debates.extend(debates)
            time.sleep(1)  # Be polite to the server
    
    # Convert to DataFrame
    metadata_df = pd.DataFrame(all_debates)
    
    if len(metadata_df) > 0:
       df_clean = pd.DataFrame({
           'dok_id': metadata_df['dok_id'],
           'rm': metadata_df['rm'],
           'beteckning': metadata_df['beteckning'],
           'titel': metadata_df['titel'],
           'datum': metadata_df['datum'],
           'debattnamn': metadata_df.get('debattnamn', ''),
           'dok_url_html': metadata_df.get('dok_url_html', ''),
           'dok_url_txt': metadata_df.get('dok_url_txt', ''),
         })
       
       # Parse Date
       df_clean['date'] = pd.to_datetime(df_clean['datum'])
       df_clean['year'] = df_clean['date'].dt.year
       df_clean['month'] = df_clean['date'].dt.month

       #Sort by date
       df_clean = df_clean.sort_values(by='date').reset_index(drop=True)

       return df_clean
    
    return pd.DataFrame()

if __name__ == "__main__":
    print("=" * 60)
    print("RIKSDAG METADATA DOWNLOADER")
    print("=" * 60)
    
    debates_df = download_all_metadata(2018, 2024)
    
    #Summary Statistics
    print("\n\n📊 SUMMARY:")
    print(f"Total debates downloaded: {len(debates_df)}")
    print(f"\nDebates by year:")
    print(debates_df['year'].value_counts().sort_index())

    #Save to CSV
    output_file = 'data/raw/riksdag_debates_metadata.csv'
    debates_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✅ Metadata saved to {output_file}")

    #Also save as json for backup
    output_json = 'data/raw/riksdag_debates_metadata.json'
    debates_df.to_json(output_json, orient='records', force_ascii=False, indent=2)
    print(f"✅ Metadata also saved to {output_json}")
