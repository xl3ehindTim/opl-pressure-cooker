"""Main application module."""
from dash import Dash, html, dcc, Input, Output
from app.dashboard import layout as dashboard_layout
from app.dashboard import callbacks as dashboard_callbacks
from app.battle import callbacks as battle_callbacks

def create_app():
    """Create and configure the Dash application."""
    app = Dash(
        __name__,
        external_stylesheets=['https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap'],
        suppress_callback_exceptions=True,
        assets_folder='../static'
    )
    
    # Set the layout directly
    app.layout = dashboard_layout.create_layout(app)
    
    # Register callbacks
    dashboard_callbacks.register_callbacks(app)
    battle_callbacks.register_callbacks(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True) 