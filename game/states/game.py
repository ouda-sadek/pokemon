import pygame

# Initialize pygame
pygame.init()
# Set up the window
screen = pygame.display.set_mode((1150, 625))
pygame.display.set_caption("Pokémon Game")


font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to display text
def text_display(text, x, y, color):
    text_render=font.render(text,True,color)
    screen.blit(text_render,(x,y))



def end_game_display():
    # Afficher le gagnant et le perdant
    if gagnant == "Joueur":
        text_display("Vous avez gagné !", 930/2, 625/2, WHITE)
        transfer_to_winner()
    elif gagnant == "Bot":
        text_display("Vous avez perdu...", 930/2, 625/2, WHITE)
        transfer_to_winner()
    pygame.display.flip()

# Transférer les pokémons perdant vers la collection du gagnant
def transfer_to_winner():
    if gagnant == "Joueur":
        # Affichage des pokémon perdus ou gagné
        """Pokémon ajouté à la collection : 3 pokémons utilisés par le bot"""
        text_display("Pokémons ajoutés à la collection :")
        for pokemon in "pokemon_collection_bot":
            """display pokemons"""
        """pokemon utilisés du bot --> pokemon collection à nous"""
    elif gagnant == "Bot":
        # Affichage des pokémon perdus ou gagné
        """Pokémon Perdu : 3 pokémons utilisés"""
        text_display("Pokémons perdus :")
        for pokemon in "pokemon_collection":
            """display pokemons"""
        """pokemon utilisés à nous --> pokemon collection du bot"""
        """retirer les pokémon utilisés perdus de notre collection"""
    




# Main loop
running = True
while running:
# Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        gagnant = "Joueur"
        end_game_display()