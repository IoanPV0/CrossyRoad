import pygame
from utils.coords import world_to_screen
from constants import TILE_SIZE

class Tile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.useable = True

    def draw(self, screen, camera_y):
        px, py = world_to_screen(self.x, self.y, camera_y)

        rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        #contour
        #pygame.draw.rect(screen, (40, 40, 40), rect, 2)
