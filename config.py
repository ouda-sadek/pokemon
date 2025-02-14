import pygame

pygame.init()
pygame.mixer.init()


# Screen dimensions
SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 625

# Colors General
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS General
FPS = 60

# Speed


# Latence Time


# Way to folders
IMAGE_FOLDER = "./pokemon/assets/Images/"
SOUND_FOLDER = "./pokemon/assets/sounds/"
FONT_FOLDER = "./pokemon/assets/font/"

# Grab musics
MUSIC_MENU = pygame.mixer.Sound(SOUND_FOLDER + r"menu.mp3")
MUSIC_FIGHT = pygame.mixer.Sound(SOUND_FOLDER + r"fight.mp3")
MUSIC_ATTACK = pygame.mixer.Sound(SOUND_FOLDER + r"attack.mp3")
MUSIC_END_GAME = pygame.mixer.Sound(SOUND_FOLDER + r"end_game.mp3")