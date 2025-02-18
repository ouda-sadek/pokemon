import pygame
import os
from pygame.locals import *
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from config import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        pygame.mixer.init()  # Initialiser le module audio

        self.hover_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "../../assets/sounds/menu_hover.wav"))
        self.click_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "../../assets/sounds/button_click.mp3"))
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "../../assets/sounds/balloon_game.mp3"))
        pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

        base_path = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_path, "..", "..", "assets", "fonts", "pokemon1.ttf")
        font_path = os.path.normpath(font_path)
        self.font = pygame.font.Font(font_path, MENU_FONT_SIZE)  
        self.buttons = self.create_menu_buttons()  
        self.background = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/images/background2.jpg"))
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.next_state = None

        # Dictionary to track the properties of each button (color + size)
        self.button_states = {
            name: {
                "color": MENU_BUTTON_COLOR,
                "scale": 1.0  # Button zoom factor (1.0 = normal size)
            }
            for name in self.buttons
        }

    def create_menu_buttons(self):
        button_width = MENU_BUTTON_WIDTH
        button_height = MENU_BUTTON_HEIGHT

        button_positions = {
            "New Game": (120, 170),
            "Continue": (900, 170),
            "Add Pokemon": (110, 500),
            "Pokedex": (900, 500),
            "Exit": (550, 550)
        }

        buttons = {}
        for name, (x, y) in button_positions.items():
            text_surface, text_rect, button_rect = self.create_button(name, self.font, x + button_width // 2, y + button_height // 2)
            buttons[name] = (text_surface, text_rect, button_rect)

        return buttons

    def create_button(self, text, font_, x, y):
        text_surface = font_.render(text, True, MENU_BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x, y))
        button_rect = text_rect.inflate(MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        return text_surface, text_rect, button_rect

    def draw_button(self, text_surface, text_rect, button_rect, color, scale):
        """Draw a button with a zoom effect"""
        scaled_rect = button_rect.inflate(int(button_rect.width * (scale - 1)), int(button_rect.height * (scale - 1)))
        pygame.draw.rect(self.screen, color, scaled_rect, border_radius=100)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for name, (_, _, button_rect) in self.buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    self.click_sound.play()
                    self.next_state = name.lower()

    def update(self):
        """ Updates the hover effect with a smooth transition """
        mouse_pos = pygame.mouse.get_pos()
        for name, (text, rect, button_rect) in self.buttons.items():
            if button_rect.collidepoint(mouse_pos):
                # Apply gradual color and zoom transition
                self.button_states[name]["color"] = self.lerp_color(self.button_states[name]["color"], MENU_BUTTON_HOVER_COLOR, 0.1)
                self.button_states[name]["scale"] = self.lerp(self.button_states[name]["scale"], 1.1, 0.1)
                self.hover_sound.play()
            else:
                # Gradually return to normal color and size
                self.button_states[name]["color"] = self.lerp_color(self.button_states[name]["color"], MENU_BUTTON_COLOR, 0.1)
                self.button_states[name]["scale"] = self.lerp(self.button_states[name]["scale"], 1.0, 0.1)

        return self.next_state if hasattr(self, 'next_state') else None

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for name, (text_surface, text_rect, button_rect) in self.buttons.items():
            color = self.button_states[name]["color"]
            scale = self.button_states[name]["scale"]
            self.draw_button(text_surface, text_rect, button_rect, color, scale)

    def lerp(self, start, end, speed):
        """ Linear interpolation for a smooth transition """
        return start + (end - start) * speed

    def lerp_color(self, start_color, end_color, speed):
        """ Linear interpolation for smooth color transition """
        return tuple(int(start + (end - start) * speed) for start, end in zip(start_color, end_color))
