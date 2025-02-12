"""Helper functions used throughout the application."""
import pandas as pd
from app.utils.constants import TYPE_EFFECTIVENESS, TYPE_MOVES

def get_pokemon_image_url(pokemon_number):
    """Get Pokemon image URL from PokeAPI."""
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_number}.png"

def get_counter_pokemon(df, target_type1, target_type2=None):
    """Find Pokemon that are effective against the given types."""
    counter_scores = {}
    
    # Calculate effectiveness score for each Pokemon
    for _, pokemon in df.iterrows():
        attacker_type1 = pokemon['type1'] if 'type1' in df.columns else pokemon['Type 1']
        attacker_type2 = pokemon['type2'] if 'type2' in df.columns else pokemon['Type 2']
        
        # Calculate damage multiplier from this Pokemon's types
        score = 0
        
        # Check type1 effectiveness
        if attacker_type1.lower() in TYPE_EFFECTIVENESS:
            if target_type1.lower() in TYPE_EFFECTIVENESS[attacker_type1.lower()]:
                score += TYPE_EFFECTIVENESS[attacker_type1.lower()][target_type1.lower()]
            if pd.notna(target_type2) and target_type2.lower() in TYPE_EFFECTIVENESS[attacker_type1.lower()]:
                score += TYPE_EFFECTIVENESS[attacker_type1.lower()][target_type2.lower()]
        
        # Check type2 effectiveness if it exists
        if pd.notna(attacker_type2) and attacker_type2.lower() in TYPE_EFFECTIVENESS:
            if target_type1.lower() in TYPE_EFFECTIVENESS[attacker_type2.lower()]:
                score += TYPE_EFFECTIVENESS[attacker_type2.lower()][target_type1.lower()]
            if pd.notna(target_type2) and target_type2.lower() in TYPE_EFFECTIVENESS[attacker_type2.lower()]:
                score += TYPE_EFFECTIVENESS[attacker_type2.lower()][target_type2.lower()]
        
        counter_scores[pokemon['name']] = score
    
    # Sort by effectiveness score and return top 5
    sorted_counters = sorted(counter_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_counters[:5]

def get_evolution_chain(df, pokemon_name):
    """Get the evolution chain for a given Pokemon."""
    # Get the evolution chain number for the selected Pokemon
    pokemon = df[df['name'] == pokemon_name].iloc[0]
    
    # Create lists for previous and next evolutions
    prev_evolutions = []
    next_evolutions = []
    
    try:
        # Check which evolution-related columns are available
        if 'family_id' in df.columns:
            chain_id = pokemon['family_id']
            chain_pokemon = df[df['family_id'] == chain_id]
        elif 'evolution_chain' in df.columns:
            chain_id = pokemon['evolution_chain']
            chain_pokemon = df[df['evolution_chain'] == chain_id]
        else:
            return [], []
        
        # Sort by pokedex number to get evolution order
        chain_pokemon = chain_pokemon.sort_values('pokedex_number')
        current_index = chain_pokemon[chain_pokemon['name'] == pokemon_name].index[0]
        
        # Get previous evolutions
        prev_evolutions = chain_pokemon[chain_pokemon.index < current_index]['name'].tolist()
        
        # Get next evolutions
        next_evolutions = chain_pokemon[chain_pokemon.index > current_index]['name'].tolist()
            
    except Exception as e:
        print(f"Error in get_evolution_chain: {str(e)}")
        pass
    
    return prev_evolutions, next_evolutions

def get_recommended_moves(df, pokemon_name):
    """Get recommended moves for a Pokemon based on its type(s)."""
    pokemon = df[df['name'] == pokemon_name].iloc[0]
    type1 = pokemon['type1'].lower() if 'type1' in df.columns else pokemon['Type 1'].lower()
    type2 = pokemon['type2'] if 'type2' in df.columns else pokemon['Type 2']
    
    recommended_moves = []
    
    # Add STAB moves from primary type
    if type1 in TYPE_MOVES:
        recommended_moves.extend([{
            'move_name': move,
            'move_type': type1,
            'coverage_score': 2.0  # STAB bonus
        } for move in TYPE_MOVES[type1][:2]])  # Get 2 moves from primary type
    
    # Add STAB moves from secondary type if it exists
    if pd.notna(type2) and type2.lower() in TYPE_MOVES:
        recommended_moves.extend([{
            'move_name': move,
            'move_type': type2.lower(),
            'coverage_score': 2.0  # STAB bonus
        } for move in TYPE_MOVES[type2.lower()][:1]])  # Get 1 move from secondary type
    
    # Add coverage moves
    coverage_types = []
    for attack_type, effectiveness in TYPE_EFFECTIVENESS.items():
        score = 0
        # Check effectiveness against common defensive types
        for def_type in ['steel', 'rock', 'fairy', 'dragon']:
            if def_type in effectiveness and effectiveness[def_type] > 1:
                score += 1
        if score > 0 and attack_type not in [type1, type2] and attack_type in TYPE_MOVES:
            coverage_types.append((attack_type, score))
    
    # Sort coverage types by effectiveness and add best coverage move
    coverage_types.sort(key=lambda x: x[1], reverse=True)
    for coverage_type, score in coverage_types[:1]:  # Get 1 coverage move
        recommended_moves.append({
            'move_name': TYPE_MOVES[coverage_type][0],
            'move_type': coverage_type,
            'coverage_score': score
        })
    
    # If we still need more moves, add from primary type
    while len(recommended_moves) < 4:
        if type1 in TYPE_MOVES and len(TYPE_MOVES[type1]) > len(recommended_moves):
            recommended_moves.append({
                'move_name': TYPE_MOVES[type1][len(recommended_moves)],
                'move_type': type1,
                'coverage_score': 1.5
            })
        else:
            break
    
    return recommended_moves[:4] 