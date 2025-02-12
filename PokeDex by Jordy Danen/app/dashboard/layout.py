"""Dashboard layout module."""
from dash import html, dcc
from app.utils.constants import POKEMON_COLORS
from app.utils.helpers import get_pokemon_image_url
from app.components.pokemon_grid import create_pokemon_grid
from app.data.pokemon_data import pokemon_df

def create_layout(app=None):
    """Create the main dashboard layout."""
    return html.Div([
        # Pokedex outer shell
        html.Div([
            # Pokedex top section with lights
            html.Div([
                # Modified blue circle to be clickable
                html.Button(
                    className='pokedex-light-big',
                    id='home-button',
                    n_clicks=0,
                    style={'cursor': 'pointer', 'border': 'none', 'padding': '0'}
                ),
                html.Div([
                    html.Div(className='pokedex-light-small red'),
                    html.Div(className='pokedex-light-small yellow'),
                    html.Div(className='pokedex-light-small green'),
                ], className='pokedex-lights-small')
            ], className='pokedex-top'),

            # Pokedex screen area
            html.Div([
                html.H1("Pokédex",
                       style={'textAlign': 'center', 
                              'color': POKEMON_COLORS['pokeball_white'],
                              'fontFamily': POKEMON_COLORS['pixel_font'],
                              'fontSize': '24px',
                              'margin': '0',
                              'padding': '10px'}),
                
                dcc.Tabs(id='tabs',
                        children=[
                    # Pokedex Entry Tab
                    dcc.Tab(label='Pokédex Entry',
                            style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                   'fontSize': '12px',
                                   'padding': '12px'},
                            selected_style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                           'fontSize': '12px',
                                           'padding': '12px',
                                           'backgroundColor': POKEMON_COLORS['pokeball_red'],
                                           'color': POKEMON_COLORS['pokeball_white']},
                            children=[
                                html.Div(id='pokemon-display', children=create_pokemon_grid(pokemon_df), style={'width': '100%'})
                            ]),
                    
                    # Type Analysis Tab
                    dcc.Tab(label='Type Analysis',
                            style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                   'fontSize': '12px',
                                   'padding': '12px'},
                            selected_style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                          'fontSize': '12px',
                                          'padding': '12px',
                                          'backgroundColor': POKEMON_COLORS['pokeball_red'],
                                          'color': POKEMON_COLORS['pokeball_white']},
                            children=[
                                html.Div([
                                    html.H3("Toggle Generations",
                                           style={'color': POKEMON_COLORS['pokeball_white'],
                                                 'fontFamily': POKEMON_COLORS['pixel_font'],
                                                 'fontSize': '14px',
                                                 'marginBottom': '15px'}),
                                    html.Div([
                                        html.Div([
                                            html.Button(
                                                f'Gen {i}',
                                                id=f'gen-button-{i}',
                                                n_clicks=0,
                                                className='gen-button active'
                                            ) for i in sorted(pokemon_df['generation'].unique())
                                        ], style={'display': 'flex', 'gap': '10px', 'flexWrap': 'wrap'})
                                    ], id='generation-buttons'),
                                    # Hidden div to store active generations
                                    html.Div(id='active-generations', style={'display': 'none'})
                                ], style={'marginBottom': '20px'}),
                                
                                # Type distribution plots
                                html.Div([
                                    dcc.Graph(id='primary-type-dist')
                                ]),
                                html.Div([
                                    dcc.Graph(id='type-heatmap')
                                ])
                            ]),
                    
                    # Stats Analysis Tab
                    dcc.Tab(label='Stats Analysis',
                            style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                   'fontSize': '12px',
                                   'padding': '12px'},
                            selected_style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                          'fontSize': '12px',
                                          'padding': '12px',
                                          'backgroundColor': POKEMON_COLORS['pokeball_red'],
                                          'color': POKEMON_COLORS['pokeball_white']},
                            children=[
                                html.Div([
                                    # Pokemon comparison selector with images
                                    html.Div([
                                        html.H3("Pokédex Search",
                                               style={'color': 'white',
                                                     'backgroundColor': POKEMON_COLORS['pokeball_red'],
                                                     'padding': '10px 15px',
                                                     'borderRadius': '8px 8px 0 0',
                                                     'margin': '0',
                                                     'fontFamily': POKEMON_COLORS['pixel_font'],
                                                     'fontSize': '14px'}),
                                        dcc.Dropdown(
                                            id='pokemon-compare',
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
                                            multi=True,
                                            placeholder="Select Pokémon to Compare",
                                            style={'fontFamily': POKEMON_COLORS['pixel_font']}
                                        )
                                    ], style={'width': '100%', 
                                             'backgroundColor': POKEMON_COLORS['pokeball_white'],
                                             'borderRadius': '10px',
                                             'marginBottom': '20px',
                                             'boxShadow': POKEMON_COLORS['card_shadow']}),
                                    
                                    # Stats visualizations
                                    html.Div([
                                        dcc.Graph(id='stats-comparison')
                                    ]),
                                    html.Div([
                                        dcc.Graph(id='stats-distribution')
                                    ])
                                ])
                            ]),
                            
                    # Battle Simulator Tab
                    dcc.Tab(label='Battle Simulator',
                            style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                   'fontSize': '12px',
                                   'padding': '12px'},
                            selected_style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                          'fontSize': '12px',
                                          'padding': '12px',
                                          'backgroundColor': POKEMON_COLORS['pokeball_red'],
                                          'color': POKEMON_COLORS['pokeball_white']},
                            children=[
                                html.Div([
                                    # Pokemon Selection Section
                                    html.Div([
                                        # Pokemon 1 Selection
                                        html.Div([
                                            html.H3("Select First Pokémon",
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
                                                placeholder="Select First Pokémon",
                                                style={'fontFamily': POKEMON_COLORS['pixel_font']}
                                            )
                                        ], style={'width': '45%', 
                                                 'backgroundColor': POKEMON_COLORS['pokeball_white'],
                                                 'borderRadius': '10px',
                                                 'boxShadow': POKEMON_COLORS['card_shadow']}),
                                        
                                        # VS Text
                                        html.Div("VS",
                                                style={'width': '10%',
                                                       'textAlign': 'center',
                                                       'fontFamily': POKEMON_COLORS['pixel_font'],
                                                       'fontSize': '24px',
                                                       'color': POKEMON_COLORS['pokeball_red']}),
                                        
                                        # Pokemon 2 Selection
                                        html.Div([
                                            html.H3("Select Second Pokémon",
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
                                                placeholder="Select Second Pokémon",
                                                style={'fontFamily': POKEMON_COLORS['pixel_font']}
                                            )
                                        ], style={'width': '45%', 
                                                 'backgroundColor': POKEMON_COLORS['pokeball_white'],
                                                 'borderRadius': '10px',
                                                 'boxShadow': POKEMON_COLORS['card_shadow']})
                                    ], style={'display': 'flex',
                                             'justifyContent': 'space-between',
                                             'alignItems': 'center',
                                             'marginBottom': '20px'}),
                                    
                                    # Battle Display Section
                                    html.Div([
                                        # Pokemon 1 Display
                                        html.Div([
                                            html.Img(id='pokemon1-image',
                                                    style={'width': '200px',
                                                           'height': '200px',
                                                           'imageRendering': 'pixelated'}),
                                            html.Div(id='pokemon1-stats',
                                                    style={'backgroundColor': POKEMON_COLORS['pokeball_white'],
                                                           'padding': '10px',
                                                           'borderRadius': '8px',
                                                           'marginTop': '10px',
                                                           'boxShadow': POKEMON_COLORS['card_shadow']})
                                        ], style={'width': '45%', 'textAlign': 'center'}),
                                        
                                        # Battle Controls
                                        html.Div([
                                            html.Div(id='battle-prediction',
                                                    style={'fontFamily': POKEMON_COLORS['pixel_font'],
                                                           'fontSize': '14px',
                                                           'textAlign': 'center',
                                                           'marginBottom': '20px',
                                                           'color': POKEMON_COLORS['pokeball_white'],
                                                           'whiteSpace': 'pre-wrap'}),
                                            html.Button("Simulate Battle",
                                                      id='simulate-battle-btn',
                                                      className='gen-button active',
                                                      style={'width': '100%',
                                                             'padding': '15px 30px',
                                                             'fontSize': '14px'})
                                        ], style={'width': '20%',
                                                 'display': 'flex',
                                                 'flexDirection': 'column',
                                                 'justifyContent': 'center',
                                                 'padding': '0 10px'}),
                                        
                                        # Pokemon 2 Display
                                        html.Div([
                                            html.Img(id='pokemon2-image',
                                                    style={'width': '200px',
                                                           'height': '200px',
                                                           'imageRendering': 'pixelated'}),
                                            html.Div(id='pokemon2-stats',
                                                    style={'backgroundColor': POKEMON_COLORS['pokeball_white'],
                                                           'padding': '10px',
                                                           'borderRadius': '8px',
                                                           'marginTop': '10px',
                                                           'boxShadow': POKEMON_COLORS['card_shadow']})
                                        ], style={'width': '40%', 'textAlign': 'center'})
                                    ], style={'display': 'flex',
                                             'justifyContent': 'space-between',
                                             'alignItems': 'flex-start',
                                             'marginBottom': '20px'}),
                                    
                                    # Battle Log Section
                                    html.Div([
                                        html.H3("Battle Log",
                                               style={'color': POKEMON_COLORS['pokeball_white'],
                                                     'fontFamily': POKEMON_COLORS['pixel_font'],
                                                     'fontSize': '14px',
                                                     'marginBottom': '10px'}),
                                        html.Pre(id='battle-log',
                                                style={'whiteSpace': 'pre-wrap',
                                                       'backgroundColor': POKEMON_COLORS['pokeball_white'],
                                                       'padding': '15px',
                                                       'borderRadius': '8px',
                                                       'maxHeight': '200px',
                                                       'overflowY': 'auto',
                                                       'fontFamily': POKEMON_COLORS['regular_font'],
                                                       'fontSize': '14px',
                                                       'boxShadow': POKEMON_COLORS['card_shadow']})
                                    ])
                                ], style={'padding': '20px'})
                            ])
                ], style={'backgroundColor': '#c0392b',
                         'border': 'none',
                         'padding': '10px'})
            ], className='pokedex-screen')
        ], className='pokedex-body')
    ], className='pokedex-container') 