# Fight Logic  (pokemons player / bot)
# System probability miss attack, turning Player - Bot, check if pokemons's life are 0, 
# and check if can replace the active pokemon by another from the 'owner hand'.
# First start --> The better speed.
# Attack damage depend on multiplier
# Add new pokemon in pokedex if it's not already discover

import random
import json
from game import *      # récuperer les pokemon actif player et opposant

file_pokemon = '/data/pokemon.json'
file_pokedex = '/data/pokedex.json'



class Fight:
    def __init__(self, pokemon_player, pokemon_opponent):
        self.pokemon_player = pokemon_player
        self.pokemon_opponent = pokemon_opponent

    # Method to determine who attacks first based on speed
    def first_tour(self):
        if self.pokemon_player.active_pokemon.speed >= self.pokemon_opponent.active_pokemon.speed:
            self.pokemon_tour = "Player"
            print("The player starts")
        else:
            self.pokemon_tour = "Bot"
            print("The bot starts")

    # Executes an attack from the active Pokémon
    def attack(self):
        if self.pokemon_tour == "Player":
            attacker = self.pokemon_player
            defender = self.pokemon_opponent
        else:
            attacker = self.pokemon_opponent
            defender = self.pokemon_player

        if random.random() < 0.2:  # 20% chance to miss the attack
            if self.pokemon_tour == "Player":
                self.pokemon_tour = "Bot"
            else:
                self.pokemon_tour = "Player"
            return f"Attack missed, it is the {self.pokemon_tour} tour."
        else:
            # Call methode to calculate and inflige damage
            self.calculate_damage(attacker, defender)
            
            # Checks if the attacked Pokémon is KO
            if defender.active_pokemon.vie <= 0:
                return self.life_check(defender.active_pokemon)
        
        # Switches turn
        if self.pokemon_tour == "Player":
            self.pokemon_tour = "Bot"
        else:
            self.pokemon_tour = "Player"
    

    def calculate_damage(self, attacker, defender):
        # Damage calculation based on attack, type, and defense
        degats_net = max(attacker.active_pokemon.attack * self.get_type_multiplier(attacker.active_pokemon, defender.active_pokemon) - defender.active_pokemon.defense, 0)
        # '0' to avoid negative damage just in case
        defender.active_pokemon.vie -= degats_net
        print(f"{attacker.active_pokemon.nom} attacks! {defender.active_pokemon.nom} loses {degats_net} HP.")

    # Returns the type multiplier based on Pokémon type effectiveness
    def get_type_multiplier(self, attacker, defender):
        type_chart = {
            ("Eau", "Feu"): 2.0, ("Feu", "Eau"): 0.5, ("Plante", "Eau"): 2.0, ("Eau", "Plante"): 0.5,
            ("Feu", "Plante"): 2.0, ("Plante", "Feu"): 0.5
        }
        return type_chart.get((attacker.type, defender.type), 1.0)
    
    # Checks if the active Pokémon is KO and replaces it if necessary
    def life_check(self, active_pokemon):
        if active_pokemon.vie <= 0:     # Active Pokémon KO
            active_pokemon.etat = False
            # Checks if the trainer still has a Pokémon with HP remaining
            for pokemon in self.trainer.pokemons:
                if pokemon.vie > 0:
                    return self.replace_pokemon_ko()    # Replace the active Pokémon with one from the bench
            # If no Pokémon is available, the game is lost
            return f"Trainer {self.trainer.name} has no more Pokémon able to fight! They lost the game."
        return "The battle continues."

    # Replaces a KO Pokémon with one from the bench
    def replace_pokemon_ko(self):
        # List to store available Pokémon still playable
        available_pokemons = []
        for pokemon in self.trainer.pokemons:
            available_pokemons.append(pokemon)
        if self.trainer.is_player:
            while True:
                try:
                    # Show pokemons available to take for the replace
                    print("Choose a replacement Pokémon:")
                    for i, p in enumerate(available_pokemons):
                        print(f"{i + 1}. {p.nom}")
                    choice = int(input("Enter the number: ")) - 1
                    break
                except ValueError:
                    print("Please enter a valid number")
        else:
            choice = random.randint(0, len(available_pokemons) - 1)
        self.trainer.active_pokemon = available_pokemons[choice]
        return f"{self.trainer.name} has replaced their Pokémon with {self.trainer.active_pokemon.nom}"

    # Updates the Pokédex with encountered Pokémon
    def update_pokedex(self, pokemon):
        try:
            with open(file_pokedex, 'r') as f:
                pokedex = json.load(f)
        except FileNotFoundError:
            pokedex = []
        
        # Adds the Pokémon if it is not already recorded
        pokemon_exist = False
        for p in pokedex:
            if p["nom"] == pokemon.nom:
                pokemon_exist = True
                break
        if not pokemon_exist:
            pokedex.append({"nom": pokemon.nom, "type": pokemon.type, "vie": pokemon.vie, "attaque": pokemon.attack, "defense": pokemon.defense})
        
        with open(file_pokedex, 'w') as f:
            json.dump(pokedex, f, indent=4)