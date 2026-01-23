import pygame

from constants import *
from grid.world import World
from entities.player import Player
from utils.camera import Camera

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moteur Crossy Road")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
high_score = 0
score = 0
max_y = 5


def reset_game():
    global world, player, camera, game_started, score, max_y
    world = World()
    player = Player()
    camera = Camera(scroll_speed=30)
    game_started = False
    score = 0
    max_y = 5
reset_game()
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            game_started = True
            if event.key == pygame.K_UP:
                player.move(0, 1, world)
                if player.grid_y > max_y:
                    score += 1
                    max_y = player.grid_y
                    if score > high_score:
                        high_score = score
            elif event.key == pygame.K_DOWN:
                player.move(0, -1, world)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0, world)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0, world)

    if game_started:
        camera.update(dt, player)
        if world.update_player_log_movement(player, dt, camera.y):
            reset_game()
        if world.check_collisions(player, camera.y):
            reset_game()
    world.update(camera.y, dt)

    screen.fill((20, 20, 20))
    world.draw(screen, camera.y)
    player.draw(screen, camera.y)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"Best: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    screen.blit(high_score_text, (20, 60))
    pygame.display.flip()

pygame.quit()
