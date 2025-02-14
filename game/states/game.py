def end_game_display(self):
    # Afficher le gagnant et le perdant
    if "gagnant" == "Bot":
        print("Vous avez perdu !")
        self.transfer_to_winner()
        
    elif "gagnant" == "Joueur":
        print("Vous avez gagné !")
        self.transfer_to_winner()

def transfer_to_winner(self):
    # Transférer les pokémons perdant vers la collection du gagnant
    if "gagnant" == "Bot":
        # Affichage des pokémon perdus ou gagné
        """Pokémon Perdu : 3 pokémons utilisés"""
        """pokemon utilisés à nous --> pokemon collection du bot"""
        """retirer les pokémon utilisés perdus de notre collection"""
        
    elif "gagnant" == "Joueur":
        # Affichage des pokémon perdus ou gagné
        """Pokémon ajouté à la collection : 3 pokémons utilisés par le bot"""
        """pokemon utilisés du bot --> pokemon collection à nous"""