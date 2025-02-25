import pygame
import sys
from game.states.menu import Menu
from game.entities.buttonsounds import SoundToggle
from game.states.fight import Fight

#from game.entities.pokedex import PokedexVisible
from config import *



def main():
    
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Game")
    clock = pygame.time.Clock()
    # Initialisation des Pokémon
    sound_toggle = SoundToggle(screen, pos=(SCREEN_WIDTH - 150, 10))  # Ajuste la position
    # Initialiser ton APIManager (si nécessaire)
    """api_manager = APIManager(use_offline_data=False) 
    api_manager.save_data_locally()  """
    current_state = Menu(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            current_state.handle_events(event)
            sound_toggle.handle_event(event)  # Handle sound button events

        next_state = current_state.update()
        if next_state:
            if next_state == "menu":
                current_state = Menu(screen)
            elif next_state == "new game":
                current_state = Fight(screen)
            elif next_state == "give_up":
                current_state = Menu(screen) 
            elif next_state == "pokedex":
                current_state = PokedexVisible(screen)
            elif next_state == "continue":
                current_state = Menu(screen)
            else:
                raise ValueError(f"Invalid next state: {next_state}")

        # Dessiner les autres éléments comme les boutons de son et le menu
        current_state.update()
        current_state.draw()
        sound_toggle.draw()  # Dessiner le bouton de son
        
        pygame.display.flip()  # Actualiser l'écran
        clock.tick(60)  # Limiter la boucle à 60 images par seconde
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
