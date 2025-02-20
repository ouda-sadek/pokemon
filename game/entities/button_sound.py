import pygame
from pygame.locals import *
from config import *
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class BoutonMuteSound:
    def __init__(self):
        self.music_status = True    # Music ON / False = Music OFF

        self.logo_sound_on = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/images/sound_on.png"))
        self.logo_sound_off = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/images/sound_off.png"))
        self.logo_sound_on = pygame.transform.scale(IMAGE_FOLDER + "sound_on.png", (50, 50))
        self.logo_sound_off = pygame.transform.scale(IMAGE_FOLDER + "sound_off.png", (50, 50))

        #self.button_rect = logo_sound_on
        self.rect = self.button_rect.get_rect(topleft=(1000, 10))

    def display_button(self, screen):
        screen.blit(self.button_rect, self.rect.topleft)

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("APPUI")
                self.turn_sound()

    def turn_sound(self):
        if self.music_status:   # Pause --> Music OFF
            pygame.mixer.music.set_volume(0)
            self.music_status = False
            self.button_rect = self.logo_sound_off
            print(self.music_status)
        else:
            pygame.mixer.music.set_volume(1)
            self.music_status = True    # Resume --> Music ON
            self.button_rect = self.logo_sound_on
            print(self.music_status)