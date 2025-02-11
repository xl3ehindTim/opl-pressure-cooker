import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
import pandas as pd
import kagglehub
import ast
import pickle
import warnings

warnings.filterwarnings('ignore')

def preprocess_data(df):
    # Create a copy of the dataframe
    df_processed = df.copy()
    
    # Convert abilities from string representation of list to actual list
    df_processed['abilities'] = df_processed['abilities'].apply(ast.literal_eval)
    
    # Create separate rows for each ability
    df_exploded = df_processed.explode('abilities')
    
    # Handle missing values - important: add 'none' to types list
    df_exploded['type2'].fillna('none', inplace=True)
    df_exploded['weight_kg'].fillna(df_exploded['weight_kg'].mean(), inplace=True)
    df_exploded['height_m'].fillna(df_exploded['height_m'].mean(), inplace=True)
    
    # Get unique values first, ensuring 'none' is included in types
    unique_types = sorted(set(df_exploded['type1'].unique()) | set(df_exploded['type2'].unique()) | {'none'})
    unique_abilities = sorted(df_exploded['abilities'].unique())
    
    # Create label encoders
    le_type = LabelEncoder().fit(unique_types)
    le_ability = LabelEncoder().fit(unique_abilities)
    
    # Encode values
    df_exploded['type1_encoded'] = le_type.transform(df_exploded['type1'])
    df_exploded['type2_encoded'] = le_type.transform(df_exploded['type2'])
    df_exploded['ability_encoded'] = le_ability.transform(df_exploded['abilities'])
    
    return df_exploded, len(unique_types), len(unique_abilities)

class PokemonTypeTransformer(nn.Module):
    def __init__(self, n_types, n_abilities, d_model=32, nhead=4, num_layers=2):
        super().__init__()
        
        # Embeddings
        self.type_embedding = nn.Embedding(n_types, d_model)
        self.ability_embedding = nn.Embedding(n_abilities, d_model)
        
        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=128,
            dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output projection
        self.output_projection = nn.Linear(d_model * 6, d_model)  # 6 = 2*type1 + 2*type2 + 2*ability
        
    def forward(self, type_ids, ability_ids):
        # Get embeddings
        type_emb = self.type_embedding(type_ids)  # Shape: [batch, 2, d_model]
        ability_emb = self.ability_embedding(ability_ids)  # Shape: [batch, 2, d_model]
        
        # Flatten embeddings
        batch_size = type_emb.size(0)
        type_emb_flat = type_emb.reshape(batch_size, -1)  # Shape: [batch, 2*d_model]
        ability_emb_flat = ability_emb.reshape(batch_size, -1)  # Shape: [batch, 2*d_model]

        # Concatenate all embeddings
        x = torch.cat([type_emb_flat, ability_emb_flat], dim=1)  # Shape: [batch, 4*d_model]

        # Project to desired output size
        x = self.output_projection(x)  # Shape: [batch, d_model]
        
        return x

class PokemonCounterPredictor(nn.Module):
    def __init__(self, type_transformer, input_size):
        super().__init__()
        
        self.type_transformer = type_transformer
        
        # Calculate input size for the predictor
        transformer_output_size = 32  # d_model from transformer
        stats_size = 48  # number of stat features (24 * 2 for both Pokemon)
        total_input_size = transformer_output_size + stats_size
        
        # Neural network for counter prediction
        self.predictor = nn.Sequential(
            nn.Linear(total_input_size, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
    def forward(self, type1_ids, type2_ids, ability_ids, stats):
        pokemon_emb = self.type_transformer(
            torch.cat([type1_ids, type2_ids], dim=1),  # Shape: [batch, 4]
            ability_ids  # Shape: [batch, 2]
        )
        
        # Combine with stats
        x = torch.cat([pokemon_emb, stats], dim=1)
        
        # Predict
        return self.predictor(x)

def calculate_effectiveness(attacker, defender):
    # Map type names to their corresponding column names
    type_map = {
        'fighting': 'fight'  # Add any other mappings if needed
    }
    
    # Calculate type effectiveness for type1
    type1_col = 'against_' + (type_map.get(attacker['type1'].lower(), attacker['type1'].lower()))
    type_effectiveness = defender[type1_col]
    
    # Calculate type effectiveness for type2 if it exists
    if attacker['type2'] != 'none':
        type2_col = 'against_' + (type_map.get(attacker['type2'].lower(), attacker['type2'].lower()))
        type_effectiveness *= defender[type2_col]
    
    # Calculate stat-based effectiveness
    stat_effectiveness = (
        attacker['attack'] + attacker['sp_attack'] + attacker['speed']
    ) / (
        defender['defense'] + defender['sp_defense'] + defender['hp']
    )
    
    return type_effectiveness * stat_effectiveness

class PokemonDataset(Dataset):
    def __init__(self, df_processed):
        self.data = df_processed
        self.scaler = StandardScaler()
        
        numerical_cols = ['attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'hp',
                         'against_bug', 'against_dark', 'against_dragon', 'against_electric',
                         'against_fairy', 'against_fight', 'against_fire', 'against_flying',
                         'against_ghost', 'against_grass', 'against_ground', 'against_ice',
                         'against_normal', 'against_poison', 'against_psychic', 'against_rock',
                         'against_steel', 'against_water']
        
        self.stats = self.scaler.fit_transform(self.data[numerical_cols])
        
    def __len__(self):
        return len(self.data) * 5
        
    def __getitem__(self, idx):
        idx1 = idx % len(self.data)
        idx2 = np.random.randint(0, len(self.data))
        
        pokemon1 = self.data.iloc[idx1]
        pokemon2 = self.data.iloc[idx2]
        
        # Calculate effectiveness
        effectiveness1 = calculate_effectiveness(pokemon1, pokemon2)
        effectiveness2 = calculate_effectiveness(pokemon2, pokemon1)
        
        # Prepare inputs with correct shapes
        type1_ids = torch.tensor([pokemon1['type1_encoded'], pokemon2['type1_encoded']])
        type2_ids = torch.tensor([pokemon1['type2_encoded'], pokemon2['type2_encoded']])
        ability_ids = torch.tensor([pokemon1['ability_encoded'], pokemon2['ability_encoded']])
        
        stats = torch.FloatTensor(np.concatenate([
            self.stats[idx1],
            self.stats[idx2]
        ]))
        
        target = torch.FloatTensor([1.0 if effectiveness1 > effectiveness2 else 0.0])
        
        return type1_ids, type2_ids, ability_ids, stats, target

def train_model(model, train_loader, num_epochs=10, learning_rate=0.001):
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for type1_ids, type2_ids, ability_ids, stats, targets in train_loader:
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(type1_ids, type2_ids, ability_ids, stats)
            loss = criterion(outputs, targets)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # Calculate accuracy
            predictions = (outputs >= 0.5).float()
            correct += (predictions == targets).sum().item()
            total += targets.size(0)
        
        epoch_loss = total_loss / len(train_loader)
        epoch_acc = correct / total
        
        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.4f}')

def save_model_and_preprocessors(model, dataset, df_processed):
    # Save model weights
    torch.save(model.state_dict(), 'battle_predictor.pth')
    
    # Get all unique types including 'none'
    all_types = sorted(set(df_processed['type1'].unique()) | 
                      set(df_processed['type2'].unique()) |
                      {'none'})
    
    # Save preprocessors
    with open('battle_predictor_preprocessors.pkl', 'wb') as f:
        pickle.dump({
            'scaler': dataset.scaler,
            'type_encoder': LabelEncoder().fit(all_types),
            'ability_encoder': LabelEncoder().fit(df_processed['abilities'].unique())
        }, f)

def main():
    # Load and preprocess data
    path = kagglehub.dataset_download("rounakbanik/pokemon")
    df = pd.read_csv(path + "/pokemon.csv")
    
    # Drop unnecessary columns
    df.drop(columns=['japanese_name', 'capture_rate', 'generation', 
                    'percentage_male', 'pokedex_number', 'base_egg_steps'], 
            inplace=True)
    
    # Preprocess data
    df_processed, n_types, n_abilities = preprocess_data(df)
    
    # Create dataset
    dataset = PokemonDataset(df_processed)
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Initialize models
    type_transformer = PokemonTypeTransformer(n_types=n_types, n_abilities=n_abilities)
    model = PokemonCounterPredictor(type_transformer, input_size=32+48)
    
    # Train model
    train_model(model, train_loader, num_epochs=15)
    
    # Save model and preprocessors
    save_model_and_preprocessors(model, dataset, df_processed)

if __name__ == "__main__":
    main()
