import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('../pokemon.csv')

# Calculate total stats
df['total_stats'] = df['hp'] + df['attack'] + df['defense'] + df['sp_attack'] + df['sp_defense'] + df['speed']

def analyze_pokemon(name):
    pokemon = df[df['name'] == name].iloc[0]
    
    # Get defensive strengths/weaknesses
    resistances = []
    weaknesses = []
    for col in df.columns:
        if col.startswith('against_'):
            type_name = col.replace('against_', '')
            effectiveness = pokemon[col]
            if effectiveness < 1:
                resistances.append(f"{type_name} ({effectiveness}x)")
            elif effectiveness > 1:
                weaknesses.append(f"{type_name} ({effectiveness}x)")
    
    print(f"\n=== {name} Analysis ===")
    print(f"Type: {pokemon['type1']}/{pokemon['type2'] if pd.notna(pokemon['type2']) else 'None'}")
    print(f"Total Stats: {pokemon['total_stats']}")
    print("\nStat Breakdown:")
    print(f"HP: {pokemon['hp']}")
    print(f"Attack: {pokemon['attack']}")
    print(f"Defense: {pokemon['defense']}")
    print(f"Sp. Attack: {pokemon['sp_attack']}")
    print(f"Sp. Defense: {pokemon['sp_defense']}")
    print(f"Speed: {pokemon['speed']}")
    print("\nStrengths (Resistances):", ', '.join(resistances))
    print("Weaknesses:", ', '.join(weaknesses))

# Example of a balanced team with different roles
suggested_team = {
    'Tyranitar': 'Physical Tank/Attacker',
    'Gengar': 'Special Attacker',
    'Starmie': 'Fast Special Attacker/Coverage',
    'Dragonite': 'All-around Powerhouse',
    'Ferrothorn': 'Defensive Wall',
    'Garchomp': 'Physical Attacker/Speed'
}

print("Suggested Balanced Team Analysis:")
print("================================")
for pokemon, role in suggested_team.items():
    print(f"\nRole: {role}")
    analyze_pokemon(pokemon)

# Create type coverage visualization
print("\nTeam Type Coverage:")
team_df = df[df['name'].isin(suggested_team.keys())]
coverage_data = team_df[[col for col in df.columns if col.startswith('against_')]].mean()

plt.figure(figsize=(12, 6))
coverage_data.plot(kind='bar')
plt.title('Team Type Coverage (Lower is Better)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('team_coverage.png')

print("\nKey Team Building Principles:")
print("1. Type Coverage: Different types to cover each other's weaknesses")
print("2. Role Distribution: Mix of attackers, defenders, and support")
print("3. Stat Balance: Some fast Pokemon, some tanky ones")
print("4. Move Variety: Consider Pokemon that can learn diverse move types")
print("5. Resistance Coverage: Team should resist most types collectively") 