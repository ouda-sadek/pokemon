import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.states.menu import Menu 
from game.states.game import * 


def main():
    pygame.init()

    # creat window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

   # The game starts with the menu
    current_state = Menu(screen)
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Event handling current statecd
            current_state.handle_events(event)

        # Update current state
        next_state = current_state.update()
        
        # If state changed
        if next_state:
            if next_state == "menu":
                current_state = Menu(screen)
            elif next_state == "New Game":
                current_state = (screen)
            elif next_state == "exit":
                running = False
            elif next_state == "Continue":
                pass
            else:
                raise ValueError(f"Invalid next state: {next_state}")
                    
            
        current_state.update()    
        # Draw current state
        current_state.draw()
        pygame.display.flip()

        
    
    # Exit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main() 
