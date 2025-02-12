"""Navigation components module."""
from dash import html

def create_navigation_buttons(df, current_pokemon):
    """Create navigation buttons for previous/next Pokemon and return to list."""
    current_number = df[df['name'] == current_pokemon]['pokedex_number'].iloc[0]
    prev_pokemon = df[df['pokedex_number'] == current_number - 1]['name'].iloc[0] if current_number > 1 else None
    next_pokemon = df[df['pokedex_number'] == current_number + 1]['name'].iloc[0] if current_number < df['pokedex_number'].max() else None
    
    return html.Div([
        # Navigation row
        html.Div([
            # Previous Pokemon
            html.Button(
                f"← #{current_number-1} {prev_pokemon}" if prev_pokemon else "",
                id={'type': 'pokemon-select', 'index': prev_pokemon} if prev_pokemon else None,
                className='nav-button prev' if prev_pokemon else 'nav-button disabled',
                style={'visibility': 'visible' if prev_pokemon else 'hidden'}
            ),
            
            # Return to list button
            html.Button(
                "Return to Pokédex",
                id={'type': 'pokemon-select', 'index': 'return'},  # Special index for return
                className='nav-button return',
            ),
            
            # Next Pokemon
            html.Button(
                f"#{current_number+1} {next_pokemon} →" if next_pokemon else "",
                id={'type': 'pokemon-select', 'index': next_pokemon} if next_pokemon else None,
                className='nav-button next' if next_pokemon else 'nav-button disabled',
                style={'visibility': 'visible' if next_pokemon else 'hidden'}
            ),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'marginBottom': '20px',
            'gap': '10px'
        })
    ]) 