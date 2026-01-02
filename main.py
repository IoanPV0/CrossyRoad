import pygame

from constants import *
from grid.world import World
from entities.player import Player
from utils.camera import Camera

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Road – Base saine")
clock = pygame.time.Clock()

world = World()
player = Player()
camera = Camera(scroll_speed=30)

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, 1)
            elif event.key == pygame.K_DOWN:
                player.move(0, -1)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)

    camera.update(dt, player)
    world.update(camera.y)

    screen.fill((20, 20, 20))
    world.draw(screen, camera.y)
    player.draw(screen, camera.y)

    pygame.display.flip()

pygame.quit()
