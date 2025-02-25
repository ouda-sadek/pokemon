# game/button.py
import pygame

class ButtonFight:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.action = action  # Action à effectuer lors du clic sur le bouton
        self.hover = False

    def draw(self, screen):
        # Détection de survol du bouton
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.hover = True
        else:
            self.hover = False

        # Dessiner le bouton avec la couleur appropriée (normal ou survol)
        button_color = self.hover_color if self.hover else self.color
        pygame.draw.rect(screen, button_color, self.rect, border_radius=10)  # Ajouter un rayon pour arrondir les coins

        # Dessiner le texte sur le bouton
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # Texte en blanc
        text_rect = text_surface.get_rect(center=self.rect.center)  # Centrer le texte dans le bouton
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        """Vérifier si le bouton a été cliqué."""
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()  # Appeler l'action associée au bouton
            return True
        return False
