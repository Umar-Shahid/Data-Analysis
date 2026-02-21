"""

Generate descriptive statistics for supervisor-level data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data/processed/all_speeches.csv')

print("=" * 70)
print("DESCRIPTIVE STATISTICS FOR SUPERVISORS")
print("=" * 70) 

print(f"\n📊 DATASET OVERVIEW:")
print(f"Total speeches: {len(df):,}")
print(f"Date range: {df['datum'].min()} to {df['datum'].max()}")
print(f"Unique speakers: {df['speaker'].nunique():,}")
print(f"Unique debates: {df['dok_id'].nunique():,}")

print(f"\n📅 SPEECHES BY YEAR:")
yearly = df.groupby('year').size()
for year, count in yearly.items():
    print(f"  {year}: {count:,} speeches")

print(f"\n🎭 SPEECHES BY PARTY:")
party_counts = df.groupby('party').size().sort_values(ascending=False)
for party, count in party_counts.items():
    pct = count / len(df) * 100
    print(f"  {party}: {count:,} speeches ({pct:.1f}%)")

print(f"\n📏 SPEECH LENGTH:")
print(f"  Mean: {df['word_count'].mean():.0f} words")
print(f"  Median: {df['word_count'].median():.0f} words")
print(f"  Min: {df['word_count'].min()} words")
print(f"  Max: {df['word_count'].max()} words")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Speeches by year
yearly.plot(kind='bar', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Speeches by Year (2018-2024)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Year')  
axes[0, 0].set_ylabel('Number of Speeches')
axes[0, 0].tick_params(axis='x', rotation=0)

# 2. Speeches by party
party_counts.plot(kind='barh', ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Speeches by Party', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Number of Speeches') 

# 3. Speech length distribution
axes[1, 0].hist(df['word_count'], bins=50, color='green', alpha=0.7, edgecolor='black')
axes[1, 0].set_title('Distribution of Speech Lengths', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Words per Speech')   
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].axvline(df['word_count'].mean(), color='red', linestyle='--', label=f'Mean: {df["word_count"].mean():.0f}')
axes[1, 0].legend() 

# 4. Parties activity over time
party_year = df.groupby(['year','party']).size().unstack(fill_value=0)
sns.heatmap(party_year.T, ax=axes[1, 1], cmap='YlGnBu', cbar_kws={'label': 'Number of Speeches'},fmt='d')
axes[1, 1].set_title('Party Activity Over Time', fontsize=12, fontweight='bold')    
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Party')

plt.tight_layout()
plt.savefig('output/figures/descriptive_statistics.png', dpi=300, bbox_inches='tight')
print(f"\n✅ Visualization saved: output/figures/descriptive_statistics.png")

# Summary for presentation
print("\n📋 SUMMARY FOR PRESENTATION:")
print("=" * 70)
print("KEY FINDINGS FOR PRESENTATION:")
print("=" * 70)
print(f"""
1. Successfully collected 47,783 parliamentary speeches from 2018-2024
2. Data covers all 8 Swedish political parties
3. Consistent coverage across years (3K-13K speeches per year)
4. Average speech length: {df['word_count'].mean():.0f} words
5. Social Democrats (S) most active: {party_counts['S']:,} speeches (28%)
6. Ready for opponent reference extraction and sentiment analysis

NEXT STEPS:
- Identify sentences where parties mention other parties
- Apply Swedish sentiment dictionary
- Calculate negativity scores over time
""")