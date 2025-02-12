import torch
import pandas as pd
import pickle
import numpy as np
from typing import Dict, Tuple, Union, List

class PokemonBattlePredictor:
    def __init__(self, model_path: str = 'battle_predictor.pth', 
                 preprocessor_path: str = 'battle_predictor_preprocessors.pkl'):
        """
        Initialize the Pokemon Battle Predictor with trained model and preprocessors.
        
        Args:
            model_path: Path to the saved model weights
            preprocessor_path: Path to the saved preprocessors
        """
        # Load preprocessors
        with open(preprocessor_path, 'rb') as f:
            preprocessors = pickle.load(f)
            self.scaler = preprocessors['scaler']
            self.type_encoder = preprocessors['type_encoder']
            self.ability_encoder = preprocessors['ability_encoder']

        # Initialize model
        n_types = len(self.type_encoder.classes_)
        n_abilities = len(self.ability_encoder.classes_)
        
        from battle_transformer import PokemonTypeTransformer, PokemonCounterPredictor
        self.type_transformer = PokemonTypeTransformer(n_types=n_types, n_abilities=n_abilities)
        self.model = PokemonCounterPredictor(self.type_transformer, input_size=32+48)
        
        # Load trained weights
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def prepare_pokemon_data(self, pokemon_data: Dict) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Prepare pokemon data for model input.
        
        Args:
            pokemon_data: Dictionary containing pokemon stats and information
                Required keys: type1, type2, ability, and all numerical stats
        """
        # Encode types and ability
        type1_encoded = self.type_encoder.transform([pokemon_data['type1']])
        type2_encoded = self.type_encoder.transform([pokemon_data.get('type2', 'none')])
        ability_encoded = self.ability_encoder.transform([pokemon_data['ability']])

        # Prepare numerical features
        numerical_features = [
            pokemon_data['attack'], pokemon_data['defense'],
            pokemon_data['sp_attack'], pokemon_data['sp_defense'],
            pokemon_data['speed'], pokemon_data['hp'],
            pokemon_data['against_bug'], pokemon_data['against_dark'],
            pokemon_data['against_dragon'], pokemon_data['against_electric'],
            pokemon_data['against_fairy'], pokemon_data['against_fight'],
            pokemon_data['against_fire'], pokemon_data['against_flying'],
            pokemon_data['against_ghost'], pokemon_data['against_grass'],
            pokemon_data['against_ground'], pokemon_data['against_ice'],
            pokemon_data['against_normal'], pokemon_data['against_poison'],
            pokemon_data['against_psychic'], pokemon_data['against_rock'],
            pokemon_data['against_steel'], pokemon_data['against_water']
        ]
        
        scaled_features = self.scaler.transform([numerical_features])
        
        return (torch.tensor(type1_encoded), 
                torch.tensor(type2_encoded),
                torch.tensor(ability_encoded),
                torch.FloatTensor(scaled_features))

    def predict_battle(self, pokemon1: Dict, pokemon2: Dict) -> Tuple[float, str]:
        """
        Predict the outcome of a battle between two Pokemon.
        
        Args:
            pokemon1: Dictionary containing first pokemon's data
            pokemon2: Dictionary containing second pokemon's data
            
        Returns:
            Tuple containing:
                - Probability of pokemon1 winning (float between 0 and 1)
                - String description of the prediction
        """
        # Prepare data for both pokemon
        type1_1, type2_1, ability_1, stats_1 = self.prepare_pokemon_data(pokemon1)
        type1_2, type2_2, ability_2, stats_2 = self.prepare_pokemon_data(pokemon2)

        # Combine inputs and ensure correct shapes
        type1_ids = torch.stack([type1_1, type1_2]).reshape(1, 2)  # Add batch dimension
        type2_ids = torch.stack([type2_1, type2_2]).reshape(1, 2)  # Add batch dimension
        ability_ids = torch.stack([ability_1, ability_2]).reshape(1, 2)  # Add batch dimension
        stats = torch.cat([stats_1, stats_2], dim=1).reshape(1, -1)  # Add batch dimension

        # Make prediction
        with torch.no_grad():
            prediction = self.model(type1_ids, type2_ids, ability_ids, stats)
            win_probability = prediction.item()

        # Create result message
        result_msg = f"{pokemon1['name']} has a {win_probability*100:.1f}% chance of winning against {pokemon2['name']}"
        
        return win_probability, result_msg

    def get_valid_types(self) -> List[str]:
        """Return list of valid Pokemon types."""
        return list(self.type_encoder.classes_)

    def get_valid_abilities(self) -> List[str]:
        """Return list of valid Pokemon abilities."""
        return list(self.ability_encoder.classes_)
