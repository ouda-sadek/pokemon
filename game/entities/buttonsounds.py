import pygame
import os

class SoundToggle:
    def __init__(self, screen, pos=(50, 50)):
        self.screen = screen
        self.pos = pos
        self.sound_on = True
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # Récupère le dossier du script
        IMAGE_PATH_ON = os.path.join(BASE_PATH, "../../assets/images/sound_on.png")
        IMAGE_PATH_OFF = os.path.join(BASE_PATH, "../../assets/images/sound_off.png")
        self.image_on = pygame.image.load(IMAGE_PATH_ON)
        self.image_off = pygame.image.load(IMAGE_PATH_OFF)
        new_size = (200, 150)  # Taille souhaitée (largeur, hauteur)

        self.image_on = pygame.transform.scale(self.image_on, new_size)
        self.image_off = pygame.transform.scale(self.image_off, new_size)
        self.rect = self.image_on.get_rect(topleft=pos)
    
    def toggle_sound(self):
        self.sound_on = not self.sound_on
        if self.sound_on:
            pygame.mixer.music.set_volume(1)
        else:
            pygame.mixer.music.set_volume(0)
    
    def draw(self):
        if self.sound_on:
            self.screen.blit(self.image_on, self.pos)
        else:
            self.screen.blit(self.image_off, self.pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.toggle_sound()
