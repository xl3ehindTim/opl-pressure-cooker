"""Constants used throughout the application."""

# Color constants
POKEMON_COLORS = {
    'background': '#f5f5f5',
    'pokeball_red': '#EE1515',
    'pokeball_white': '#FFFFFF',
    'pokeball_black': '#222224',
    'pokedex_blue': '#3B4CCA',
    'pokemon_yellow': '#FFDE00',
    'pokemon_blue': '#3B4CCA',
    'type_box': '#30a7d7',
    'card_shadow': '0 4px 8px rgba(0,0,0,0.1)',
    'pixel_font': '"Press Start 2P", cursive',
    'regular_font': 'Arial, sans-serif'
}

# Type colors
TYPE_COLORS = {
    'normal': '#A8A878',
    'fire': '#F08030',
    'water': '#6890F0',
    'electric': '#F8D030',
    'grass': '#78C850',
    'ice': '#98D8D8',
    'fighting': '#C03028',
    'poison': '#A040A0',
    'ground': '#E0C068',
    'flying': '#A890F0',
    'psychic': '#F85888',
    'bug': '#A8B820',
    'rock': '#B8A038',
    'ghost': '#705898',
    'dragon': '#7038F8',
    'dark': '#705848',
    'steel': '#B8B8D0',
    'fairy': '#EE99AC'
}

# Type effectiveness matrix
TYPE_EFFECTIVENESS = {
    'normal': {'rock': 0.5, 'ghost': 0, 'steel': 0.5},
    'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 2, 'bug': 2, 'rock': 0.5, 'dragon': 0.5, 'steel': 2},
    'water': {'fire': 2, 'water': 0.5, 'grass': 0.5, 'ground': 2, 'rock': 2, 'dragon': 0.5},
    'electric': {'water': 2, 'electric': 0.5, 'grass': 0.5, 'ground': 0, 'flying': 2, 'dragon': 0.5},
    'grass': {'fire': 0.5, 'water': 2, 'grass': 0.5, 'poison': 0.5, 'ground': 2, 'flying': 0.5, 'bug': 0.5, 'rock': 2, 'dragon': 0.5, 'steel': 0.5},
    'ice': {'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 0.5, 'ground': 2, 'flying': 2, 'dragon': 2, 'steel': 0.5},
    'fighting': {'normal': 2, 'ice': 2, 'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 2, 'ghost': 0, 'dark': 2, 'steel': 2, 'fairy': 0.5},
    'poison': {'grass': 2, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0, 'fairy': 2},
    'ground': {'fire': 2, 'electric': 2, 'grass': 0.5, 'poison': 2, 'flying': 0, 'bug': 0.5, 'rock': 2, 'steel': 2},
    'flying': {'electric': 0.5, 'grass': 2, 'fighting': 2, 'bug': 2, 'rock': 0.5, 'steel': 0.5},
    'psychic': {'fighting': 2, 'poison': 2, 'psychic': 0.5, 'dark': 0, 'steel': 0.5},
    'bug': {'fire': 0.5, 'grass': 2, 'fighting': 0.5, 'poison': 0.5, 'flying': 0.5, 'psychic': 2, 'ghost': 0.5, 'dark': 2, 'steel': 0.5, 'fairy': 0.5},
    'rock': {'fire': 2, 'ice': 2, 'fighting': 0.5, 'ground': 0.5, 'flying': 2, 'bug': 2, 'steel': 0.5},
    'ghost': {'normal': 0, 'psychic': 2, 'ghost': 2, 'dark': 0.5},
    'dragon': {'dragon': 2, 'steel': 0.5, 'fairy': 0},
    'dark': {'fighting': 0.5, 'psychic': 2, 'ghost': 2, 'dark': 0.5, 'fairy': 0.5},
    'steel': {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2, 'rock': 2, 'steel': 0.5, 'fairy': 2},
    'fairy': {'fire': 0.5, 'fighting': 2, 'poison': 0.5, 'dragon': 2, 'dark': 2, 'steel': 0.5}
}

# Common moves for each type
TYPE_MOVES = {
    'normal': ['Tackle', 'Quick Attack', 'Hyper Beam', 'Body Slam'],
    'fire': ['Flamethrower', 'Fire Blast', 'Fire Punch', 'Heat Wave'],
    'water': ['Hydro Pump', 'Surf', 'Water Pulse', 'Aqua Jet'],
    'electric': ['Thunderbolt', 'Thunder', 'Thunder Wave', 'Volt Tackle'],
    'grass': ['Solar Beam', 'Leaf Blade', 'Energy Ball', 'Giga Drain'],
    'ice': ['Ice Beam', 'Blizzard', 'Ice Punch', 'Freeze-Dry'],
    'fighting': ['Close Combat', 'Dynamic Punch', 'Brick Break', 'Aura Sphere'],
    'poison': ['Sludge Bomb', 'Poison Jab', 'Toxic', 'Gunk Shot'],
    'ground': ['Earthquake', 'Earth Power', 'Dig', 'Bulldoze'],
    'flying': ['Air Slash', 'Brave Bird', 'Hurricane', 'Aerial Ace'],
    'psychic': ['Psychic', 'Psybeam', 'Psycho Cut', 'Zen Headbutt'],
    'bug': ['Bug Buzz', 'X-Scissor', 'Megahorn', 'Signal Beam'],
    'rock': ['Stone Edge', 'Rock Slide', 'Rock Tomb', 'Ancient Power'],
    'ghost': ['Shadow Ball', 'Shadow Claw', 'Shadow Punch', 'Phantom Force'],
    'dragon': ['Dragon Claw', 'Outrage', 'Dragon Pulse', 'Draco Meteor'],
    'dark': ['Dark Pulse', 'Crunch', 'Night Slash', 'Foul Play'],
    'steel': ['Iron Head', 'Flash Cannon', 'Steel Wing', 'Meteor Mash'],
    'fairy': ['Moonblast', 'Dazzling Gleam', 'Play Rough', 'Draining Kiss']
} 