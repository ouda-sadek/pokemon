import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.states.menu import Menu 
from game.states.game import * 
from game.entities.buttonsounds import SoundToggle

def main():
    pygame.init()

    # Create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

    # The game starts with the menu
    current_state = Menu(screen)
    
    # Create sound toggle button
    sound_toggle = SoundToggle(screen)
    sound_toggle = SoundToggle(screen, pos=(SCREEN_WIDTH - 150, 10))  # Ajuste la position
    
    # Main loop
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Event handling current state
            current_state.handle_events(event)
            sound_toggle.handle_event(event)  # Handle sound button events

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
        sound_toggle.draw()  # Draw sound button
        pygame.display.flip()

    # Exit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
