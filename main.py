import pygame

from constants import *
from grid.world import World
from entities.player import Player
from utils.camera import Camera
from utils.coords import world_to_screen
from entities.eagle import Eagle

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Road 2D")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
high_score = 0
score = 0
max_y = 5


def reset_game():
    global world, player, camera, game_started, score, max_y, eagle
    world = World()
    player = Player()
    camera = Camera(scroll_speed=30)
    eagle = Eagle()
    camera.x = player.grid_x * TILE_SIZE - (SCREEN_WIDTH / 2 - TILE_SIZE / 2)
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

        if event.type == pygame.KEYDOWN and not eagle.active:
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
                if player.grid_x > 2:
                    player.move(-1, 0, world)
            elif event.key == pygame.K_RIGHT:
                if player.grid_x < GRID_WIDTH - 3:
                    player.move(1, 0, world)

    camera_pos = (camera.x, camera.y)
    if game_started:
        if not eagle.active:
            # gestion camera
            camera.update(dt, player)
            camera_pos = (camera.x, camera.y)

            #gestion aigle
            px, py = world_to_screen(player.grid_x, player.grid_y, camera_pos)
            if py > SCREEN_HEIGHT - TILE_SIZE * 2: # marge de 1 tile
                eagle.trigger(px, py)
            
            if world.update_player_log_movement(player, dt, camera_pos):
                reset_game()
            if world.check_collisions(player, camera_pos):
                reset_game()
        else:
            if eagle.update(dt):
                reset_game()
    world.update(camera.y, dt)
    screen.fill((20, 20, 20))
    world.draw(screen, camera_pos)
    if not eagle.has_caught_player:
        player.draw(screen, camera_pos)
    eagle.draw(screen)

    #affichage score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"Best: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    screen.blit(high_score_text, (20, 60))
    pygame.display.flip()

pygame.quit()
