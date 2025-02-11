import pandas as pd
import numpy as np
import random
from typing import Dict, List, Tuple

class Pokemon:
    def __init__(self, name: str, data: pd.Series):
        self.name = name
        self.max_hp = data['hp']
        self.current_hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.sp_attack = data['sp_attack']
        self.sp_defense = data['sp_defense']
        self.speed = data['speed']
        self.type1 = data['type1']
        self.type2 = data['type2'] if pd.notna(data['type2']) else None
        
        # Status conditions
        self.status = None  # Can be: burn, freeze, paralysis, poison, sleep
        self.status_counter = 0
        
        # Stat modifiers
        self.modifiers = {
            'attack': 1.0,
            'defense': 1.0,
            'sp_attack': 1.0,
            'sp_defense': 1.0,
            'speed': 1.0
        }

class Move:
    def __init__(self, name: str, type: str, power: int, accuracy: int, category: str):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.category = category  # 'physical' or 'special'

class BattleSimulator:
    def __init__(self):
        # Load Pokemon data
        self.pokemon_data = pd.read_csv('pokemon.csv')
        
        # Type effectiveness chart (using the one from type_effectiveness.py)
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
        
        # Define some sample moves
        self.moves_database = {
            'Thunderbolt': Move('Thunderbolt', 'electric', 90, 100, 'special'),
            'Flamethrower': Move('Flamethrower', 'fire', 90, 100, 'special'),
            'Ice Beam': Move('Ice Beam', 'ice', 90, 100, 'special'),
            'Close Combat': Move('Close Combat', 'fighting', 120, 100, 'physical'),
            'Earthquake': Move('Earthquake', 'ground', 100, 100, 'physical'),
            'Dragon Claw': Move('Dragon Claw', 'dragon', 80, 100, 'physical'),
        }

    def calculate_type_effectiveness(self, move_type: str, defender_type1: str, defender_type2: str = None) -> float:
        effectiveness = self.type_chart.get(move_type, {}).get(defender_type1, 1.0)
        if defender_type2:
            effectiveness *= self.type_chart.get(move_type, {}).get(defender_type2, 1.0)
        return effectiveness

    def apply_status_effects(self, pokemon: Pokemon):
        if pokemon.status == 'burn':
            damage = pokemon.max_hp // 16
            pokemon.current_hp -= damage
            print(f"{pokemon.name} is hurt by burn! (-{damage} HP)")
            pokemon.modifiers['attack'] = 0.5
        elif pokemon.status == 'poison':
            damage = pokemon.max_hp // 8
            pokemon.current_hp -= damage
            print(f"{pokemon.name} is hurt by poison! (-{damage} HP)")
        elif pokemon.status == 'paralysis':
            pokemon.modifiers['speed'] = 0.5
            if random.random() < 0.25:
                return False  # Pokemon is fully paralyzed
        elif pokemon.status == 'freeze':
            if random.random() < 0.2:
                pokemon.status = None
                print(f"{pokemon.name} thawed out!")
            else:
                return False  # Pokemon is frozen
        elif pokemon.status == 'sleep':
            if pokemon.status_counter == 0:
                pokemon.status = None
                print(f"{pokemon.name} woke up!")
            else:
                pokemon.status_counter -= 1
                return False  # Pokemon is asleep
        return True

    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, move: Move) -> int:
        # Base damage formula
        if move.category == 'physical':
            attack = attacker.attack * attacker.modifiers['attack']
            defense = defender.defense * defender.modifiers['defense']
        else:
            attack = attacker.sp_attack * attacker.modifiers['sp_attack']
            defense = defender.sp_defense * defender.modifiers['sp_defense']

        # Calculate base damage
        level = 50  # Assuming level 50 for all Pokemon
        base_damage = ((2 * level / 5 + 2) * move.power * attack / defense / 50) + 2

        # Type effectiveness
        type_multiplier = self.calculate_type_effectiveness(move.type, defender.type1, defender.type2)
        
        # STAB (Same Type Attack Bonus)
        stab = 1.5 if move.type in [attacker.type1, attacker.type2] else 1.0
        
        # Critical hit (1/16 chance)
        critical = 1.5 if random.random() < 0.0625 else 1.0
        if critical > 1:
            print("A critical hit!")

        # Random factor (0.85 to 1.00)
        random_factor = random.uniform(0.85, 1.0)
        
        # Calculate final damage
        final_damage = int(base_damage * type_multiplier * stab * critical * random_factor)
        
        # Print effectiveness message
        if type_multiplier > 1:
            print("It's super effective!")
        elif type_multiplier < 1 and type_multiplier > 0:
            print("It's not very effective...")
        elif type_multiplier == 0:
            print("It doesn't affect the opposing Pokemon...")

        return final_damage

    def simulate_battle(self, pokemon1_name: str, pokemon2_name: str) -> str:
        # Initialize Pokemon
        pokemon1_data = self.pokemon_data[self.pokemon_data['name'] == pokemon1_name].iloc[0]
        pokemon2_data = self.pokemon_data[self.pokemon_data['name'] == pokemon2_name].iloc[0]
        
        pokemon1 = Pokemon(pokemon1_name, pokemon1_data)
        pokemon2 = Pokemon(pokemon2_name, pokemon2_data)
        
        # Assign random moves to each Pokemon
        pokemon1_moves = random.sample(list(self.moves_database.values()), 4)
        pokemon2_moves = random.sample(list(self.moves_database.values()), 4)

        print(f"\nBattle Start: {pokemon1_name} vs {pokemon2_name}!")
        print(f"{pokemon1_name} HP: {pokemon1.current_hp}")
        print(f"{pokemon2_name} HP: {pokemon2.current_hp}\n")

        turn = 1
        while True:
            print(f"\nTurn {turn}")
            
            # Determine order based on speed
            first = pokemon1 if pokemon1.speed * pokemon1.modifiers['speed'] >= pokemon2.speed * pokemon2.modifiers['speed'] else pokemon2
            second = pokemon2 if first == pokemon1 else pokemon1
            first_moves = pokemon1_moves if first == pokemon1 else pokemon2_moves
            second_moves = pokemon2_moves if first == pokemon1 else pokemon1_moves

            # First Pokemon's turn
            if self.apply_status_effects(first):
                move = random.choice(first_moves)
                print(f"{first.name} used {move.name}!")
                if random.random() * 100 < move.accuracy:
                    damage = self.calculate_damage(first, second, move)
                    second.current_hp -= damage
                    print(f"{second.name} took {damage} damage! ({second.current_hp} HP remaining)")
                else:
                    print("But it missed!")

            if second.current_hp <= 0:
                return first.name

            # Second Pokemon's turn
            if self.apply_status_effects(second):
                move = random.choice(second_moves)
                print(f"{second.name} used {move.name}!")
                if random.random() * 100 < move.accuracy:
                    damage = self.calculate_damage(second, first, move)
                    first.current_hp -= damage
                    print(f"{first.name} took {damage} damage! ({first.current_hp} HP remaining)")
                else:
                    print("But it missed!")

            if first.current_hp <= 0:
                return second.name

            turn += 1

def main():
    simulator = BattleSimulator()
    
    test_battles = [
        ('Mewtwo', 'Charizard'),
        # ('Charizard', 'Blastoise'),
        # ('Mewtwo', 'Gengar'),
        # ('Dragonite', 'Tyranitar'),
    ]
    
    for pokemon1, pokemon2 in test_battles:
        winner = simulator.simulate_battle(pokemon1, pokemon2)
        print(f"\nWinner: {winner}!")
        print("-" * 50)

if __name__ == "__main__":
    main() 
