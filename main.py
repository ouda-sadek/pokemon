import pygame
from config import *
#from game.states.menu import Menu

# The main function that runs the game
def main():

    # Initialize pygame
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Game")

    """menu = Menu(screen)
    menu.display_menu()"""

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
