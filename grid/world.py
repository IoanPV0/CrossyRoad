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
        # 1. Les 2 voies du bas (0, 1) : GrassLane pleines d'arbres
        for y in range(3):
            self.lanes.append(GrassLane(y, full_of_trees=True))


        # 2. Les 3 voies suivantes (2, 3, 4) : GrassLane avec arbres sur les côtés
        for y in range(3, 7):
            if y == 5:
               self.lanes.append(GrassLane(y, forbidden_indices=[6]))
            else:
                self.lanes.append(GrassLane(y))


        for y in range(7, 15):
            choices = [GrassLane, LogLane, LilypadLane, TrainLane, CarLane]
            # Pas plus de 2 lignes de nénuphars à la suite
            if len(self.lanes) >= 2 and isinstance(self.lanes[-1], LilypadLane) and isinstance(self.lanes[-2], LilypadLane):
                choices.remove(LilypadLane)
            
            lane_type = choice(choices)
            
            if lane_type in [LilypadLane, GrassLane] and self.lanes:
                self.lanes.append(lane_type(y, previous_lane=self.lanes[-1]))
            else:
                self.lanes.append(lane_type(y))

    def update(self, camera_y, dt):
        while self.lanes[-1].y * 64 - camera_y < 640:
            new_y = self.lanes[-1].y + 1
            choices = [GrassLane, LogLane, LilypadLane, TrainLane, CarLane]
            # Pas plus de 2 lignes de nénuphars à la suite
            if len(self.lanes) >= 2 and isinstance(self.lanes[-1], LilypadLane) and isinstance(self.lanes[-2], LilypadLane):
                choices.remove(LilypadLane)

            lane_type = choice(choices)
            if lane_type in [LilypadLane, GrassLane]:
                self.lanes.append(lane_type(new_y, previous_lane=self.lanes[-1]))
            else:
                self.lanes.append(lane_type(new_y))

        self.lanes = [
            lane for lane in self.lanes
            if lane.y * 64 - camera_y < 700
        ]

        # Appeler `update` pour chaque voie avec `dt`
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
        # Appliquer la vitesse de la bûche si le joueur est dessus
        px, py = world_to_screen(player.grid_x, player.grid_y, camera_y)
        player_rect = pygame.Rect(px + 8, py + 8, 48, 48)

        for lane in self.lanes:
            if lane.y == player.grid_y:
                speed = lane.get_speed(player_rect, camera_y)
                if speed != 0:
                    player.grid_x += speed * dt
                    
                    # Vérifier si le joueur sort de l'écran (Game Over)
                    if player.grid_x < 2 or player.grid_x > GRID_WIDTH - 2:
                        return True # Indique une mort par sortie d'écran
        return False

    def check_collisions(self, player, camera_y):
        # On recrée le rect du joueur pour tester les collisions
        px, py = world_to_screen(player.grid_x, player.grid_y, camera_y)
        player_rect = pygame.Rect(px + 8, py + 8, 48, 48)

        for lane in self.lanes:
            if lane.y == player.grid_y:
                return lane.check_collision(player_rect, camera_y)
        return False
    def snap_player_x(self, x, y):
        for lane in self.lanes:
            if lane.y == y:
                if isinstance(lane, LogLane):
                    # Si c'est une voie de rivière, on essaie de s'aligner sur une bûche
                    for log in lane.logs:
                        log_x, length = log
                        # Si x est à portée de cette bûche (avec une petite marge)
                        if log_x - 0.5 <= x <= log_x + length - 0.5:
                            # On s'aligne sur la section de la bûche (offset entier)
                            return log_x + round(x - log_x)
                    # Si pas de bûche, on s'aligne sur la grille (pour la noyade propre)
                    return round(x)
                else:
                    # Pour toutes les autres voies (Herbe, Route, Rail, Nénuphar), on s'aligne sur la grille
                    return round(x)
        return round(x)