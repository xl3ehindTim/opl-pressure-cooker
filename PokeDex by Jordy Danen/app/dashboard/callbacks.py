"""Dashboard callbacks module."""
from dash import Input, Output, State, ALL, callback_context, html, dcc, no_update
import plotly.graph_objects as go
import pandas as pd
from app.components.pokemon_grid import create_pokemon_grid
from app.components.pokemon_info import create_pokemon_info, create_moves_display
from app.components.navigation import create_navigation_buttons
from app.data.pokemon_data import pokemon_df

def register_callbacks(app):
    """Register all callbacks for the dashboard."""
    
    @app.callback(
        [Output('pokemon-display', 'children'),
         Output('tabs', 'value', allow_duplicate=True),
         Output('pokemon1-select', 'value', allow_duplicate=True)],
        [Input('home-button', 'n_clicks'),
         Input({'type': 'pokemon-select', 'index': ALL}, 'n_clicks'),
         Input({'type': 'battle-button', 'pokemon': ALL}, 'n_clicks')],
        [State({'type': 'pokemon-select', 'index': ALL}, 'id'),
         State({'type': 'battle-button', 'pokemon': ALL}, 'id')],
        prevent_initial_call=True
    )
    def update_selected_pokemon(home_clicks, pokemon_clicks, battle_clicks, pokemon_ids, battle_ids):
        ctx = callback_context
        if not ctx.triggered:
            return create_pokemon_grid(pokemon_df), no_update, no_update
        
        triggered_id = ctx.triggered[0]['prop_id']
        
        # Handle home button click
        if triggered_id == 'home-button.n_clicks':
            return create_pokemon_grid(pokemon_df), 'Pokédex Entry', no_update
        
        # Handle battle button click
        if '.n_clicks' in triggered_id and 'battle-button' in triggered_id:
            pokemon_name = eval(triggered_id.split('.')[0])['pokemon']
            return create_pokemon_grid(pokemon_df), 'Battle Simulator', pokemon_name
        
        # Handle Pokemon selection
        if '.n_clicks' in triggered_id:
            pokemon_name = eval(triggered_id.split('.')[0])['index']
            
            # Check for return to list
            if pokemon_name == 'return':
                return create_pokemon_grid(pokemon_df), no_update, no_update
                
            if not pokemon_name:
                return create_pokemon_grid(pokemon_df), no_update, no_update
                
            pokemon = pokemon_df[pokemon_df['name'] == pokemon_name].iloc[0]
            
            # Create Pokemon info display with navigation
            return html.Div([
                create_navigation_buttons(pokemon_df, pokemon_name),
                create_pokemon_info(pokemon),
                create_moves_display(pokemon_df, pokemon)
            ]), no_update, no_update
    
    @app.callback(
        [Output('gen-button-' + str(i), 'className') for i in sorted(pokemon_df['generation'].unique())] +
        [Output('active-generations', 'children')],
        [Input('gen-button-' + str(i), 'n_clicks') for i in sorted(pokemon_df['generation'].unique())]
    )
    def update_button_states(*args):
        ctx = callback_context
        
        # Initialize all generations as active on first load
        if not ctx.triggered or ctx.triggered[0]['prop_id'] == '.':
            active_gens = list(sorted(pokemon_df['generation'].unique()))
            return ['gen-button active'] * len(active_gens) + [str(active_gens)]
        
        # Get which button was clicked
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        clicked_gen = int(button_id.split('-')[-1])
        
        # Get current states
        button_states = []
        active_gens = []
        
        # Get all button states
        for i in sorted(pokemon_df['generation'].unique()):
            button_key = f'gen-button-{i}.className'
            # Default to active if state not found
            current_state = 'gen-button active'
            
            # Only toggle the clicked button
            if i == clicked_gen:
                if button_key in ctx.states and 'active' in ctx.states[button_key]:
                    current_state = 'gen-button'  # Deactivate if it was active
                else:
                    current_state = 'gen-button active'  # Activate if it was inactive
            else:
                # Keep existing state or default to active
                if button_key in ctx.states:
                    current_state = ctx.states[button_key]
            
            button_states.append(current_state)
            if 'active' in current_state:
                active_gens.append(i)
        
        # Ensure at least one generation is active
        if not active_gens:
            active_gens = [clicked_gen]
            button_states[sorted(pokemon_df['generation'].unique()).index(clicked_gen)] = 'gen-button active'
        
        return button_states + [str(active_gens)]

    @app.callback(
        [Output('primary-type-dist', 'figure'),
         Output('type-heatmap', 'figure')],
        [Input('active-generations', 'children')]
    )
    def update_type_distributions(active_gens_str):
        try:
            selected_generations = [int(x.strip()) for x in active_gens_str.strip('[]').split(',') if x.strip()]
        except:
            selected_generations = list(sorted(pokemon_df['generation'].unique()))
        
        # Create simpler bar chart
        type_dist_data = []
        for gen in selected_generations:
            type_counts = pokemon_df[pokemon_df['generation'] == gen]['type1'].value_counts()
            type_dist_data.append(
                go.Bar(
                    name=f'Gen {gen}',
                    x=sorted(pokemon_df['type1'].unique()),
                    y=[type_counts.get(t, 0) for t in sorted(pokemon_df['type1'].unique())]
                )
            )
        
        type_dist_fig = {
            'data': type_dist_data,
            'layout': {
                'title': 'Type Distribution by Generation',
                'barmode': 'group',
                'template': 'plotly_dark'
            }
        }
        
        # Create simpler heatmap
        filtered_df = pokemon_df[pokemon_df['generation'].isin(selected_generations)]
        type_combinations = pd.crosstab(filtered_df['type1'], filtered_df['type2'])
        
        heatmap_fig = {
            'data': [
                go.Heatmap(
                    z=type_combinations.values,
                    x=type_combinations.columns,
                    y=type_combinations.index
                )
            ],
            'layout': {
                'title': 'Type Combinations Heatmap',
                'template': 'plotly_dark'
            }
        }
        
        return type_dist_fig, heatmap_fig

    @app.callback(
        [Output('stats-comparison', 'figure'),
         Output('stats-distribution', 'figure')],
        [Input('pokemon-compare', 'value')]
    )
    def update_stats_analysis(selected_pokemon):
        # Initialize empty figures if no Pokemon selected
        if not selected_pokemon:
            selected_pokemon = []  # Convert None to empty list
        
        # Stats radar chart for comparison
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        
        comparison_fig = go.Figure()
        for pokemon_name in selected_pokemon:
            pokemon = pokemon_df[pokemon_df['name'] == pokemon_name].iloc[0]
            stat_values = [pokemon[stat] for stat in stats]
            
            comparison_fig.add_trace(go.Scatterpolar(
                r=stat_values + [stat_values[0]],
                theta=stats + [stats[0]],
                fill='toself',
                name=pokemon_name
            ))
        
        comparison_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, pokemon_df[stats].max().max() * 1.2])),
            showlegend=True,
            title='Stats Comparison',
            plot_bgcolor='rgba(0,0,0,0.1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        # Stats distribution boxplots with selected Pokemon highlighted
        stats_dist_fig = go.Figure()
        
        # Add boxplots for each stat
        for stat in stats:
            stats_dist_fig.add_trace(go.Box(
                y=pokemon_df[stat],
                name=stat,
                boxpoints='outliers',
                marker_color='lightgray',
                showlegend=False
            ))
            
            # Add markers for selected Pokemon
            for pokemon_name in selected_pokemon:
                pokemon = pokemon_df[pokemon_df['name'] == pokemon_name].iloc[0]
                stats_dist_fig.add_trace(go.Scatter(
                    x=[stat],
                    y=[pokemon[stat]],
                    mode='markers',
                    name=pokemon_name,
                    marker=dict(
                        size=10,
                        symbol='star',
                        line=dict(width=2)
                    ),
                    showlegend=True
                ))
        
        stats_dist_fig.update_layout(
            title='Stats Distribution (Selected Pokemon shown as stars)',
            yaxis_title='Value',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            # Add hover template
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12
            )
        )
        
        return comparison_fig, stats_dist_fig 