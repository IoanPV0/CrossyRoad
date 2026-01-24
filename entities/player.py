import pygame
from utils.coords import world_to_screen
from constants import GRID_WIDTH, TILE_SIZE

class Player:
    def __init__(self):
        self.grid_x = 6
        self.grid_y = 5
        self.color = (250, 250, 250)
        self.angle = 0

    def move(self, dx, dy, world):
        if dx == 1:
            self.angle = -90
        elif dx == -1:
            self.angle = 90
        elif dy == 1:
            self.angle = 0
        elif dy == -1:
            self.angle = 180

        next_x = self.grid_x + dx
        next_y = self.grid_y + dy

        next_x = world.snap_player_x(next_x, next_y)


        if 0 <= next_x < GRID_WIDTH and not world.is_grass_obstacle(next_x, next_y):
            self.grid_x = next_x
            self.grid_y = next_y

    def draw(self, screen, camera_y):
        px, py = world_to_screen(self.grid_x, self.grid_y, camera_y)

        chicken_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        # corps
        rect = pygame.Rect(17, 17, 30, 30)
        pygame.draw.rect(chicken_surf, self.color, rect, border_radius=4)
        
        # ailes
        pygame.draw.rect(chicken_surf, (220, 220, 220), (13, 22, 4, 20), border_radius=2)
        pygame.draw.rect(chicken_surf, (220, 220, 220), (47, 22, 4, 20), border_radius=2)

        # tête
        pygame.draw.rect(chicken_surf, (255, 0, 0), (29, 20, 6, 10), border_radius=2)

        # bec
        pygame.draw.rect(chicken_surf, (255, 200, 0), (27, 12, 10, 6), border_radius=2)

        rotated_surf = pygame.transform.rotate(chicken_surf, self.angle)
        new_rect = rotated_surf.get_rect(center=(px + TILE_SIZE // 2, py + TILE_SIZE // 2))
        screen.blit(rotated_surf, new_rect)
