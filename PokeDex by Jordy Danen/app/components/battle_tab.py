"""Battle tab component module."""
from dash import html, dcc
import plotly.graph_objects as go
from app.utils.constants import POKEMON_COLORS, TYPE_COLORS
from app.utils.helpers import get_pokemon_image_url
from app.data.pokemon_data import pokemon_df
from app.battle.simulator import BattleSimulator
from app.battle.predictor import BattlePredictor

def create_battle_tab():
    """Create the battle tab component."""
    return html.Div([
        # Pokemon Selection Section
        html.Div([
            html.Div([
                html.H3("Select Pokemon 1",
                       style={'color': 'white',
                             'backgroundColor': POKEMON_COLORS['pokeball_red'],
                             'padding': '10px 15px',
                             'borderRadius': '8px 8px 0 0',
                             'margin': '0',
                             'fontFamily': POKEMON_COLORS['pixel_font'],
                             'fontSize': '14px'}),
                dcc.Dropdown(
                    id='pokemon1-select',
                    options=[{
                        'label': html.Div([
                            html.Img(
                                src=get_pokemon_image_url(row['pokedex_number']),
                                style={'height': '30px', 'width': '30px', 'marginRight': '10px', 'verticalAlign': 'middle'}
                            ),
                            f"#{row['pokedex_number']} {row['name']}"
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                        'value': row['name']
                    } for _, row in pokemon_df.sort_values('pokedex_number').iterrows()],
                    placeholder="Select First Pokemon",
                    style={'fontFamily': POKEMON_COLORS['pixel_font']}
                )
            ], style={'width': '45%', 
                     'backgroundColor': POKEMON_COLORS['pokeball_white'],
                     'borderRadius': '10px',
                     'marginBottom': '20px',
                     'boxShadow': POKEMON_COLORS['card_shadow']}),

            html.Div("VS", style={
                'width': '10%',
                'textAlign': 'center',
                'fontFamily': POKEMON_COLORS['pixel_font'],
                'fontSize': '24px',
                'color': POKEMON_COLORS['pokeball_red']
            }),

            html.Div([
                html.H3("Select Pokemon 2",
                       style={'color': 'white',
                             'backgroundColor': POKEMON_COLORS['pokeball_red'],
                             'padding': '10px 15px',
                             'borderRadius': '8px 8px 0 0',
                             'margin': '0',
                             'fontFamily': POKEMON_COLORS['pixel_font'],
                             'fontSize': '14px'}),
                dcc.Dropdown(
                    id='pokemon2-select',
                    options=[{
                        'label': html.Div([
                            html.Img(
                                src=get_pokemon_image_url(row['pokedex_number']),
                                style={'height': '30px', 'width': '30px', 'marginRight': '10px', 'verticalAlign': 'middle'}
                            ),
                            f"#{row['pokedex_number']} {row['name']}"
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                        'value': row['name']
                    } for _, row in pokemon_df.sort_values('pokedex_number').iterrows()],
                    placeholder="Select Second Pokemon",
                    style={'fontFamily': POKEMON_COLORS['pixel_font']}
                )
            ], style={'width': '45%', 
                     'backgroundColor': POKEMON_COLORS['pokeball_white'],
                     'borderRadius': '10px',
                     'marginBottom': '20px',
                     'boxShadow': POKEMON_COLORS['card_shadow']})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),

        # Battle Display Section
        html.Div([
            # Pokemon 1 Display
            html.Div([
                html.Img(id='pokemon1-image',
                        style={'width': '200px',
                               'height': '200px',
                               'imageRendering': 'pixelated'}),
                html.Div(id='pokemon1-stats')
            ], style={'width': '45%'}),

            # Battle Prediction
            html.Div([
                html.Div(id='battle-prediction',
                        style={'fontFamily': POKEMON_COLORS['pixel_font'],
                               'fontSize': '18px',
                               'textAlign': 'center',
                               'marginBottom': '20px'}),
                html.Button("Simulate Battle",
                          id='simulate-battle-btn',
                          style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                 'fontSize': '14px',
                                 'padding': '10px 20px',
                                 'backgroundColor': POKEMON_COLORS['pokeball_red'],
                                 'color': 'white',
                                 'border': 'none',
                                 'borderRadius': '5px',
                                 'cursor': 'pointer'})
            ], style={'width': '10%',
                     'display': 'flex',
                     'flexDirection': 'column',
                     'alignItems': 'center',
                     'justifyContent': 'center'}),

            # Pokemon 2 Display
            html.Div([
                html.Img(id='pokemon2-image',
                        style={'width': '200px',
                               'height': '200px',
                               'imageRendering': 'pixelated'}),
                html.Div(id='pokemon2-stats')
            ], style={'width': '45%'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),

        # Battle Log Section
        html.Div([
            html.H3("Battle Log",
                   style={'color': POKEMON_COLORS['pokeball_red'],
                          'fontFamily': POKEMON_COLORS['pixel_font'],
                          'marginBottom': '10px'}),
            html.Div(id='battle-log',
                    style={'height': '200px',
                           'overflowY': 'auto',
                           'padding': '10px',
                           'backgroundColor': '#f5f5f5',
                           'borderRadius': '5px',
                           'fontFamily': POKEMON_COLORS['regular_font']})
        ])
    ]) 