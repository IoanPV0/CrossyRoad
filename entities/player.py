import pygame
from utils.coords import world_to_screen
from constants import GRID_WIDTH

class Player:
    def __init__(self):
        self.grid_x = 6
        self.grid_y = 5
        self.color = (250, 250, 250)

    def move(self, dx, dy, world):
        next_x = self.grid_x + dx
        next_y = self.grid_y + dy

        next_x = world.snap_player_x(next_x, next_y)


        if 0 <= next_x < GRID_WIDTH and not world.is_grass_obstacle(next_x, next_y):
            self.grid_x = next_x
            self.grid_y = next_y

    def draw(self, screen, camera_y):
        px, py = world_to_screen(self.grid_x, self.grid_y, camera_y)

        rect = pygame.Rect(px + 17, py + 17, 30, 30)
        pygame.draw.rect(screen, self.color, rect)
