# Pokédex with Battle Simulator

A modern web-based Pokédex application built with Python and Dash, featuring a battle simulator and detailed Pokémon statistics.

## Features

- **Pokédex Entry**: Browse through all Pokémon with their basic information and stats
- **Type Analysis**: Visualize Pokémon type distributions and combinations across generations
- **Stats Analysis**: Compare Pokémon stats with interactive radar charts and distribution plots
- **Battle Simulator**: Simulate battles between any two Pokémon with:
  - Type effectiveness calculations
  - Battle outcome predictions
  - Detailed battle logs
  - Move recommendations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate  # On Windows
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python -m app.main
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8050/
```

## How It Works

### Architecture

The application is built using a modular architecture:

- `app/`
  - `main.py`: Application entry point and server configuration
  - `components/`: Reusable UI components
  - `dashboard/`: Main dashboard layout and callbacks
  - `battle/`: Battle simulation and prediction logic
  - `data/`: Data loading and processing
  - `utils/`: Helper functions and constants

### Features in Detail

#### Pokédex Entry
- View detailed information about each Pokémon
- Navigate through Pokémon using the navigation buttons
- Quick access to battle simulation from any Pokémon's page

#### Type Analysis
- Interactive bar charts showing type distribution across generations
- Heatmap visualization of type combinations
- Generation toggle buttons for filtered analysis

#### Stats Analysis
- Compare multiple Pokémon using radar charts
- View stat distributions with boxplots
- Highlighted markers showing selected Pokémon's stats

#### Battle Simulator
- Select two Pokémon to battle
- View detailed stats comparison
- Get battle outcome predictions based on:
  - Base stats
  - Type effectiveness
  - Move types
- Simulate battles with turn-by-turn logs

### Technologies Used

- **Dash**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **Python**: Core programming language

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 