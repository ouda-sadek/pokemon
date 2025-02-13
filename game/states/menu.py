import pygame
import os
from pygame.locals import *
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from config import * 

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)
        self.buttons = self.create_menu_buttons()
        self.background = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/images/background2.jpg"))
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.submenu = None
        self.next_state = None

    def create_menu_buttons(self):
        button_width = MENU_BUTTON_WIDTH
        button_height = MENU_BUTTON_HEIGHT
        new_game_x = 120
        new_game_y = 170
        continue_x= 900
        continue_y = 170
        add_pokemon_x = 110
        add_pokemon_y = 500
        pokedex_x = continue_x
        pokedex_y = add_pokemon_y
        exit_x= 550
        exit_y = 550

        new_game_text, new_game_rect, new_game_button = self.create_button("New Game", self.font, new_game_x + button_width // 2, new_game_y + button_height // 2)
        continue_text, continue_rect, continue_button = self.create_button("Continue", self.font, continue_x + button_width // 2, continue_y + button_height // 2)
        add_pokemon_text, add_pokemon_rect, add_pokemon_button = self.create_button("Add Pokemon", self.font, add_pokemon_x + button_width // 2, add_pokemon_y + button_height // 2)
        pokedex_text,pokedex_rect, pokedex_button = self.create_button("Pokedex", self.font, pokedex_x + button_width // 2, pokedex_y + button_height // 2)
        exit_text,exit_rect, exit_button = self.create_button("Exit", self.font, exit_x + button_width // 2, exit_y + button_height // 2)

        buttons = {
            "New Game": (new_game_text, new_game_rect, new_game_button),
            "Continue": (continue_text, continue_rect, continue_button),
            "Setting": (add_pokemon_text, add_pokemon_rect, add_pokemon_button),
            "Pokedex": (pokedex_text, pokedex_rect, pokedex_button),
            "Exit": (exit_text, exit_rect, exit_button)
        }
        return buttons

    def create_button(self, text, font, x, y):
        text_surface = font.render(text, True, MENU_BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x, y))
        button_rect = text_rect.inflate(MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        return text_surface, text_rect, button_rect

    def draw_button(self, text_surface, text_rect, button_rect, color):
        pygame.draw.rect(self.screen, color, button_rect, border_radius=100)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for name, (_,_, button_rect) in self.buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    self.next_state = name.lower()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for name, (text, rect, button_rect) in self.buttons.items():
            if button_rect.collidepoint(mouse_pos):
                color = MENU_BUTTON_HOVER_COLOR
            else:
                color = MENU_BUTTON_COLOR
            self.draw_button(text, rect, button_rect, color)
        return self.next_state   if hasattr(self, 'next_state') else None

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.submenu:
            self.submenu.draw()
        else:
            for text_surface, text_rect, button_rect in self.buttons.values():
                self.draw_button(text_surface, text_rect, button_rect, MENU_BUTTON_COLOR)