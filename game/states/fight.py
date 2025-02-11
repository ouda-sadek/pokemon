# Game Logic (PlayerVSBot)
# 3 pokemons in each sides
import random
import json

# Récuperer les 6 pokémons du Joueur et du Bot (par l'autre fichier)
"""pokemon_player = ...."""
# Joindre le fichier json
file_pokemon = '/data/pokemon.json'


# Classe qui Check la vie du pokémon, et qui remplace le pokemon KO par celui du 'banc' ou game_over si aucun pokemon dispo
class Check:
    def __init__(self, vie):
        self.vie = vie
        self.etat = True    # True=En vie, False=KO
        self.game_over = False   # False=Jouer, True=Jeu Fini

    # Méthode pour vérifier la vie
    def life_check(self):
        if self.vie > 0:    # Encore des HP/PV
            return "Pokemon encore en vie, c'est à son tour"
        else:   # 0 PV, Pokémon KO
            self.etat = False
            self.replace_pokemon_ko()   # Remplacer le pokemon
    
    # Méthode pour remplacer le pokémon KO par un pokemon du banc
    def replace_pokemon_ko(self):
        # Lire le stock de pokémon, si il en reste en vie :
        """Choisir un pokémon disponible avec de la vie"""
        """Echanger le pokémon actif par le pokémon du banc"""
        """Le pokémon 'rangé' n'est plus utilisable mais reste encore au joueur/bot"""
        """Au tour du pokémon vainqueur précédemment"""

        # Lire le stock de pokémon, si il n'en reste aucun avec de la vie :
        if not self.vie > 0 in """Si aucuns pokémon ont de la vie""":
            self.game_over = True
            """Affichage screen de win/loose"""
            """Retour au menu après 3000ms"""


class Fight:
    def __init__(self):
        self.pokemon_player_active = random.choice("""Dans la liste des pokémons du joueur""")
        self.pokemon_bot_active = random.choice("""Dans la liste des pokémons du bot""")
        self.pokemon_tour = "Player"


    # Méthode qui choisi le premier pokémon a jouer avec la vitesse
    def first_tour(self):
        with open(file_pokemon, 'r') as f:
            json.load(f)

            if self.pokemon_player_active.speed > self.pokemon_bot_active.speed:    # Vitesse du pokemon player est plus grand
                return
            elif self.pokemon_bot_active.speed > self.pokemon_player_active.speed:      # Vitesse du pokemon bot est plus grand
                self.pokemon_tour =  "Bot"
                return self.pokemon_tour


    # Méthode pour executé l'attaque d'un pokémon à l'autre
    def attack(self):
        if self.pokemon_tour == "Player":
            # Probabilité que l'attaque rate est de 20%
            if random.random() < 0.2:
                self.pokemon_tour =  "Bot"
                return "Attaque raté"
            else:
                # Attaque du pokemon player --> bot
                degats_net = self.pokemon_player_active.attack * self.pokemon_player_active.multiplier - self.pokemon_bot_active.resistance
                self.pokemon_bot_active.vie -= degats_net
                print(f"Dégats infligés : {degats_net}")
                return self.pokemon_bot_active.vie  # Vie de la victime après dégâts infligés

        elif self.pokemon_tour == "Bot":
            # Probabilité que l'attaque rate est de 20%
            if random.random() < 0.2:
                self.pokemon_tour =  "Player"
                return "Attaque raté"
            else:
                # Attaque du pokemon bot --> player
                degats_net = self.pokemon_bot_active.attack * self.pokemon_bot_active.multiplier - self.pokemon_player_active.resistance
                self.pokemon_player_active.vie -= degats_net
                print(f"Dégats infligés : {degats_net}")
                return self.pokemon_player_active.vie  # Vie de la victime après dégâts infligés


    # Méthode pour transferer les 3 pokémons perdants vers la main du vainqueur (+ reset health to 100HP)
    def transfert_pokemon_to_winner(self):
        # A la fin du jeu, le gagnant gagne les pokémons de l'adversaire
        pass