"""Battle tab layout module."""
from dash import html, dcc
from app.data.pokemon_data import pokemon_df

def create_layout():
    """Create the layout for the battle tab."""
    return html.Div([
        # Pokemon Selection Row
        html.Div([
            # Pokemon 1 Selection
            html.Div([
                html.Label('Select Pokemon 1:'),
                dcc.Dropdown(
                    id='pokemon1-select',
                    options=[{'label': name, 'value': name} 
                            for name in sorted(pokemon_df['name'].unique())],
                    placeholder='Select a Pokemon'
                )
            ], style={'width': '45%', 'display': 'inline-block'}),
            
            # VS Text
            html.Div([
                html.H2('VS', style={'textAlign': 'center'})
            ], style={'width': '10%', 'display': 'inline-block'}),
            
            # Pokemon 2 Selection
            html.Div([
                html.Label('Select Pokemon 2:'),
                dcc.Dropdown(
                    id='pokemon2-select',
                    options=[{'label': name, 'value': name}
                            for name in sorted(pokemon_df['name'].unique())],
                    placeholder='Select a Pokemon'
                )
            ], style={'width': '45%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px'}),
        
        # Battle Display Row
        html.Div([
            # Pokemon 1 Display
            html.Div([
                html.Img(id='pokemon1-image',
                        style={'maxWidth': '200px',
                               'maxHeight': '200px'}),
                html.Div(id='pokemon1-stats')
            ], style={'width': '45%', 'display': 'inline-block',
                     'verticalAlign': 'top', 'textAlign': 'center'}),
            
            # Battle Info
            html.Div([
                html.Div(id='battle-prediction',
                        style={'textAlign': 'center',
                               'marginBottom': '10px',
                               'fontWeight': 'bold'}),
                html.Button('Simulate Battle',
                          id='simulate-battle-btn',
                          style={'width': '100%',
                                 'padding': '10px',
                                 'backgroundColor': '#4CAF50',
                                 'color': 'white',
                                 'border': 'none',
                                 'borderRadius': '5px',
                                 'cursor': 'pointer'})
            ], style={'width': '10%', 'display': 'inline-block',
                     'verticalAlign': 'top'}),
            
            # Pokemon 2 Display
            html.Div([
                html.Img(id='pokemon2-image',
                        style={'maxWidth': '200px',
                               'maxHeight': '200px'}),
                html.Div(id='pokemon2-stats')
            ], style={'width': '45%', 'display': 'inline-block',
                     'verticalAlign': 'top', 'textAlign': 'center'})
        ], style={'marginBottom': '20px'}),
        
        # Battle Log
        html.Div([
            html.H3('Battle Log'),
            html.Pre(id='battle-log',
                    style={'whiteSpace': 'pre-wrap',
                           'border': '1px solid #ddd',
                           'padding': '10px',
                           'maxHeight': '300px',
                           'overflowY': 'auto'})
        ])
    ], style={'padding': '20px'}) 