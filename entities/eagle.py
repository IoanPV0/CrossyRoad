import pygame
from constants import SCREEN_HEIGHT

class Eagle:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.target_y = 0
        self.speed = 1200
        self.has_caught_player = False

    def trigger(self, target_x, target_y):
        self.active = True
        self.x = target_x
        self.y = -200 # au dessus de lecran
        self.target_y = target_y
        self.has_caught_player = False

    def update(self, dt):
        if not self.active:
            return False

        if not self.has_caught_player:
            # descente vers le joueur
            self.y += self.speed * dt
            if self.y >= self.target_y:
                self.y = self.target_y
                self.has_caught_player = True
        else:
            # remontée avec joueur
            self.y -= self.speed * dt
            if self.y < -200:
                return True # fin animation  - exit
        return False

    def draw(self, screen):
        if not self.active:
            return
        #Dessin aigle
        pygame.draw.rect(screen, (100, 50, 10), (self.x - 60, self.y - 10, 160, 20)) # Ailes
        pygame.draw.rect(screen, (139, 69, 19), (self.x - 20, self.y - 20, 80, 50))  # Corps
        pygame.draw.rect(screen, (255, 255, 255), (self.x + 10, self.y + 10, 30, 20)) # Tête
        pygame.draw.rect(screen, (255, 215, 0), (self.x + 25, self.y + 20, 15, 10))   # Bec
        
        if self.has_caught_player:
            px = self.x
            py = self.y + 10
            # dessin joueur (poulet)
            pygame.draw.rect(screen, (250, 250, 250), (px + 17, py + 17, 30, 30), border_radius=4)
            pygame.draw.rect(screen, (220, 220, 220), (px + 13, py + 22, 4, 20), border_radius=2)
            pygame.draw.rect(screen, (220, 220, 220), (px + 47, py + 22, 4, 20), border_radius=2)
            pygame.draw.rect(screen, (255, 0, 0), (px + 29, py + 20, 6, 10), border_radius=2)
            pygame.draw.rect(screen, (255, 200, 0), (px + 27, py + 12, 10, 6), border_radius=2)