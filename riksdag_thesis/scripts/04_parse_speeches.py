"""
Parse Debate Transcripts into Individual Speeches
Extract speaker names, party affiliations, and speech 
texts from raw transcript files.
"""
import pandas as pd
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import xml.etree.ElementTree as ET
import html

def extract_metadata_from_xml(text):
    """Extract metadata"""
    try:
        xml_match = re.search(r'<dokument>(.*?)</dokument>', text, re.DOTALL)
        if xml_match:
            xml_text = '<dokument>' + xml_match.group(1) + '</dokument>'
            root = ET.fromstring(xml_text)
            
            metadata = {
                'dok_id': root.find('dok_id').text if root.find('dok_id') is not None else None,
                'datum': root.find('datum').text.split()[0] if root.find('datum') is not None else None,
                'titel': root.find('titel').text if root.find('titel') is not None else None,
                'rm': root.find('rm').text if root.find('rm') is not None else None
            }
            return metadata
    except:
        pass
    return {}

def parse_riksdag_html(html_text, filename=""):
    """Parse speeches - handles HTML entities properly"""
    
    speeches = []
    
    try:
        # Decode HTML entities FIRST
        html_decoded = html.unescape(html_text)
        
        soup = BeautifulSoup(html_decoded, 'html.parser')
        full_text = soup.get_text(separator='\n')
        
        # Now the text has real spaces instead of &#xa0;
        
        # PATTERN 1: "Anf. NUMBER NAME (PARTY)" or "Anf. NUMBER NAME (PARTY):"
        # Allows multiple spaces/whitespace
        pattern_anf = r'Anf\.\s+(\d+)\s+(.{5,80}?)\s+\(([A-ZÅÄÖ]+)\)\s*:?'
        
        matches_anf = []
        for match in re.finditer(pattern_anf, full_text):
            name_part = match.group(2).strip()
            # Clean up titles like "Försvarsminister", "Statsråd", etc.
            name_clean = re.sub(r'^(Försvarsminister|Statsråd|Minister|Statsminister|Talman)\s+', '', name_part, flags=re.IGNORECASE)
            
            matches_anf.append({
                'pos': match.start(),
                'speaker': name_clean.strip(),
                'party': match.group(3).strip(),
                'speech_num': match.group(1),
                'match_end': match.end(),
                'type': 'anf'
            })
        
        # PATTERN 2: Look for <h2> tags which often contain speaker info
        # These are more reliable than just text patterns
        h2_tags = soup.find_all('h2')

        for h2 in h2_tags:
            h2_text = h2.get_text()
            h2_match = re.search(r'(?:Anf\.\s+(\d+)\s+)?(.{5,80}?)\s+\(([A-ZÅÄÖ]+)\)', h2_text)
            if h2_match:
                name_part = h2_match.group(2).strip() if h2_match.group(2) else ""
                party = h2_match.group(3).strip()
                speech_num = h2_match.group(1) if h2_match.group(1) else None

                # Clean up titles like "Försvarsminister", "Statsråd", etc.
                name_clean = re.sub(r'^(Försvarsminister|Statsråd|Minister|Statsminister|Talman|Vice talman)\s+', '', name_part, flags=re.IGNORECASE)
                
                # Get position in full_text
                h2_pos = full_text.find(h2_text)

                if h2_pos >= 0 and name_clean:

                    # Check not duplicate
                    is_dup = any(abs(h2_pos - m['pos']) < 5 for m in matches_anf)
                    
                    if not is_dup:
                        matches_anf.append({
                            'pos': h2_pos,
                            'speaker': name_clean.strip(),
                            'party': party,
                            'speech_num': speech_num,
                            'match_end': h2_pos + len(h2_text),
                            'type': 'h2'
                    })
        # Sort all matches by position
        matches_anf.sort(key=lambda x: x['pos'])
        # Extract speeches based on matches
        for i, match_info in enumerate(matches_anf):
            speaker = match_info['speaker']
            party = match_info['party']
            start_pos = match_info['match_end']

            # Get text until next speech
            if i + 1 < len(matches_anf):
                end_pos = matches_anf[i + 1]['pos']
            else:
                end_pos = min(start_pos + 5000, len(full_text))
            speech_text = full_text[start_pos:end_pos].strip()

            # Clean
            speech_text = re.sub(r'\n+', ' ', speech_text)
            speech_text = re.sub(r'\s+', ' ', speech_text)

            # Remove remaining HTML artifacts
            speech_text = re.sub(r'<[^>]+>', '', speech_text)
            speech_text = re.sub(r'\s+', ' ', speech_text).strip()

            word_count = len(speech_text.split())

            # Filter: only keep if substantial and speaker name looks valid
            if word_count >= 30 and word_count <= 5000:
                # Check speaker name is reasonable (2+ words, not too long)
                speaker_words = speaker.split()
                if 2 <= len(speaker_words) <= 6 :
                    speeches.append({
                        'speaker': speaker,
                        'party': party,
                        'text': speech_text,
                        'word_count': word_count,
                        'speech_number': match_info['speech_num'],
                        
                })
    except Exception as e:
        print(f"\nError: {e}")
    
    return speeches

def parse_riksdag_transcript(filepath):
    """Parse speeches from Riksdag transcript text"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = extract_metadata_from_xml(content)
    html_match = re.search(r'<html>(.*?)</html>', content, re.DOTALL | re.IGNORECASE)
    if html_match:
        speeches = parse_riksdag_html(html_match.group(1), os.path.basename(filepath))
        for speech in speeches:
            speech.update(metadata)
        return speeches
    return []

def process_all_transcripts(transcript_dir='data/raw/transcripts'):
    """Process all transcript files in a directory and save to CSV"""

    files = [f for f in os.listdir(transcript_dir) 
             if f.endswith('.txt') and f != 'failed_downloads.txt']
    
    print(f"\n📝 Processing {len(files)} files...\n")
    
    all_speeches = []
    file_stats = []

    for filename in tqdm(files, desc="Parsing"):
        filepath = os.path.join(transcript_dir, filename)

        try:
            speeches = parse_riksdag_transcript(filepath)
            file_stats.append({
                'file': filename,
                'speeches': len(speeches)
            })
            all_speeches.extend(speeches)
        except:
            file_stats.append({
                'file': filename,   
                'speeches': 0
            })
    return pd.DataFrame(all_speeches), pd.DataFrame(file_stats)

if __name__ == "__main__":
    print("=" * 70)
    print("FINAL WORKING PARSER (HTML entity aware)")
    print("=" * 70)
    
    #Test
    print("\n🧪 Testing HC0940.txt...\n")

    test_file = 'data/raw/transcripts/HC0940.txt'
    speeches = parse_riksdag_transcript(test_file)

    print(f"✅ Found {len(speeches)} speeches\n")

    if len(speeches) > 0:
        print("Speeches found:")
        print("-" * 70)
        for i, s in enumerate(speeches[:10], 1):
            print(f"{i}. {s['speaker']} ({s['party']}) - {s['word_count']} words")
            print(f"   {s['text'][:100]}...")
            print()

    print("-" * 70)
    proceed = input("Process ALL transcripts in 'data/raw/transcripts'? (y/n): ")

    if proceed.lower() == 'y':
        speeches_df, stats_df = process_all_transcripts()

        if len(speeches_df) > 0:
            print("\n" + "=" * 70)
            print("RESULTS")
            print("=" * 70)

            speeches_df['year'] = pd.to_datetime(speeches_df['datum']).dt.year

            print(f"\n📊 TOTAL: {len(speeches_df):,} speeches")
            print(f"\n📅 BY YEAR:")

            for y,c in speeches_df['year'].value_counts().sort_index().items():
                print(f"  {y}: {c:,}")
            
            print(f"\n🎭 BY PARTY:")
            for p, c in speeches_df['party'].value_counts().items():
                print(f"  {p}: {c:,} ({c/len(speeches_df)*100:.1f}%)")

            print(f"\n📁 FILES:")
            print(f"  With speeches: {(stats_df['speeches']>0).sum()}/{len(stats_df)}")
            print(f"  Mean/file: {stats_df['speeches'].mean():.1f}")

            # Save to CSV
            speeches_df.to_csv('data/processed/all_speeches.csv', index=False,encoding='utf-8')
            stats_df.to_csv('data/processed/file_stats.csv', index=False)

            print(f"\n✅ Saved: data/processed/all_speeches.csv")
            print("\n🎉 DONE! Ready for analysis!")