"""
Create summary for supervisor presentation

"""

import pandas as pd

print("=" * 70)
print("SUMMARY FOR SUPERVISORS")
print("=" * 70)

# Load data
speeches = pd.read_csv('data/processed/speeches_with_opponents.csv')
opponent_matrix = pd.read_csv('output/tables/opponent_matrix.csv', index_col=0)

print(f"""
DATA COLLECTION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━

📥 Source: Riksdag Open Data API
📅 Period: 2018-2024
📊 Total Speeches: {len(speeches):,}

Coverage by Year:
""")

yearly = speeches.groupby('year').size()
for year, count in yearly.items():
    print(f"  {year}: {count:,} speeches")

print(f"""
Coverage by Party:
""")
party = speeches.groupby('party').size().sort_values(ascending=False)
for p, count in party.items():
    pct = count / len(speeches) * 100
    print(f"  {p}: {count:,} ({pct:.1f}%)")

# Opponent references
opponent_speeches = speeches['has_opponent_ref'].sum()
opponent_pct = opponent_speeches / len(speeches) * 100

print(f"""
OPPONENT REFERENCES IDENTIFIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ {opponent_speeches:,} speeches mention opponent parties
✓ {opponent_pct:.1f}% of all speeches contain opponent references
✓ Matrix created showing who mentions whom

Most Active in Mentioning Opponents:
""")

top_mentioners = speeches.groupby('party')['has_opponent_ref'].mean().sort_values(ascending=False).head(5)
for party, rate in top_mentioners.items():
    print(f"  {party}: {rate*100:.1f}% of their speeches")  

print(f"""
Most Mentioned Parties:
""")

# Count total mentions received
mentions_received = opponent_matrix.sum(axis=0).sort_values(ascending=False)
for party, count in mentions_received.head(5).items():
    print(f"  {party}: mentioned {count:,} times")

print(f"""
NEXT STEPS
━━━━━━━━━━

1. ✓ Data collection complete
2. ✓ Opponent references identified
3. ⏳ Sentiment analysis (dictionary-based)
4. ⏳ Statistical modeling
5. ⏳ Visualization of trends

FILES GENERATED:
- data/processed/all_speeches.csv
- data/processed/speeches_with_opponents.csv
- output/figures/basic_stats.png
- output/figures/opponent_references.png
- output/tables/opponent_matrix.csv
"""
)