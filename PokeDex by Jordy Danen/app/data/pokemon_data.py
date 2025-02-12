"""Module for loading and processing Pokemon data."""
import pandas as pd
import os

def load_pokemon_data():
    """Load Pokemon data from CSV file."""
    # Get the absolute path to the data file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'pokemon.csv')
    
    # Load the data
    df = pd.read_csv(data_path)
    return df

# Load the data once when the module is imported
pokemon_df = load_pokemon_data() 