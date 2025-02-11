import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('../pokemon.csv')

# Calculate total base stats
df['total_stats'] = df['hp'] + df['attack'] + df['defense'] + df['sp_attack'] + df['sp_defense'] + df['speed']

# Some known evolution families for analysis
evolution_families = {
    'Basic': ['Charmander', 'Charmeleon', 'Charizard'],
    'Branching': ['Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Espeon', 'Umbreon', 'Leafeon', 'Glaceon', 'Sylveon'],
    'Bug': ['Caterpie', 'Metapod', 'Butterfree'],
    'Dragon': ['Dratini', 'Dragonair', 'Dragonite']
}

# Create visualization
plt.figure(figsize=(15, 10))

for i, (family_name, pokemon_list) in enumerate(evolution_families.items()):
    # Get stats for each Pokemon in the family
    family_stats = df[df['name'].isin(pokemon_list)][['name', 'total_stats']]
    family_stats = family_stats.set_index('name')
    
    # Plot
    plt.subplot(2, 2, i+1)
    family_stats['total_stats'].plot(kind='bar')
    plt.title(f'{family_name} Evolution Line')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Total Base Stats')

plt.tight_layout()
plt.savefig('evolution_analysis.png')
print("Evolution analysis has been saved to 'evolution_analysis.png'")

# Print stat differences
print("\nStat Improvements in Evolution Lines:")
for family_name, pokemon_list in evolution_families.items():
    print(f"\n{family_name} Evolution Line:")
    family_stats = df[df['name'].isin(pokemon_list)][['name', 'total_stats']].set_index('name')
    
    for i in range(len(pokemon_list)-1):
        current = pokemon_list[i]
        next_form = pokemon_list[i+1]
        stat_diff = family_stats.loc[next_form, 'total_stats'] - family_stats.loc[current, 'total_stats']
        print(f"{current} → {next_form}: +{stat_diff} total stats") 