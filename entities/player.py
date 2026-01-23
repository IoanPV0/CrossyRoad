import pygame
from utils.coords import world_to_screen
class Player:
    def __init__(self):
        self.grid_x = 5
        self.grid_y = 5
        self.color = (250, 250, 250)

    def move(self, dx, dy):
        self.grid_x = max(1, min(9, self.grid_x + dx))
        self.grid_y += dy

    def draw(self, screen, camera_y):
        px, py = world_to_screen(self.grid_x, self.grid_y, camera_y)

        rect = pygame.Rect(px + 8, py + 8, 48, 48)
        pygame.draw.rect(screen, self.color, rect)
