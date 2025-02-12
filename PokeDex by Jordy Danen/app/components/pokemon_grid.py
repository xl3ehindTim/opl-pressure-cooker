"""Pokemon grid component module."""
from dash import html
from app.utils.helpers import get_pokemon_image_url
from app.utils.constants import POKEMON_COLORS

def create_pokemon_grid(df):
    """Create the Pokemon grid component."""
    return html.Div([
        html.Div([
            html.Div([
                html.Img(
                    src=get_pokemon_image_url(row['pokedex_number']),
                    style={
                        'width': '50px',
                        'height': '50px',
                        'imageRendering': 'pixelated'
                    }
                ),
                html.Div(
                    f"#{row['pokedex_number']} {row['name']}",
                    style={
                        'fontSize': '12px',
                        'fontFamily': POKEMON_COLORS['pixel_font'],
                        'color': 'white',
                        'textAlign': 'center',
                        'marginTop': '5px'
                    }
                )
            ],
            id={'type': 'pokemon-select', 'index': row['name']},
            className='pokemon-grid-item',
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'padding': '10px',
                'backgroundColor': '#2c3e50',
                'borderRadius': '8px',
                'cursor': 'pointer',
                'transition': 'all 0.3s ease'
            }
            ) for _, row in df.sort_values('pokedex_number').iterrows()
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fill, minmax(100px, 1fr))',
            'gap': '10px',
            'padding': '20px',
            'maxHeight': '70vh',
            'overflowY': 'auto'
        })
    ], id='pokemon-grid') 