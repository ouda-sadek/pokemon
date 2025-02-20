import json

class Pokedex:
    def __init__(self, file="pokedex.json"):
        self.pokemon_collection = []
        self.file = file
        self.load_pokedex()

    def load_pokedex(self):
        try:
            with open(self.file, 'r') as file:
                self.pokemon_collection = json.load(file)
        except FileNotFoundError:
            self.pokemon_collection = []

    def add_pokemon(self, pokemon):
        if pokemon.name not in [p['name'] for p in self.pokemon_collection]:
            self.pokemon_collection.append({
                "name": pokemon.name,
                "type": pokemon.types,
                "hp": pokemon.hp,    
                "attack": pokemon.attack,
                "defense": pokemon.defense
            })
            self.save_pokedex()

    def save_pokedex(self):
        with open(self.file, 'w') as file:
            json.dump(self.pokemon_collection, file)

    def display_pokedex(self):
        for pokemon in self.pokemon_collection:
            print(f"Name: {pokemon['name']}, Type: {pokemon['type']}, hp: {pokemon['hp']}")
