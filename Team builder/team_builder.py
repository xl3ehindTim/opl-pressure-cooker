import pandas as pd
import numpy as np
from itertools import combinations

class TeamBuilder:
    def __init__(self, pokemon_df):
        self.pokemon_df = pokemon_df
        self.type_chart = {
            'normal': {'rock': 0.5, 'ghost': 0, 'steel': 0.5},
            'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 2, 'bug': 2, 'rock': 0.5, 'dragon': 0.5, 'steel': 2},
            'water': {'fire': 2, 'water': 0.5, 'grass': 0.5, 'ground': 2, 'rock': 2, 'dragon': 0.5},
            'electric': {'water': 2, 'electric': 0.5, 'grass': 0.5, 'ground': 0, 'flying': 2, 'dragon': 0.5},
            'grass': {'fire': 0.5, 'water': 2, 'grass': 0.5, 'poison': 0.5, 'ground': 2, 'flying': 0.5, 'bug': 0.5, 'rock': 2, 'dragon': 0.5, 'steel': 0.5},
            'ice': {'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 0.5, 'ground': 2, 'flying': 2, 'dragon': 2, 'steel': 0.5},
            'fighting': {'normal': 2, 'ice': 2, 'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 2, 'ghost': 0, 'dark': 2, 'steel': 2},
            'poison': {'grass': 2, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0},
            'ground': {'fire': 2, 'electric': 2, 'grass': 0.5, 'poison': 2, 'flying': 0, 'bug': 0.5, 'rock': 2, 'steel': 2},
            'flying': {'electric': 0.5, 'grass': 2, 'fighting': 2, 'bug': 2, 'rock': 0.5, 'steel': 0.5},
            'psychic': {'fighting': 2, 'poison': 2, 'psychic': 0.5, 'dark': 0, 'steel': 0.5},
            'bug': {'fire': 0.5, 'grass': 2, 'fighting': 0.5, 'poison': 0.5, 'flying': 0.5, 'psychic': 2, 'ghost': 0.5, 'dark': 2, 'steel': 0.5},
            'rock': {'fire': 2, 'ice': 2, 'fighting': 0.5, 'ground': 0.5, 'flying': 2, 'bug': 2, 'steel': 0.5},
            'ghost': {'normal': 0, 'psychic': 2, 'ghost': 2, 'dark': 0.5},
            'dragon': {'dragon': 2, 'steel': 0.5},
            'dark': {'fighting': 0.5, 'psychic': 2, 'ghost': 2, 'dark': 0.5},
            'steel': {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2, 'rock': 2, 'steel': 0.5}
        }

    def calculate_defensive_coverage(self, types):
        """Calculate defensive coverage for a set of types"""
        weaknesses = set()
        resistances = set()
        immunities = set()
        
        for def_type in types:
            if pd.isna(def_type):
                continue
            for atk_type, effectiveness in self.type_chart.items():
                multiplier = effectiveness.get(def_type, 1.0)
                if multiplier == 2:
                    weaknesses.add(atk_type)
                elif multiplier == 0.5:
                    resistances.add(atk_type)
                elif multiplier == 0:
                    immunities.add(atk_type)
        
        return weaknesses, resistances, immunities

    def calculate_offensive_coverage(self, types):
        """Calculate offensive coverage (super effective hits)"""
        coverage = set()
        for atk_type in types:
            if pd.isna(atk_type):
                continue
            for def_type, effectiveness in self.type_chart.items():
                if effectiveness.get(atk_type, 1.0) == 2:
                    coverage.add(def_type)
        return coverage

    def calculate_team_stats(self, team):
        """Calculate average and standard deviation of team stats"""
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        team_stats = {stat: [] for stat in stats}
        
        for pokemon in team:
            for stat in stats:
                team_stats[stat].append(pokemon[stat])
        
        return {
            'averages': {stat: np.mean(values) for stat, values in team_stats.items()},
            'balance': {stat: np.std(values) for stat, values in team_stats.items()}
        }

    def evaluate_team(self, team):
        """Evaluate overall team composition"""
        # Get all types in team
        team_types = [(p['type1'], p['type2']) for p in team]
        all_types = [t for types in team_types for t in types if pd.notna(t)]
        
        # Calculate defensive coverage
        weaknesses, resistances, immunities = self.calculate_defensive_coverage(all_types)
        
        # Calculate offensive coverage
        offensive_coverage = self.calculate_offensive_coverage(all_types)
        
        # Calculate team stats
        team_stats = self.calculate_team_stats(team)
        
        # Score calculation
        score = 0
        score += len(offensive_coverage) * 2  # Reward offensive coverage
        score -= len(weaknesses)  # Penalize weaknesses
        score += len(resistances) * 0.5  # Reward resistances
        score += len(immunities) * 1.5  # Reward immunities
        
        # Balance score
        avg_speed = team_stats['averages']['speed']
        avg_bulk = (team_stats['averages']['hp'] + team_stats['averages']['defense'] + team_stats['averages']['sp_defense']) / 3
        score += (avg_speed + avg_bulk) / 100  # Reward good speed and bulk
        
        return score, weaknesses, resistances, immunities, offensive_coverage, team_stats

    def build_team(self, core_pokemon_name, team_size=6):
        """Build optimal team around a core Pokemon"""
        # Get core Pokemon
        core_pokemon = self.pokemon_df[self.pokemon_df['name'] == core_pokemon_name].iloc[0]
        team = [core_pokemon]
        
        remaining_pokemon = self.pokemon_df[self.pokemon_df['name'] != core_pokemon_name]
        
        while len(team) < team_size:
            best_score = -float('inf')
            best_pokemon = None
            
            for _, candidate in remaining_pokemon.iterrows():
                test_team = team + [candidate]
                score, *_ = self.evaluate_team(test_team)
                
                if score > best_score:
                    best_score = score
                    best_pokemon = candidate
            
            if best_pokemon is not None:
                team.append(best_pokemon)
                remaining_pokemon = remaining_pokemon[remaining_pokemon['name'] != best_pokemon['name']]
        
        return team

    def print_team_analysis(self, team):
        """Print detailed team analysis"""
        score, weaknesses, resistances, immunities, offensive_coverage, team_stats = self.evaluate_team(team)
        
        print("\nTeam Composition:")
        for i, pokemon in enumerate(team, 1):
            print(f"{i}. {pokemon['name']} ({pokemon['type1']}/{pokemon['type2'] if pd.notna(pokemon['type2']) else '-'})")
            print(f"   Stats: HP={pokemon['hp']}, Atk={pokemon['attack']}, Def={pokemon['defense']}, ",
                  f"SpA={pokemon['sp_attack']}, SpD={pokemon['sp_defense']}, Spe={pokemon['speed']}")
        
        print("\nTeam Analysis:")
        print(f"Overall Score: {score:.2f}")
        print(f"Weaknesses: {', '.join(sorted(weaknesses))}")
        print(f"Resistances: {', '.join(sorted(resistances))}")
        print(f"Immunities: {', '.join(sorted(immunities))}")
        print(f"Offensive Coverage: {', '.join(sorted(offensive_coverage))}")
        
        print("\nTeam Stats Averages:")
        for stat, value in team_stats['averages'].items():
            print(f"{stat.upper()}: {value:.1f}")

def main():
    # Read Pokemon data
    pokemon_df = pd.read_csv('../pokemon.csv')
    
    # Create team builder
    builder = TeamBuilder(pokemon_df)
    
    core_pokemon = "Snivy"
    team = builder.build_team(core_pokemon)
    
    # Print team analysis
    builder.print_team_analysis(team)

if __name__ == "__main__":
    main()
