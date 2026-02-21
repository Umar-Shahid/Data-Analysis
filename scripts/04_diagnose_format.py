"""
Diagnose the exact format of Riksdag transcripts
"""

import re
import os
from bs4 import BeautifulSoup

def diagnose_transcript(filepath):
    """Deep dive into transcript structure"""
    
    print("=" * 70)
    print("TRANSCRIPT FORMAT DIAGNOSIS")
    print("=" * 70)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nFile: {os.path.basename(filepath)}")
    print(f"Total length: {len(content):,} characters\n")
    
    # 1. Extract HTML section
    print("1. EXTRACTING HTML SECTION...")
    html_match = re.search(r'<html>(.*?)(?:</html>|$)', content, re.DOTALL | re.IGNORECASE)
    
    if html_match:
        html_content = html_match.group(1)
        print(f"   ✓ Found HTML section ({len(html_content):,} chars)")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 2. Look for all text
        full_text = soup.get_text(separator='\n')
        print(f"   ✓ Extracted text ({len(full_text):,} chars)")
        
        # 3. Search for common Swedish parliamentary terms
        print("\n2. SEARCHING FOR KEY TERMS...")
        
        terms = {
            'Anförande': full_text.count('Anförande'),
            'Talman': full_text.count('Talman'),
            'Ledamot': full_text.count('Ledamot'),
            'Minister': full_text.count('Minister'),
            '(S)': full_text.count('(S)'),
            '(M)': full_text.count('(M)'),
            '(SD)': full_text.count('(SD)'),
            '(V)': full_text.count('(V)'),
            '(C)': full_text.count('(C)'),
            '(L)': full_text.count('(L)'),
            '(MP)': full_text.count('(MP)'),
            '(KD)': full_text.count('(KD)'),
        }
        
        for term, count in terms.items():
            if count > 0:
                print(f"   '{term}': {count} occurrences")
        
        # 4. Find all potential speaker patterns
        print("\n3. FINDING SPEAKER PATTERNS...")
        
        # Pattern 1: Name (Party)
        pattern1 = re.findall(
            r'([A-ZÅÄÖ][a-zåäö]+\s+[A-ZÅÄÖ][a-zåäö]+)\s*\(([SMVCLKD]+)\)',
            full_text[:50000]
        )
        
        if pattern1:
            print(f"\n   Pattern 'Name Name (P)': Found {len(pattern1)} matches")
            print("   First 10 matches:")
            for name, party in pattern1[:10]:
                print(f"     {name} ({party})")
        
        # Pattern 2: Just party codes
        pattern2 = re.findall(r'\(([SMVCLKD]{1,2})\)', full_text[:20000])
        if pattern2:
            print(f"\n   Party codes found: {len(set(pattern2))} unique")
            print(f"   Parties: {set(pattern2)}")
        
        # 5. Show structure around first potential speech
        print("\n4. EXAMINING STRUCTURE AROUND FIRST SPEAKER...")
        
        # Find first occurrence of Anförande or similar
        anforande_pos = full_text.find('Anförande')
        if anforande_pos == -1:
            anforande_pos = full_text.find('§')  # Section markers
        
        if anforande_pos >= 0:
            # Show 2000 chars around it
            start = max(0, anforande_pos - 200)
            end = min(len(full_text), anforande_pos + 2000)
            
            print(f"\n   Context around position {anforande_pos}:")
            print("   " + "-" * 66)
            print(full_text[start:end])
            print("   " + "-" * 66)
        
        # 6. Look at HTML structure
        print("\n5. HTML STRUCTURE ANALYSIS...")
        
        # Find all headers
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        print(f"\n   Found {len(headers)} headers (h1-h4)")
        
        if headers:
            print("\n   First 10 headers:")
            for i, h in enumerate(headers[:10], 1):
                print(f"     {i}. <{h.name}> {h.get_text(strip=True)[:80]}")
        
        # Find all paragraphs
        paragraphs = soup.find_all('p')
        print(f"\n   Found {len(paragraphs)} paragraphs")
        
        if paragraphs:
            print("\n   First 5 non-empty paragraphs:")
            count = 0
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and len(text) > 20:
                    print(f"     {count+1}. {text[:100]}...")
                    count += 1
                    if count >= 5:
                        break
        
        # Look for div classes
        divs = soup.find_all('div', class_=True)
        classes = set()
        for div in divs:
            classes.update(div.get('class', []))
        
        if classes:
            print(f"\n   Found {len(classes)} unique div classes:")
            for cls in sorted(classes)[:20]:
                print(f"     .{cls}")
        
        # 7. Try to find actual speech content
        print("\n6. SEARCHING FOR ACTUAL SPEECH CONTENT...")
        
        # Look for paragraphs with substantial text
        substantial_paragraphs = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 100:  # Substantial content
                substantial_paragraphs.append(text)
        
        if substantial_paragraphs:
            print(f"\n   Found {len(substantial_paragraphs)} substantial paragraphs (>100 chars)")
            print("\n   First substantial paragraph:")
            print("   " + "-" * 66)
            print("   " + substantial_paragraphs[0][:500])
            print("   " + "-" * 66)
        
        # 8. Check for specific Riksdag markers
        print("\n7. CHECKING RIKSDAG-SPECIFIC MARKERS...")
        
        # Common Riksdag debate markers
        markers = [
            'anförande',
            'talman',
            'fru talman',
            'herr talman', 
            'ledamot',
            'statsråd',
            'replik',
            'svar på interpellation'
        ]
        
        for marker in markers:
            count = full_text.lower().count(marker.lower())
            if count > 0:
                print(f"   '{marker}': {count} occurrences")
                
                # Show first occurrence
                pos = full_text.lower().find(marker.lower())
                if pos >= 0:
                    context_start = max(0, pos - 100)
                    context_end = min(len(full_text), pos + 300)
                    print(f"     First occurrence context:")
                    print(f"     ...{full_text[context_start:context_end]}...")
                    print()
    
    else:
        print("   ✗ No HTML section found!")
        
        # Show raw content structure
        print("\n   First 3000 characters of raw content:")
        print("   " + "-" * 66)
        print(content[:3000])
        print("   " + "-" * 66)

if __name__ == "__main__":
    transcript_dir = 'data/raw/transcripts'
    files = [f for f in os.listdir(transcript_dir) 
             if f.endswith('.txt') and f != 'failed_downloads.txt']
    
    if files:
        # Diagnose first file
        test_file = os.path.join(transcript_dir, files[0])
        diagnose_transcript(test_file)
        
        print("\n\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("""
Based on the output above, I need to know:

1. What terms appear most frequently?
   (Anförande, Talman, Ledamot, etc.)

2. What does the structure around speakers look like?
   (The context section will show this)

3. Are there HTML classes or tags that mark speeches?
   (Check the div classes section)

4. What do substantial paragraphs contain?
   (Are they speeches, or something else?)

Send me this complete output and I'll write the perfect parser!
        """)
    else:
        print("No transcript files found!")