from grid.lane import GrassLane, LogLane, LilypadLane, TrainLane, CarLane
from random import randint, choice
from constants import GRID_WIDTH, TILE_SIZE
from utils.coords import world_to_screen
import pygame

class World:
    def __init__(self):
        self.lanes = []
        self.generate_initial()

    def generate_initial(self):
        # Premieres voies = que des arbres (spawn)
        for y in range(3):
            self.lanes.append(GrassLane(y, full_of_trees=True))


        # Les 3 voies suivantes GrassLane avec arbres sur les cotes (spawn 2)
        for y in range(3, 7):
            if y == 5:
               self.lanes.append(GrassLane(y, forbidden_indices=[6]))
            else:
                self.lanes.append(GrassLane(y))


        for y in range(7, 15):
            choices = [GrassLane, LogLane, LilypadLane, TrainLane, CarLane]
            # Pas plus de 2 lignes de nénuphars a la suite
            if len(self.lanes) >= 2 and isinstance(self.lanes[-1], LilypadLane) and isinstance(self.lanes[-2], LilypadLane):
                choices.remove(LilypadLane)
            
            lane_type = choice(choices)
            
            if lane_type in [LilypadLane, GrassLane, CarLane] and self.lanes:
                self.lanes.append(lane_type(y, previous_lane=self.lanes[-1]))
            else:
                self.lanes.append(lane_type(y))

    def update(self, camera_y, dt):
        while self.lanes[-1].y * 64 - camera_y < 640:
            new_y = self.lanes[-1].y + 1
            choices = [GrassLane, LogLane, LilypadLane, TrainLane, CarLane]
            # Pas plus de 2 lignes de nénuphars a la suite
            if len(self.lanes) >= 2 and isinstance(self.lanes[-1], LilypadLane) and isinstance(self.lanes[-2], LilypadLane):
                choices.remove(LilypadLane)

            lane_type = choice(choices)
            if lane_type in [LilypadLane, GrassLane, CarLane]:
                self.lanes.append(lane_type(new_y, previous_lane=self.lanes[-1]))
            else:
                self.lanes.append(lane_type(new_y))

        self.lanes = [
            lane for lane in self.lanes
            if lane.y * 64 - camera_y < 700
        ]

        # update pour chaque voie
        for lane in self.lanes:
            lane.update(dt)

    def draw(self, screen, camera_y):
        for lane in self.lanes:
            lane.draw(screen, camera_y)

    def is_grass_obstacle(self, x, y):
        for lane in self.lanes:
            if lane.y == y:
                if isinstance(lane, GrassLane):
                    for obs in lane.obstacles:
                        if obs[0] == x:
                            return True
                return False
        return False

    def update_player_log_movement(self, player, dt, camera_y):
        # Joueur emporté par la buche
        px, py = world_to_screen(player.grid_x, player.grid_y, camera_y)
        player_rect = pygame.Rect(px + 8, py + 8, 48, 48)

        for lane in self.lanes:
            if lane.y == player.grid_y:
                speed = lane.get_speed(player_rect, camera_y)
                if speed != 0:
                    player.grid_x += speed * dt
                    
                    # verif joueur sort de lecran
                    if player.grid_x < 2 or player.grid_x > GRID_WIDTH - 2:
                        return True
        return False

    def check_collisions(self, player, camera_y):
        # Le joueur est un carre pour les collisions
        px, py = world_to_screen(player.grid_x, player.grid_y, camera_y)
        player_rect = pygame.Rect(px + 8, py + 8, 48, 48)

        for lane in self.lanes:
            if lane.y == player.grid_y:
                return lane.check_collision(player_rect, camera_y)
        return False
    #Fonction servant a aligner le joueur sur les buches ou la grid (pas dentre 2)
    def snap_player_x(self, x, y):
        for lane in self.lanes:
            if lane.y == y:
                if isinstance(lane, LogLane):
                    # Alignement buches
                    for log in lane.logs:
                        log_x, length = log
                        if log_x - 0.5 <= x <= log_x + length - 0.5:
                            # On s'aligne sur la section de la buche (offset entier)
                            return log_x + round(x - log_x)
                    # Si pas de bûche on s'aligne sur la grille (noyade)
                    return round(x)
                else:
                    # pour toutes les autres voies on s'aligne sur la grille
                    return round(x)
        return round(x)