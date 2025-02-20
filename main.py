"""import pygame
from config import *
#from game.states.menu import Menu

# The main function that runs the game
def main():

    # Initialize pygame
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

    menu = Menu(screen)
    menu.display_menu()

    # Main loop
    running = True
    while running:
    # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Exit pygame
pygame.quit()

if __name__ == "__main__":
    main()
"""
####################################################
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.states.menu import Menu  # Assure-toi que ce module existe

# The main function that runs the game
def main():
    # Initialize pygame
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

    # Initialize the clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Initialize the game state (e.g., Menu)
    current_state = Menu(screen)

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass the event to the current state
            current_state.handle_event(event)

        # Update the current state
        current_state.update()

        # Render the current state
        screen.fill((0, 0, 0))  # Clear the screen with black (or any other color)
        current_state.render(screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    # Exit pygame
    pygame.quit()

if __name__ == "__main__":
    main()