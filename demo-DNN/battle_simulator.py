import pandas as pd
import numpy as np
import random
import kagglehub

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
        path = kagglehub.dataset_download("rounakbanik/pokemon")
        self.pokemon_data = pd.read_csv(path + "/pokemon.csv")
        
        # Type effectiveness chart
        self.type_chart = {
            'normal': {'normal': 1, 'fire': 1, 'water': 1, 'electric': 1, 'grass': 1, 'ice': 1, 'fighting': 1, 
                      'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 0.5, 'ghost': 0, 
                      'dragon': 1, 'dark': 1, 'steel': 0.5},
            'fire': {'normal': 1, 'fire': 0.5, 'water': 0.5, 'electric': 1, 'grass': 2, 'ice': 2, 'fighting': 1,
                    'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 2, 'rock': 0.5, 'ghost': 1,
                    'dragon': 0.5, 'dark': 1, 'steel': 2},
            'water': {'normal': 1, 'fire': 2, 'water': 0.5, 'electric': 1, 'grass': 0.5, 'ice': 1, 'fighting': 1,
                     'poison': 1, 'ground': 2, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 2, 'ghost': 1,
                     'dragon': 0.5, 'dark': 1, 'steel': 1},
            'electric': {'normal': 1, 'fire': 1, 'water': 2, 'electric': 0.5, 'grass': 0.5, 'ice': 1, 'fighting': 1,
                        'poison': 1, 'ground': 0, 'flying': 2, 'psychic': 1, 'bug': 1, 'rock': 1, 'ghost': 1,
                        'dragon': 0.5, 'dark': 1, 'steel': 1},
            'grass': {'normal': 1, 'fire': 0.5, 'water': 2, 'electric': 1, 'grass': 0.5, 'ice': 1, 'fighting': 1,
                     'poison': 0.5, 'ground': 2, 'flying': 0.5, 'psychic': 1, 'bug': 0.5, 'rock': 2, 'ghost': 1,
                     'dragon': 0.5, 'dark': 1, 'steel': 0.5},
            'ice': {'normal': 1, 'fire': 0.5, 'water': 0.5, 'electric': 1, 'grass': 2, 'ice': 0.5, 'fighting': 1,
                   'poison': 1, 'ground': 2, 'flying': 2, 'psychic': 1, 'bug': 1, 'rock': 1, 'ghost': 1,
                   'dragon': 2, 'dark': 1, 'steel': 0.5}
        }
        
        # Define moves database
        self.moves_database = {
            'Thunderbolt': Move('Thunderbolt', 'electric', 90, 100, 'special'),
            'Flamethrower': Move('Flamethrower', 'fire', 90, 100, 'special'),
            'Ice Beam': Move('Ice Beam', 'ice', 90, 100, 'special'),
            'Close Combat': Move('Close Combat', 'fighting', 120, 100, 'physical'),
            'Earthquake': Move('Earthquake', 'ground', 100, 100, 'physical'),
            'Dragon Claw': Move('Dragon Claw', 'dragon', 80, 100, 'physical'),
        }

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
        
        # Random factor (0.85 to 1.00)
        random_factor = random.uniform(0.85, 1.00)
        
        # Calculate final damage
        final_damage = int(base_damage * type_multiplier * stab * critical * random_factor)
        
        return final_damage

    def calculate_type_effectiveness(self, move_type: str, defender_type1: str, defender_type2: str = None) -> float:
        effectiveness = self.type_chart.get(move_type, {}).get(defender_type1, 1.0)
        if defender_type2 and pd.notna(defender_type2):
            effectiveness *= self.type_chart.get(move_type, {}).get(defender_type2, 1.0)
        return effectiveness 
