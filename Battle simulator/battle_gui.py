import tkinter as tk
from tkinter import ttk
from battle_simulator import BattleSimulator, Pokemon
import threading
import time
from PIL import Image, ImageTk
import requests
import io
import os
import random

class PokemonBattleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Battle Simulator")
        self.root.geometry("800x600")
        
        # Initialize battle simulator
        self.simulator = BattleSimulator()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create battle selection frame
        self.create_selection_frame()
        
        # Create battle display frame
        self.create_battle_frame()
        
        # Create battle log frame
        self.create_log_frame()
        
        # Initialize image cache
        self.image_cache = {}
        
    def create_selection_frame(self):
        """Create the Pokemon selection interface"""
        selection_frame = ttk.LabelFrame(self.main_frame, text="Select Pokemon", padding="5")
        selection_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Get list of Pokemon names
        pokemon_names = sorted(self.simulator.pokemon_data['name'].tolist())
        
        # Pokemon 1 selection
        ttk.Label(selection_frame, text="Pokemon 1:").grid(row=0, column=0, padx=5)
        self.pokemon1_var = tk.StringVar()
        self.pokemon1_combo = ttk.Combobox(selection_frame, textvariable=self.pokemon1_var)
        self.pokemon1_combo['values'] = pokemon_names
        self.pokemon1_combo.grid(row=0, column=1, padx=5)
        self.pokemon1_combo.set(pokemon_names[0])
        
        # Pokemon 2 selection
        ttk.Label(selection_frame, text="Pokemon 2:").grid(row=0, column=2, padx=5)
        self.pokemon2_var = tk.StringVar()
        self.pokemon2_combo = ttk.Combobox(selection_frame, textvariable=self.pokemon2_var)
        self.pokemon2_combo['values'] = pokemon_names
        self.pokemon2_combo.grid(row=0, column=3, padx=5)
        self.pokemon2_combo.set(pokemon_names[1])
        
        # Start battle button
        self.start_button = ttk.Button(selection_frame, text="Start Battle", command=self.start_battle)
        self.start_button.grid(row=0, column=4, padx=5)

    def create_battle_frame(self):
        """Create the battle display interface"""
        self.battle_frame = ttk.LabelFrame(self.main_frame, text="Battle", padding="5")
        self.battle_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Pokemon 1 display
        self.pokemon1_frame = ttk.Frame(self.battle_frame)
        self.pokemon1_frame.grid(row=0, column=0, padx=10)
        
        self.pokemon1_image_label = ttk.Label(self.pokemon1_frame)
        self.pokemon1_image_label.grid(row=0, column=0)
        
        self.pokemon1_hp_var = tk.StringVar(value="HP: 100%")
        self.pokemon1_hp_label = ttk.Label(self.pokemon1_frame, textvariable=self.pokemon1_hp_var)
        self.pokemon1_hp_label.grid(row=1, column=0)
        
        self.pokemon1_status_var = tk.StringVar(value="")
        self.pokemon1_status_label = ttk.Label(self.pokemon1_frame, textvariable=self.pokemon1_status_var)
        self.pokemon1_status_label.grid(row=2, column=0)
        
        # VS label
        ttk.Label(self.battle_frame, text="VS").grid(row=0, column=1)
        
        # Pokemon 2 display
        self.pokemon2_frame = ttk.Frame(self.battle_frame)
        self.pokemon2_frame.grid(row=0, column=2, padx=10)
        
        self.pokemon2_image_label = ttk.Label(self.pokemon2_frame)
        self.pokemon2_image_label.grid(row=0, column=0)
        
        self.pokemon2_hp_var = tk.StringVar(value="HP: 100%")
        self.pokemon2_hp_label = ttk.Label(self.pokemon2_frame, textvariable=self.pokemon2_hp_var)
        self.pokemon2_hp_label.grid(row=1, column=0)
        
        self.pokemon2_status_var = tk.StringVar(value="")
        self.pokemon2_status_label = ttk.Label(self.pokemon2_frame, textvariable=self.pokemon2_status_var)
        self.pokemon2_status_label.grid(row=2, column=0)

    def create_log_frame(self):
        """Create the battle log interface"""
        log_frame = ttk.LabelFrame(self.main_frame, text="Battle Log", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        self.log_text = tk.Text(log_frame, height=10, width=70, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set

    def get_pokemon_image(self, pokemon_name):
        """Get Pokemon image from the web or cache"""
        if pokemon_name in self.image_cache:
            return self.image_cache[pokemon_name]
        
        # Create images directory if it doesn't exist
        if not os.path.exists('images'):
            os.makedirs('images')
        
        image_path = f'images/{pokemon_name.lower()}.png'
        
        # Check if image exists locally
        if os.path.exists(image_path):
            image = Image.open(image_path)
        else:
            # Get Pokemon ID from the dataset
            pokemon_id = self.simulator.pokemon_data[
                self.simulator.pokemon_data['name'] == pokemon_name
            ].index[0] + 1
            
            # Download image from PokeAPI
            url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png'
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))
            
            # Save image locally
            image.save(image_path)
        
        # Resize image
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_cache[pokemon_name] = photo
        return photo

    def update_battle_log(self, message):
        """Update the battle log with a new message"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def update_pokemon_display(self, pokemon1, pokemon2):
        """Update Pokemon display with current battle state"""
        # Update Pokemon 1
        hp_percentage1 = (pokemon1.current_hp / pokemon1.max_hp) * 100
        self.pokemon1_hp_var.set(f"HP: {hp_percentage1:.1f}%")
        self.pokemon1_status_var.set(f"Status: {pokemon1.status or 'None'}")
        
        # Update Pokemon 2
        hp_percentage2 = (pokemon2.current_hp / pokemon2.max_hp) * 100
        self.pokemon2_hp_var.set(f"HP: {hp_percentage2:.1f}%")
        self.pokemon2_status_var.set(f"Status: {pokemon2.status or 'None'}")
        
        self.root.update()

    def start_battle(self):
        """Start the battle simulation"""
        # Disable start button during battle
        self.start_button.state(['disabled'])
        
        # Clear battle log
        self.log_text.delete(1.0, tk.END)
        
        # Get selected Pokemon
        pokemon1_name = self.pokemon1_var.get()
        pokemon2_name = self.pokemon2_var.get()
        
        # Load Pokemon images
        self.pokemon1_image_label.configure(image=self.get_pokemon_image(pokemon1_name))
        self.pokemon2_image_label.configure(image=self.get_pokemon_image(pokemon2_name))
        
        # Start battle in separate thread
        battle_thread = threading.Thread(
            target=self.run_battle,
            args=(pokemon1_name, pokemon2_name)
        )
        battle_thread.start()

    def run_battle(self, pokemon1_name, pokemon2_name):
        """Run the battle simulation"""
        try:
            # Initialize Pokemon
            pokemon1_data = self.simulator.pokemon_data[
                self.simulator.pokemon_data['name'] == pokemon1_name
            ].iloc[0]
            pokemon2_data = self.simulator.pokemon_data[
                self.simulator.pokemon_data['name'] == pokemon2_name
            ].iloc[0]
            
            pokemon1 = Pokemon(pokemon1_name, pokemon1_data)
            pokemon2 = Pokemon(pokemon2_name, pokemon2_data)
            
            # Battle loop
            turn = 1
            while pokemon1.current_hp > 0 and pokemon2.current_hp > 0:
                self.update_battle_log(f"\nTurn {turn}")
                
                # Determine turn order
                first = pokemon1 if pokemon1.speed >= pokemon2.speed else pokemon2
                second = pokemon2 if first == pokemon1 else pokemon1
                
                # First Pokemon's turn
                self.simulate_turn(first, second)
                self.update_pokemon_display(pokemon1, pokemon2)
                time.sleep(1)  # Add delay for readability
                
                if second.current_hp <= 0:
                    self.update_battle_log(f"\n{first.name} wins!")
                    break
                
                # Second Pokemon's turn
                self.simulate_turn(second, first)
                self.update_pokemon_display(pokemon1, pokemon2)
                time.sleep(1)  # Add delay for readability
                
                if first.current_hp <= 0:
                    self.update_battle_log(f"\n{second.name} wins!")
                    break
                
                turn += 1
        
        finally:
            # Re-enable start button
            self.root.after(0, lambda: self.start_button.state(['!disabled']))

    def simulate_turn(self, attacker, defender):
        """Simulate one turn of the battle"""
        # Select random move
        move = self.simulator.moves_database[
            random.choice(list(self.simulator.moves_database.keys()))
        ]
        
        self.update_battle_log(f"{attacker.name} used {move.name}!")
        
        # Calculate and apply damage
        damage = self.simulator.calculate_damage(attacker, defender, move)
        defender.current_hp = max(0, defender.current_hp - damage)
        
        self.update_battle_log(
            f"{defender.name} took {damage} damage! "
            f"({defender.current_hp}/{defender.max_hp} HP remaining)"
        )

def main():
    root = tk.Tk()
    app = PokemonBattleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
