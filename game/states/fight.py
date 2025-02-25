import pygame
from config import *
from game.entities.pokemon import Pokemon
import random
import requests
from game.entities.button_fight import ButtonFight 
import math


class Fight:
    def __init__(self, screen):
        self.screen = screen
        self.BACKGROUND_IMAGE = pygame.image.load(r"./assets/images/arène1.jpg")
        self.BACKGROUND_IMAGE = pygame.transform.scale(self.BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

      # Créer une liste de 6 Pokémon du joueur en récupérant leurs données depuis PokéAPI
        self.player_pokemon = [
            Pokemon("bulbasaur"),   # Bulbasaur
            Pokemon("charmander"),   # Charmander
            Pokemon("squirtle"),     # Squirtle
            Pokemon("pikachu"),      # Pikachu
            Pokemon("eevee"),        # Eevee
            Pokemon("mewtwo")        # Mewtwo
        ]
        
        self.computer_pokemon = None  # Initialement aucun Pokémon pour l'ordinateur
        self.font = pygame.font.Font(None, 40)  # Taille de la police pour le texte
        self.selected_pokemon = None  # Aucun Pokémon sélectionné au départ
        self.is_battle_started = False  # Le combat n'a pas encore commencé

        # Définir les boutons avec hover
        self.attack_button = ButtonFight(900, 360, 200, 50, "Pokedex", self.font, (0, 128, 0), (0, 255, 0), self.attack)
        self.defend_button = ButtonFight(900, 430, 200, 50, "Attack", self.font, (0, 0, 255), (135, 206, 250), self.defend)
        self.potion_button = ButtonFight(900, 500, 200, 50, "Potion", self.font, (255, 165, 0), (255, 255, 0), self.use_potion)
        #self.give_up_button = ButtonFight(900, 570, 200, 50, "Give-Up", self.font, (255, 69, 0), (200, 0, 0), self.give_up)
        self.give_up_button = ButtonFight(x=900, y=570, width=200, height=50,text="Give-Up", font=self.font,color=(255, 69, 0), hover_color=(200, 0, 0),action=self.give_up ) # Associer la méthode give_up
        # create the fight and use potion buttons
        self.fight_button = ButtonFight(240, 140, 10, 350, 130, 412, "Fight", self.font,)
        #self.potion_button = ButtonFight(240, 140, 250, 350, 370, 412, f"Use Potion ({self.player_pokemon.num_potions})")
        # draw the BLACK border
        pygame.draw.rect(screen, TRANSPARENT, (10, 350, 480, 140), 3)  #color ok
        
        pygame.display.update()
        
        self.is_defending = False
        self.circle_pos = None
        self.circle_radius = 10
        self.circle_speed = 5  # Vitesse du cercle
        self.circle_target = None  # Cible du cercle (destination)
        self.circle_start = None  # Position de départ
        self.circle_move_direction = None  # Direction du mouvement

       
    def determine_first_turn(self):
        
        """Le plus rapide commence (dépend du niveau ou d'une statistique spécifique)."""
        # Ici on utilise les niveaux pour déterminer qui commence, mais tu peux ajouter d'autres logiques (vitesse, etc.)
        if self.player_pokemon is None or self.computer_pokemon is None:
            raise ValueError("Les Pokémon doivent être initialisés avant de commencer le combat.")
        
        if self.player_pokemon.level >= self.computer_pokemon.level:
            return 'player'
        else:
            return "computer"
        
    def execute_turn(self):
        """Exécuter le tour en cours."""
        if self.turn == 'player':
            move_power = 40  # Exemple de puissance de l'attaque
            damage = self.player_pokemon.attack(self.computer_pokemon, move_power)
            print(f"{self.player_pokemon.name} attaque {self.computer_pokemon.name} et inflige {damage} dégâts !")
            if not self.computer_pokemon.is_alive():
                print(f"{self.computer_pokemon.name} a été vaincu !")
            self.turn = 'computer'
        else:
            move_power = 40  # Exemple de puissance de l'attaque
            damage = self.computer_pokemon.attack(self.player_pokemon, move_power)
            print(f"{self.computer_pokemon.name} attaque {self.player_pokemon.name} et inflige {damage} dégâts !")
            if not self.player_pokemon.is_alive():
                print(f"{self.player_pokemon.name} a été vaincu !")
            self.turn = 'player'

    def run_battle(self):
        """Lancer la bataille et alterner les tours jusqu'à ce qu'un Pokémon soit vaincu."""
        while self.player_pokemon.is_alive() and self.computer_pokemon.is_alive():
            self.execute_turn()

        if self.player_pokemon.is_alive():
            print(f"{self.player_pokemon.name} a gagné !")
        else:
            print(f"{self.computer_pokemon.name} a gagné !")


    def get_random_computer_pokemon(self):
        """Retourne un Pokémon aléatoire pour l'ordinateur en utilisant l'API PokéAPI"""
        pokemon_id = random.randint(1, 151)  # Pokémon entre 1 et 151
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon_name = data["name"]  # Récupérer le nom du Pokémon
            return Pokemon(pokemon_name)  # Passer le nom du Pokémon au lieu de l'ID
        else:
            raise ValueError(f"Erreur lors de la récupération du Pokémon {pokemon_id}.")

    def handle_events(self, event):
        """Gérer les événements dans l'état de combat"""
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.player_attack()  # Attaque avec l'attaque 1 du joueur
            elif event.key == pygame.K_2:
                self.player_attack()  # Attaque avec l'attaque 2 du joueur

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if not self.selected_pokemon:
                self.select_pokemon(mouse_x, mouse_y)

            # Si le combat a commencé, gérer les clics sur les boutons
            if self.is_battle_started:
                self.check_button_clicks(mouse_x, mouse_y)

    def select_pokemon(self, mouse_x, mouse_y):
        """Sélectionne un Pokémon du joueur en fonction de la position du clic"""
        x_offset = 50  # Position de départ à gauche
        y_offset = 300  # Position verticale (en bas de l'écran)
        for i, pokemon in enumerate(self.player_pokemon):
            if x_offset + i * 150 <= mouse_x <= x_offset + i * 150 + 200 and y_offset <= mouse_y <= y_offset + 200:
                self.selected_pokemon = pokemon
                self.selected_pokemon.set_sprite("back_default")  # Mettre à jour le sprite du Pokémon sélectionné
                print(f"{pokemon.name} a été sélectionné.")
                #self.display_message(f"{pokemon.name} go")
                self.computer_pokemon = self.get_random_computer_pokemon()  # Choisir un Pokémon de l'ordinateur
                self.is_battle_started = True  # Le combat commence
                break

    def check_button_clicks(self, mouse_x, mouse_y):
        """Vérifie si un bouton a été cliqué pendant le combat"""
        if self.attack_button.is_clicked((mouse_x, mouse_y)):
            self.attack()
        elif self.defend_button.is_clicked((mouse_x, mouse_y)):
            self.defend()
        elif self.potion_button.is_clicked((mouse_x, mouse_y)):
            self.use_potion()
        elif self.give_up_button.is_clicked((mouse_x, mouse_y)):
            return self.give_up() # Appeler la méthode d'abandon

    def update(self):
        """Mettre à jour la logique du combat (si nécessaire)"""
        if self.is_battle_started:
        # Gérer les clics sur les boutons
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    next_state = self.check_button_clicks(mouse_x, mouse_y)
                    if next_state:
                        return next_state  # Retourner l'état "menu" si Give-Up est cliqué
        return None   

    def draw(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        if self.is_battle_started:
            # Dessiner les Pokémon du joueur et de l'ordinateur
            self.selected_pokemon.draw(self.screen, 200, 400)
            self.computer_pokemon.draw(self.screen, 600, 210)

            # Afficher les barres de vie
            self.selected_pokemon.draw_health_bar(self.screen, 200, 400)
            self.computer_pokemon.draw_health_bar(self.screen, 600, 210)

            self.display_moves()
            # Afficher les boutons de combat
            self.show_battle_buttons()
            # Dessiner le bouton "Give Up"
            self.give_up_button.draw(self.screen)
        else:
            self.display_pokemon_selection()
       
            # Si un cercle est en mouvement, on l'anime
        if self.is_defending and self.circle_pos:
            # Déplacer le cercle
            if self.circle_pos != self.circle_target:
                self.move_circle()
            # Dessiner le cercle
            pygame.draw.circle(self.screen, (0, 255, 0), self.circle_pos, self.circle_radius)


    def display_pokemon_selection(self):
        #Affiche tous les Pokémon du joueur pour la sélection"""
        x_offset = 50
        y_offset = 300
        for i, pokemon in enumerate(self.player_pokemon):
            pokemon.draw(self.screen, x_offset + i * 150, y_offset)
            pokemon_text = f"{pokemon.name} - Niveau {pokemon.level}"
        # Afficher un message de sélection
        message = "Choose your Pokémon for battle"
        message_surface = self.font.render(message, True, (255, 255, 255))
        message_width = message_surface.get_width()
        message_x = (SCREEN_WIDTH - message_width) // 2
        message_y = y_offset + 250
        self.screen.blit(message_surface, (message_x, message_y))

    def show_battle_buttons(self):
        """Afficher les boutons pendant le combat"""
        # Afficher les boutons de combat : Attaque, Défense, Potion
        self.attack_button.draw(self.screen)
        self.defend_button.draw(self.screen)
        self.potion_button.draw(self.screen)

    def attack(self):
        """Effectuer une attaque du joueur"""
        if self.computer_pokemon:
            damage = 10  # Exemple de dégâts
            self.computer_pokemon.take_damage(damage)
            print(f"{self.selected_pokemon.name} attaque {self.computer_pokemon.name} !")
            # Vérifie si le Pokémon adverse est à 0 PV
            #if self.computer_pokemon.hp <= 0:
                #print(f"{self.computer_pokemon.name} a été vaincu !")
                # Choisir un nouveau Pokémon pour l'ordinateur
            self.computer_pokemon = self.get_random_computer_pokemon()
            print(f"Un nouveau Pokémon de l'ordinateur a été choisi : {self.computer_pokemon.name}")

    def defend(self):
        """Logique pour la défense"""
        # Position du cercle et son rayon
        circle_position = (400, 300)  # Au centre de l'écran
        circle_radius = 50
        # Dessiner le cercle
        pygame.draw.circle(self.screen, RED, circle_position, circle_radius)
        print(f"{self.selected_pokemon.name} se défend !")
        move_url = "https://pokeapi.co/api/v2/move/tackle/"
        tackle = self.Move(move_url)
        print(tackle.name)  # Affiche "tackle"
        print(tackle.power)  # Affiche la puissance de l'attaque

    def use_potion(self):
        """Utiliser une potion"""
        print(f"Potion utilisée par {self.selected_pokemon.name} !")
        print(f" une potion")

    def give_up(self):
    #Logique pour abandonner le combat
        print(f"{self.selected_pokemon.name} a abandonné le combat !")
        self.is_battle_started = False  # Arrêter le combat
        self.selected_pokemon = None   # Réinitialiser le Pokémon sélectionné
        self.computer_pokemon = None   # Réinitialiser le Pokémon de l'ordinateur
        return "menu"  
    def display_moves(self):
        """Affiche les mouvements du Pokémon sélectionné pendant le combat"""
        if self.selected_pokemon:
            moves = self.selected_pokemon.get_moves()  # Récupérer les attaques
            for i, move in enumerate(moves):
                message = f"{i+1}: {move}"  # Afficher chaque mouvement avec un numéro
                message_surface = self.font.render(message, True, (255, 255, 255))
                self.screen.blit(message_surface, (50, 50 + (i * 40)))  # Afficher les attaques à un endroit défini

    """def display_message(screen, message):
    
        # draw a WHITE box with BLACK border
        pygame.draw.rect(screen, TRANSPARENT, (10, 350, 480, 140))
        pygame.draw.rect(screen, TRANSPARENT, (10, 350, 480, 140), 3)
        
        # display the message
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render(message, True, WHITE)  # color ok
        text_rect = text.get_rect()
        text_rect.x = 475
        text_rect.y = 410
        screen.blit(text, text_rect)
        
        pygame.display.update()"""
    def move_circle(self):
        """Déplacer le cercle sur une ligne droite entre start et target."""
        start_x, start_y = self.circle_start
        target_x, target_y = self.circle_target

        # Calculer la direction du mouvement (vecteur)
        direction_x = target_x - start_x
        direction_y = target_y - start_y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        
        # Normaliser le vecteur de direction
        direction_x /= distance
        direction_y /= distance

        # Déplacer le cercle en fonction de la vitesse
        self.circle_pos = (self.circle_pos[0] + direction_x * self.circle_speed,
                           self.circle_pos[1] + direction_y * self.circle_speed)

        # Si le cercle a atteint la cible, on arrête le mouvement
        if math.sqrt((self.circle_pos[0] - target_x) ** 2 + (self.circle_pos[1] - target_y) ** 2) < 5:
            self.is_defending = False  # Arrêter l'animation

    def defend(self):
        """Logique pour la défense (initier l'attaque par le cercle)."""
        print(f"{self.player_pokemon.name} se défend !")

        # Position de départ du cercle (Pokémon attaquant)
        self.circle_start = (200, 200)  # Position du joueur (ici, exemple fixe)

        # Position de la cible du cercle (Pokémon défenseur)
        self.circle_target = (400, 200)  # Position de l'adversaire (ici, exemple fixe)

        self.circle_pos = self.circle_start  # Initialisation de la position du cercle
        self.is_defending = True  # Commencer l'animation

    class Move:
        def __init__(self, url):
            # Appel à l'API pour récupérer les données de l'attaque
            req = requests.get(url)
            self.json = req.json()
            
            # Propriétés de l'attaque
            self.name = self.json["name"]
            self.power = self.json["power"]
            self.type = self.json["type"]["name"]
            