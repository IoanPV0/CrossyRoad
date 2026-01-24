import pygame
from constants import SCREEN_HEIGHT

class Eagle:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.target_y = 0
        self.speed = 1200 # Vitesse de l'aigle (pixels/s)
        self.has_caught_player = False

    def trigger(self, target_x, target_y):
        self.active = True
        self.x = target_x
        self.y = -200 # Commence bien au-dessus de l'écran
        self.target_y = target_y
        self.has_caught_player = False

    def update(self, dt):
        if not self.active:
            return False

        if not self.has_caught_player:
            # Phase 1 : Descente en piqué
            self.y += self.speed * dt
            if self.y >= self.target_y:
                self.y = self.target_y
                self.has_caught_player = True
        else:
            # Phase 2 : Remontée avec le joueur
            self.y -= self.speed * dt
            if self.y < -200:
                return True # Animation terminée
        return False

    def draw(self, screen):
        if not self.active:
            return
        
        # Dessin de l'aigle (forme simplifiée)
        pygame.draw.rect(screen, (100, 50, 10), (self.x - 60, self.y - 10, 160, 20)) # Ailes
        pygame.draw.rect(screen, (139, 69, 19), (self.x - 20, self.y - 20, 80, 50))  # Corps
        pygame.draw.rect(screen, (255, 255, 255), (self.x + 10, self.y + 10, 30, 20)) # Tête
        pygame.draw.rect(screen, (255, 215, 0), (self.x + 25, self.y + 20, 15, 10))   # Bec
        
        if self.has_caught_player:
            # Dessiner le "joueur" capturé dans les serres (carré blanc)
            pygame.draw.rect(screen, (250, 250, 250), (self.x + 8, self.y + 30, 48, 48))
