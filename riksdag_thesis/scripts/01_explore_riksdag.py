"""
Exploration of Riksdag Open Data API
Goal: Finding all parliamentary debate transcripts 2018-2024
"""

import requests
import json
import pandas as pd
from datetime import datetime

# Riksdag API
BASE_URL = "https://data.riksdagen.se/dokumentlista/"

def test_riksdag_api():
    """ Test connection to Riksdag Open Data API """
    
    print("Testing Riksdag Open Data API...")
    
    params = {
        'doktyp': 'prot',  # protokoll (debate transcripts)
        'from': '2023-01-01',
        'tom': '2023-01-31',
        'utformat': 'json',
        'sort': 'datum'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            print("✅ API connection successful!")
            
            data = response.json()
            
            if 'dokumentlista' in data:
                docs = data['dokumentlista']['dokument']
                print(f"\n📊 Found {len(docs)} documents for Jan 2023")
                
                if len(docs) > 0:
                    print("\n📄 Sample document structure:")
                    print(json.dumps(docs[0], indent=2, ensure_ascii=False))
                    
                return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
def get_available_years():
    """ Check which years have data available """
    
    print("\n\nChecking available years...")
    
    years_with_data = [] 

    for year in range(2018, 2025):

        params = {
            'doktyp': 'prot',
            'from': f'{year}-01-01',
            'tom': f'{year}-12-31',
            'utformat': 'json',
            
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'dokumentlista' in data:
                    count = len(data['dokumentlista']['dokument'])
                    print(f"  {year}: {count} documents")
                    years_with_data.append({
                        'year': year,
                        'count': count
                    })
                
        except:
            pass

    return pd.DataFrame(years_with_data)

if __name__ == "__main__":

    success = test_riksdag_api()

    if success:
        # Get Overview of available data
        df = get_available_years()
        print("\n✅ Available years with document counts:")
        print(df)
        print(f"\nTotal documents: {df['count'].sum()}")

        #Save summary
        df.to_csv('data/riksdag_available_years.csv', index=False)
        print("\n✅ Saved overview to data/riksdag_available_years.csv")
