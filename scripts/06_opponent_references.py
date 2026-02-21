"""
Identify Opponent References in Speeches
"""

import pandas as pd
import re
from tqdm import tqdm

print("=" * 70)
print("06. IDENTIFYING OPPONENT REFERENCES IN SPEECHES")
print("=" * 70)

# Load Speeches Data

df = pd.read_csv('data/processed/all_speeches.csv')

# Party keywords in Swedish
PARTY_KEYWORDS = {
    'S': ['socialdemokrat', 'socialdemokraterna', 'sossarna', 's-parti'],
    'M': ['moderat', 'moderaterna', 'm-parti'],
    'SD': ['sverigedemokrat', 'sverigedemokraterna', 'sd-parti', 'sd'],
    'V': ['vänsterparti', 'vänsterpartiet', 'vänstern', 'v-parti'],
    'C': ['centerparti', 'centerpartiet', 'centern', 'c-parti'],
    'L': ['liberal', 'liberalerna', 'l-parti'],
    'MP': ['miljöparti', 'miljöpartiet', 'gröna', 'de gröna', 'mp'],
    'KD': ['kristdemokrat', 'kristdemokraterna', 'kd-parti', 'kd']
}

# Bloc keywords
BLOC_KEYWORDS = {
    'left_bloc': ['vänsterblocket', 'rödgröna'],
    'right_bloc': ['högerblocket', 'alliansen', 'borgerliga'],
    'government': ['regeringen', 'regeringspartierna'],
    'opposition': ['oppositionen']
}

def detect_party_mentions(text, speaker_party):
    """
    Detect which parties are mentioned in the text
    Returns list of mentioned parties (excluding speaker's own party)
    """
    text_lower = text.lower()
    mentioned_parties = []
    
    for party, keywords in PARTY_KEYWORDS.items():
        if party == speaker_party:
            continue  # Don't count mentions of own party
        
        for keyword in keywords:
            if keyword in text_lower:
                mentioned_parties.append(party)
                break  # Found this party, move to next
    
    return list(set(mentioned_parties))  # Remove duplicates

def has_opponent_reference(text, speaker_party):
    """Check if speech mentions any opponent"""
    mentions = detect_party_mentions(text, speaker_party)
    return len(mentions) > 0

# Process speeches to identify opponent references
print("\n🔍 Analyzing opponent references...")

df['has_opponent_ref'] = False
df['mentioned_parties'] = ''

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    text = row['text']
    party = row['party']
    
    # Check for opponent mentions
    mentioned = detect_party_mentions(text, party)

    df.at[idx, 'has_opponent_ref'] = len(mentioned) > 0
    df.at[idx, 'mentioned_parties'] = ','.join(mentioned) if mentioned else ''

# Calculate Statistics
total_speeches = len(df)
opponent_speeches = df['has_opponent_ref'].sum()    
opponent_pct = opponent_speeches / total_speeches * 100

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

print(f"\n📊 OVERALL:")
print(f"   Total speeches: {total_speeches:,}")
print(f"   Speeches with opponent references: {opponent_speeches:,}")
print(f"   Percentage : {opponent_pct:.1f}%")

print(f"\n🎭 BY PARTY (How often each party mentions opponents):")

party_opponent_rates = df.groupby('party')['has_opponent_ref'].agg(['sum', 'count'])
party_opponent_rates['pct'] = (party_opponent_rates['sum'] / party_opponent_rates['count'] * 100)
party_opponent_rates = party_opponent_rates.sort_values('pct', ascending=False)

for party, row in party_opponent_rates.iterrows():
    print(f"   {party}: {row['sum']:,} ({row['count']:,} out of {row['pct']:.1f})")    

# Create Opponent Mention Matrix
print(f"\n🔗 OPPONENT MENTION MATRIX:")
print("(Rows = Speaker Party, Columns = Mentioned Party)")

# Create matrix
opponent_matrix = pd.DataFrame(0, index=PARTY_KEYWORDS.keys(), columns=PARTY_KEYWORDS.keys())

for idx, row in df.iterrows():
    if row['mentioned_parties']:
        speaker = row['party']
        mentioned = row['mentioned_parties'].split(',')
        
        for target in mentioned:
            if target in opponent_matrix.columns:
                opponent_matrix.at[speaker, target] += 1

print("\n" + opponent_matrix.to_string())

# Save Results
df.to_csv('data/processed/speeches_with_opponents.csv', index=False, encoding='utf-8')
opponent_matrix.to_csv('output/tables/opponent_matrix.csv')

print(f"\n✅ Saved:")
print(f"  - data/processed/speeches_with_opponents.csv")
print(f"  - output/tables/opponent_matrix.csv")

# Visualization

import matplotlib.pyplot as plt
import seaborn as sns

fig , axes = plt.subplots(1,2,figsize=(14, 6))

# Chart 1: Opponent reference rate by party
party_opponent_rates['pct'].plot(kind='barh', ax=axes[0], color='steelblue')
axes[0].set_title('Opponent Reference Rate by Party', fontweight='bold')
axes[0].set_xlabel('Percentage of Speeches with Opponent References')
axes[0].set_ylabel('Party')

# Chart 2: Opponent Mention Matrix Heatmap
sns.heatmap(opponent_matrix, annot=True, fmt='d', cmap='YlOrRd'
            , ax=axes[1], cbar_kws={'label': 'Mentions'})
axes[1].set_title('Who Mentions Whom', fontweight='bold') 
axes[1].set_xlabel('Mentioned Party')
axes[1].set_ylabel('Speaker Party')

plt.tight_layout()
plt.savefig('output/figures/opponent_references.png', dpi=300, bbox_inches='tight')

print(f"  - output/figures/opponent_references.png")

print("\n" + "=" * 70)
print("✅ OPPONENT ANALYSIS COMPLETE!")
print("=" * 70)


      
    