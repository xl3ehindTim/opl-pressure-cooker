"""Battle tab callbacks module."""
from dash import Input, Output, State, callback_context, html, dcc, no_update
import plotly.graph_objects as go
from app.utils.helpers import get_pokemon_image_url
from app.data.pokemon_data import pokemon_df
from app.battle.simulator import BattleSimulator
from app.battle.predictor import BattlePredictor

# Initialize battle simulator and predictor
battle_simulator = BattleSimulator(pokemon_df)
battle_predictor = BattlePredictor(pokemon_df)

def register_callbacks(app):
    """Register all callbacks for the battle tab."""
    
    @app.callback(
        [Output('pokemon1-image', 'src'),
         Output('pokemon2-image', 'src'),
         Output('pokemon1-stats', 'children'),
         Output('pokemon2-stats', 'children'),
         Output('battle-prediction', 'children'),
         Output('battle-log', 'children')],
        [Input('pokemon1-select', 'value'),
         Input('pokemon2-select', 'value'),
         Input('simulate-battle-btn', 'n_clicks')],
        [State('battle-log', 'children')],
        prevent_initial_call=True
    )
    def update_battle_display(pokemon1_name, pokemon2_name, n_clicks, current_log):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'] if ctx.triggered else None
        
        # Initialize outputs
        pokemon1_image = ''
        pokemon2_image = ''
        pokemon1_stats = ''
        pokemon2_stats = ''
        prediction_text = ''
        battle_log = current_log or ''
        
        # If no Pokemon selected, return empty values
        if not pokemon1_name and not pokemon2_name:
            return pokemon1_image, pokemon2_image, pokemon1_stats, pokemon2_stats, prediction_text, battle_log
        
        # Update Pokemon 1 display if selected
        if pokemon1_name:
            pokemon1 = pokemon_df[pokemon_df['name'] == pokemon1_name].iloc[0]
            pokemon1_image = get_pokemon_image_url(pokemon1['pokedex_number'])
            pokemon1_stats = create_stats_display(pokemon1)
        
        # Update Pokemon 2 display if selected
        if pokemon2_name:
            pokemon2 = pokemon_df[pokemon_df['name'] == pokemon2_name].iloc[0]
            pokemon2_image = get_pokemon_image_url(pokemon2['pokedex_number'])
            pokemon2_stats = create_stats_display(pokemon2)
        
        # Update prediction only if both Pokemon are selected
        if pokemon1_name and pokemon2_name:
            win_probability = battle_predictor.predict_battle(pokemon1_name, pokemon2_name)
            prediction_text = f"{pokemon1_name} has a {win_probability*100:.1f}% chance of winning"
            
            # If battle button was clicked, simulate battle
            if triggered_id == 'simulate-battle-btn.n_clicks' and n_clicks:
                battle_log = '\n'.join(battle_simulator.simulate_battle(pokemon1_name, pokemon2_name))
        
        return pokemon1_image, pokemon2_image, pokemon1_stats, pokemon2_stats, prediction_text, battle_log

def create_stats_display(pokemon):
    """Create a stats display for a Pokemon."""
    stats = [
        ('HP', pokemon['hp']),
        ('Attack', pokemon['attack']),
        ('Defense', pokemon['defense']),
        ('Sp. Attack', pokemon['sp_attack']),
        ('Sp. Defense', pokemon['sp_defense']),
        ('Speed', pokemon['speed'])
    ]
    
    return html.Div([
        html.H4(f"{pokemon['name']}",
               style={'textAlign': 'center',
                      'marginBottom': '10px'}),
        html.Div([
            html.Div([
                html.Span(f"{stat}: ",
                         style={'fontWeight': 'bold'}),
                html.Span(str(value))
            ]) for stat, value in stats
        ])
    ]) 