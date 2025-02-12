"""Pokemon information display component."""
from dash import html
import pandas as pd
from app.utils.helpers import get_pokemon_image_url, get_recommended_moves
from app.utils.constants import POKEMON_COLORS, TYPE_COLORS

def create_pokemon_info(pokemon):
    """Create the Pokemon information display."""
    type1 = pokemon['type1'] if 'type1' in pokemon.index else pokemon['Type 1']
    type2 = pokemon['type2'] if 'type2' in pokemon.index else pokemon['Type 2']
    
    return html.Div([
        html.Div([
            # Add Pokemon image at the top
            html.Div([
                html.Img(
                    src=get_pokemon_image_url(pokemon['pokedex_number']),
                    style={
                        'height': '150px',
                        'width': '150px',
                        'display': 'block',
                        'margin': '20px auto',
                        'imageRendering': 'pixelated'
                    }
                )
            ], style={
                'backgroundColor': '#f0f0f0',
                'borderRadius': '10px',
                'padding': '10px',
                'marginBottom': '15px'
            }),
            
            # Pokemon number and name
            html.Div([
                html.H4(f"#{pokemon['pokedex_number']} {pokemon['name']}", 
                        style={'margin': '0',
                               'color': 'white',
                               'fontSize': '16px',
                               'fontFamily': POKEMON_COLORS['pixel_font'],
                               'backgroundColor': POKEMON_COLORS['pokeball_red'],
                               'padding': '10px 15px',
                               'borderRadius': '8px 8px 0 0'})
            ]),
            
            # Pokemon info including types and stats
            html.Div([
                # Types
                html.Div([
                    html.Span(f"Type 1: {type1}", 
                             style={'backgroundColor': TYPE_COLORS[type1.lower()],
                                   'color': 'white',
                                   'padding': '5px 10px',
                                   'borderRadius': '20px',
                                   'marginRight': '10px',
                                   'fontSize': '14px'}),
                    html.Span(f"Type 2: {type2}" if pd.notna(type2) else "Type 2: None",
                             style={'backgroundColor': TYPE_COLORS[type2.lower()] if pd.notna(type2) else '#A8A878',
                                   'color': 'white',
                                   'padding': '5px 10px',
                                   'borderRadius': '20px',
                                   'fontSize': '14px'})
                ], style={'marginBottom': '15px', 'marginTop': '15px'}),
                
                # Base Stats
                html.Div([
                    html.H5("Base Stats",
                           style={'color': POKEMON_COLORS['pokeball_red'],
                                  'fontFamily': POKEMON_COLORS['pixel_font'],
                                  'marginBottom': '10px',
                                  'fontSize': '14px'}),
                    html.Div([
                        html.Div([
                            html.Span(stat.upper(),
                                    style={'width': '100px', 
                                          'display': 'inline-block',
                                          'fontFamily': POKEMON_COLORS['pixel_font'],
                                          'fontSize': '12px'}),
                            html.Div(
                                style={'display': 'inline-block',
                                      'width': f'{(pokemon[stat]/255)*100}%',
                                      'height': '12px',
                                      'backgroundColor': POKEMON_COLORS['pokeball_red'],
                                      'borderRadius': '10px',
                                      'marginLeft': '10px'}),
                            html.Span(str(pokemon[stat]),
                                    style={'marginLeft': '10px',
                                          'fontFamily': POKEMON_COLORS['pixel_font'],
                                          'fontSize': '12px'})
                        ], style={'margin': '5px 0'})
                        for stat in ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
                    ])
                ], style={'backgroundColor': '#e8e8e8',
                         'padding': '10px 15px',
                         'borderRadius': '5px'}),
                
                # Battle Button
                html.Div([
                    html.Button(
                        "Battle This Pokémon",
                        id={'type': 'battle-button', 'pokemon': pokemon['name']},
                        className='gen-button active',
                        style={
                            'width': '100%',
                            'marginTop': '15px',
                            'padding': '15px',
                            'fontSize': '14px',
                            'fontFamily': POKEMON_COLORS['pixel_font']
                        }
                    )
                ])
            ], style={'padding': '15px',
                      'backgroundColor': '#f8f8f8'})
        ], style={'border': f'2px solid {POKEMON_COLORS["pokeball_red"]}',
                  'borderRadius': '10px',
                  'overflow': 'hidden'})
    ])

def create_moves_display(df, pokemon):
    """Create the moves display."""
    moves = get_recommended_moves(df, pokemon['name'])
    return html.Div([
        html.Div([
            html.H4("Recommended Moves",
                    style={'color': POKEMON_COLORS['pokedex_blue'],
                           'marginBottom': '15px',
                           'borderBottom': f'3px solid {POKEMON_COLORS["pokemon_yellow"]}',
                           'paddingBottom': '10px',
                           'fontFamily': POKEMON_COLORS['pixel_font']}),
            html.Div([
                html.Div([
                    html.Strong(f"{move['move_name']} ",
                              style={'color': 'white'}),
                    html.Span(f"({move['move_type'].title()})",
                             style={'color': 'white'}),
                    html.Div(f"Coverage: {move['coverage_score']:.1f}",
                            style={'fontSize': '14px',
                                   'color': 'white'})
                ], style={'backgroundColor': TYPE_COLORS[move['move_type'].lower()],
                         'padding': '12px',
                         'margin': '8px 0',
                         'borderRadius': '8px',
                         'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
                for move in moves
            ])
        ])
    ]) 