"""Battle simulator module."""
import random
import pandas as pd
from app.utils.constants import TYPE_EFFECTIVENESS, TYPE_MOVES

class Pokemon:
    """Class representing a Pokemon in battle."""
    
    def __init__(self, data: pd.Series):
        """Initialize Pokemon with data from DataFrame row."""
        self.name = data['name']
        self.types = [data['type1']]
        if pd.notna(data['type2']):
            self.types.append(data['type2'])
        self.hp = data['hp']
        self.current_hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.sp_attack = data['sp_attack']
        self.sp_defense = data['sp_defense']
        self.speed = data['speed']
        
    def is_fainted(self) -> bool:
        """Check if Pokemon has fainted."""
        return self.current_hp <= 0
        
    def calculate_damage(self, move_power: int, attacker_stat: int, 
                        defender_stat: int, type_effectiveness: float) -> int:
        """Calculate damage for an attack."""
        # Basic damage formula based on Pokemon games
        base_damage = ((2 * 50 / 5 + 2) * move_power * attacker_stat / defender_stat) / 50 + 2
        # Apply random factor (85-100%)
        random_factor = random.uniform(0.85, 1.0)
        # Apply type effectiveness
        final_damage = int(base_damage * type_effectiveness * random_factor)
        return max(1, final_damage)  # Minimum 1 damage

class BattleSimulator:
    """Class for simulating Pokemon battles."""
    
    def __init__(self, pokemon_df: pd.DataFrame):
        """Initialize battle simulator with Pokemon data."""
        self.pokemon_df = pokemon_df
        self.battle_log = []
        
    def log(self, message: str):
        """Add message to battle log."""
        self.battle_log.append(message)
        
    def get_type_effectiveness(self, move_type: str, defender_types: list) -> float:
        """Calculate type effectiveness multiplier."""
        effectiveness = 1.0
        for def_type in defender_types:
            if def_type and pd.notna(def_type):
                if move_type.lower() in TYPE_EFFECTIVENESS and def_type.lower() in TYPE_EFFECTIVENESS[move_type.lower()]:
                    effectiveness *= TYPE_EFFECTIVENESS[move_type.lower()][def_type.lower()]
        return effectiveness
        
    def simulate_turn(self, attacker: Pokemon, defender: Pokemon) -> None:
        """Simulate one turn of battle."""
        # For simplicity, use a basic move with power based on attack stat
        move_power = 80
        is_special = random.choice([True, False])
        
        # Choose attack type randomly from attacker's types
        move_type = random.choice(attacker.types)
        
        # Get a random move of the chosen type
        if move_type.lower() in TYPE_MOVES:
            move_name = random.choice(TYPE_MOVES[move_type.lower()])
        else:
            move_name = "Attack"
        
        # Calculate stats to use
        atk_stat = attacker.sp_attack if is_special else attacker.attack
        def_stat = defender.sp_defense if is_special else defender.defense
        
        # Calculate type effectiveness
        effectiveness = self.get_type_effectiveness(move_type, defender.types)
        
        # Calculate and apply damage
        damage = attacker.calculate_damage(move_power, atk_stat, def_stat, effectiveness)
        defender.current_hp -= damage
        
        # Log the attack
        effectiveness_text = ""
        if effectiveness > 1:
            effectiveness_text = "It's super effective!"
        elif effectiveness < 1:
            effectiveness_text = "It's not very effective..."
            
        self.log(f"{attacker.name} used {move_name}!")
        if effectiveness_text:
            self.log(effectiveness_text)
        self.log(f"{defender.name} took {damage} damage!")
        if defender.is_fainted():
            self.log(f"{defender.name} fainted!")
        else:
            self.log(f"{defender.name} has {defender.current_hp} HP remaining!")
        
    def simulate_battle(self, pokemon1_name: str, pokemon2_name: str) -> list:
        """Simulate a battle between two Pokemon."""
        # Reset battle log
        self.battle_log = []
        
        # Get Pokemon data
        pokemon1_data = self.pokemon_df[self.pokemon_df['name'] == pokemon1_name].iloc[0]
        pokemon2_data = self.pokemon_df[self.pokemon_df['name'] == pokemon2_name].iloc[0]
        
        # Create Pokemon instances
        pokemon1 = Pokemon(pokemon1_data)
        pokemon2 = Pokemon(pokemon2_data)
        
        self.log(f"Battle between {pokemon1.name} and {pokemon2.name} begins!")
        
        # Main battle loop
        while not (pokemon1.is_fainted() or pokemon2.is_fainted()):
            # Determine turn order based on speed
            if pokemon1.speed >= pokemon2.speed:
                first, second = pokemon1, pokemon2
            else:
                first, second = pokemon2, pokemon1
                
            # First Pokemon attacks
            self.simulate_turn(first, second)
            if second.is_fainted():
                break
                
            # Second Pokemon attacks
            self.simulate_turn(second, first)
            
        # Determine winner
        winner = pokemon1 if pokemon2.is_fainted() else pokemon2
        self.log(f"\n{winner.name} wins the battle!")
        
        return self.battle_log 
