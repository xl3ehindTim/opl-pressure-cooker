from transformer_based_pokemon import PokemonBattlePredictor
from kagglehub import kagglehub
import pandas as pd
import ast
import numpy as np

# Load data
path = kagglehub.dataset_download("rounakbanik/pokemon")
pokemon_data = pd.read_csv(path + "/pokemon.csv")

# Helper function to get first ability from the abilities list
def get_first_ability(abilities_str):
    abilities_list = ast.literal_eval(abilities_str)
    return abilities_list[0]

# Add single ability field to the dataframe
pokemon_data['ability'] = pokemon_data['abilities'].apply(get_first_ability)

# Replace NaN in type2 with 'none'
pokemon_data['type2'] = pokemon_data['type2'].fillna('none')

predictor = PokemonBattlePredictor()

# Get Pokemon data and add the single ability field
charizard = pokemon_data[pokemon_data['name'] == 'Charizard'].iloc[0].to_dict()
blastoise = pokemon_data[pokemon_data['name'] == 'Blastoise'].iloc[0].to_dict()

probability, result = predictor.predict_battle(charizard, blastoise)
print(result)
print(probability)