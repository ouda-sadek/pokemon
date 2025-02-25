import requests
import pygame
from io import BytesIO  # Ajouter cette ligne pour importer BytesIO
from config import *
import random

class Pokemon:
    def __init__(self, pokemon_name, max_hp=None, level=5):
        # Récupérer les données du Pokémon via l'API
        self.name, self.types, self.image, self.sprite_url, self.max_hp = self.load_pokemon_data(pokemon_name.lower())
        
        # Si max_hp est fourni, utiliser cette valeur, sinon utiliser la valeur de l'API
        if max_hp is not None:
            self.max_hp = max_hp
        
        self.current_hp = self.max_hp
        self.level = level
        self.hp_x = 100  # Position x pour la barre de vie
        self.hp_y = 50  # Position y pour la barre de vie
        self.font = pygame.font.Font(None, 40)  # Police pour le nom
        self.type_font = pygame.font.Font(None, 30)  # Police pour les types
        self.moves = []
    def load_pokemon_data(self, pokemon_name):
        """Récupère les données d'un Pokémon depuis l'API PokéAPI et télécharge l'image"""
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
        response = requests.get(url)
        # Vérification que la requête est réussie
        if response.status_code != 200:
            raise ValueError(f"Erreur lors de la récupération du Pokémon {pokemon_name}.")
        data = response.json()
        
        # Extraire les informations
        name = data["name"].capitalize()
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        image_url = data["sprites"]["front_default"]
        back_url = data["sprites"]["back_default"]
        max_hp = data["stats"][0]["base_stat"]  # HP du Pokémon
        self.moves = [move['move']['name'] for move in data['moves'][:4]]  # Prendre uniquement les 4 premiers mouvements
        # Télécharger l'image depuis l'URL
        image_response = requests.get(image_url)
        image_data = BytesIO(image_response.content)
        
        # Charger l'image dans Pygame
        image = pygame.image.load(image_data)
        image = pygame.transform.scale(image, (200, 200))  # Ajuster la taille si nécessaire
        
        return name, types, image, back_url, max_hp
    def get_moves(self):
        """Retourne les mouvements du Pokémon, limité à 4"""
        return self.moves
    def take_damage(self, damage):
        """Applique les dégâts reçus à ce Pokémon."""
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
    
  
    
    def set_sprite(self, sprite_type):
        """Change l'image du Pokémon en fonction du type de sprite"""
        if sprite_type == "back_default":
            # Changer l'image vers le sprite arrière
            image_response = requests.get(self.sprite_url)
            image_data = BytesIO(image_response.content)
            self.image = pygame.image.load(image_data)
            self.image = pygame.transform.scale(self.image, (200, 200))  # Ajuster la taille si nécessaire

    def draw(self, screen, x, y):
        """Affiche le Pokémon à la position (x, y)"""
        # Dessiner le nom du Pokémon au-dessus de l'image
        name_surface = self.font.render(self.name, True, BLACK)  # Texte en noir
        # Afficher les types sous le nom
        type_text = ", ".join(self.types)  # Combiner les types en une seule chaîne
        type_surface = self.type_font.render(type_text, True, (255, 255, 255))  # Texte des types en blanc
        
        # Calculer la largeur du texte des types et le centrer horizontalement
        type_width = type_surface.get_width()
        type_x = x + (200 - type_width) // 2  # Centrer les types sous l'image

        # Afficher les types sous le nom
        screen.blit(type_surface, (type_x, y - 50))  # Position ajustée pour placer les types sous le nom

        # Calculer la largeur du texte du nom et le centrer horizontalement
        name_width = name_surface.get_width()
        name_x = x + (200 - name_width) // 2  # Centrer le nom au-dessus de l'image
        
        # Dessiner le nom au-dessus de l'image
        screen.blit(name_surface, (name_x, y - 100))  # Ajusté pour le placer au-dessus de l'image
        screen.blit(self.image, (x, y))  # Dessiner l'image du Pokémon

        # Afficher la barre de vie au-dessus du Pokémon
        #self.draw_health_bar(screen, x, y - 10)
    
    def draw_health_bar(self, screen, x, y):
        """Affiche la barre de vie du Pokémon à la position (x, y)."""
        health_bar_width = 200  # Largeur de la barre de vie
        health_bar_height = 20  # Hauteur de la barre de vie
        health_ratio = self.current_hp / self.max_hp  # Proportion des points de vie restants

        # Dessiner la barre de fond (barre vide)
        pygame.draw.rect(screen, (50, 50, 50), (x, y, health_bar_width, health_bar_height))

        # Choisir la couleur de la barre en fonction des points de vie
        if self.current_hp > self.max_hp * 0.5:
            bar_color = (0, 255, 0)  # Vert pour plus de 50% de vie
        elif self.current_hp > self.max_hp * 0.2:
            bar_color = (255, 255, 0)  # Jaune pour entre 20% et 50% de vie
        else:
            bar_color = (255, 0, 0)  # Rouge pour moins de 20% de vie

        # Dessiner la barre de vie (barre pleine selon les HP actuels)
        pygame.draw.rect(screen, bar_color, (x, y, health_bar_width * health_ratio, health_bar_height))
        
        # Afficher le niveau du Pokémon
        font = pygame.font.Font(pygame.font.get_default_font(), 14)
        text = font.render(f"Lvl: {self.level}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = x + 150
        text_rect.y = y + 30
        screen.blit(text, text_rect)

        # Afficher le texte HP actuel / max HP
        text_hp = font.render(f"HP: {self.current_hp} / {self.max_hp}", True, (255, 255, 255))
        text_hp_rect = text_hp.get_rect()
        text_hp_rect.x = x
        text_hp_rect.y = y + 30
        screen.blit(text_hp, text_hp_rect)

    def attack(self, target, move_power):
        """Exécuter une attaque et infliger des dégâts."""
        damage = self.calculate_damage(target, move_power)
        target.take_damage(damage)
        return damage


    def is_alive(self):
        """Vérifier si le Pokémon est encore en vie."""
        return self.current_hp > 0
    
    def calculate_damage(self, target, move_power):
        """Calculer les dégâts en tenant compte de l'attaque, de la défense et des types."""
        # Calcul des dégâts de base : [(Attaque - Défense) * 2] (simplifié ici)
        base_damage = (self.attack - target.defense) + move_power

        # Appliquer les multiplicateurs de type
        type_multiplier = self.get_type_multiplier(target)
        final_damage = base_damage * type_multiplier

        # Ajouter une probabilité que l'attaque rate
        if random.random() > 0.95:  # 5% de chance de rater
            return 0  # L'attaque rate

        return max(0, final_damage)
    
    def get_type_multiplier(self, target):
        """Renvoie le multiplicateur basé sur les types."""
        # Exemple simple : À étendre avec un véritable tableau de types
        type_chart = {
            ('Feu', 'Plante'): 2.0,
            ('Feu', 'Eau'): 0.5,
            ('Plante', 'Eau'): 2.0,
            # etc.
        }
        for attacker_type in self.types:
            for defender_type in target.types:
                multiplier = type_chart.get((attacker_type, defender_type), 1.0)
                if multiplier != 1.0:
                    return multiplier
        return 1.0


