from grid.tile import Tile
from utils.coords import world_to_screen
from constants import TILE_SIZE, GRID_WIDTH, SCREEN_WIDTH
import pygame
import random
import math

class Lane:
    def __init__(self, y_index, tile_color):
        self.y = y_index
        self.tiles = [
            Tile(x, y_index, tile_color)
            for x in range(-5, GRID_WIDTH + 5)
        ]

    def draw(self, screen, camera_y):
        for tile in self.tiles:
            tile.draw(screen, camera_y)

    def draw_side_shading(self, screen, camera_y):
        # Opacite ombre gauche
        px_start, py = world_to_screen(2, self.y, camera_y)
        w_left = int(px_start)
        if w_left > 0:
            shadow_surface = pygame.Surface((w_left, TILE_SIZE), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 128))
            screen.blit(shadow_surface, (0, py))

        # Ombre droite
        px_end, _ = world_to_screen(GRID_WIDTH - 2, self.y, camera_y)
        w_right = SCREEN_WIDTH - int(px_end)
        if w_right > 0:
            shadow_surface = pygame.Surface((w_right, TILE_SIZE), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 128))
            screen.blit(shadow_surface, (int(px_end), py))
   
        
    def check_collision(self, player_rect, camera_y):
        return False
    def get_speed(self, player_rect, camera_y):
        return 0

class GrassLane(Lane):
    def __init__(self, y_index, previous_lane=None, full_of_trees=False, forbidden_indices=None):
        super().__init__(y_index, (70, 170, 70))
        self.obstacles = []
        self.generate_obstacles(previous_lane, full_of_trees, forbidden_indices)
    def generate_obstacles(self, previous_lane, full_of_trees, forbidden_indices):
        for x in range(-5, 2):
            self.obstacles.append((x, 'tree'))
        for x in range(GRID_WIDTH - 2, GRID_WIDTH + 5):
            self.obstacles.append((x, 'tree'))
        forbidden_x = set()
        if forbidden_indices:
            forbidden_x.update(forbidden_indices)
        # pas dobstacles devant nénuphars
        if previous_lane and isinstance(previous_lane, LilypadLane):
            forbidden_x.update(previous_lane.pads)

        if full_of_trees:
            for x in range(2, GRID_WIDTH - 2):
                if x not in forbidden_x:
                    self.obstacles.append((x, 'tree'))
        else: # generation aleatoire zone jouable
            nb_obstacles = random.randint(0, 3)
            candidates = [x for x in range(2, GRID_WIDTH - 2) if x not in forbidden_x]
            if candidates:
                chosen_x = random.sample(candidates, min(nb_obstacles, len(candidates)))
                for x in chosen_x:
                    self.obstacles.append((x, random.choice(['tree', 'rock'])))


    def update(self, dt):
        pass

    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        for x, obs_type in self.obstacles:
            px, py = world_to_screen(x, self.y, camera_y)
            if obs_type == 'tree':
                # dessin arbre
                pygame.draw.rect(screen, (101, 67, 33), (px + 24, py + 32, 16, 32))
                pygame.draw.rect(screen, (34, 139, 34), (px + 12, py + 10, 40, 30))
            else:
                # dessin rocher
                pygame.draw.rect(screen, (100, 100, 100), (px + 10, py + 20, 44, 30))
        self.draw_side_shading(screen, camera_y)

class RiverLane(Lane):
    def __init__(self, y_index):
        super().__init__(y_index, (80, 80, 200))

    def update(self, dt):
        pass
    def check_collision(self, player_rect, camera_y):
        return True
    def draw_side_shading(self, screen, camera_y):
        pass
    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        # mousse (rectangles blancs)
        t = pygame.time.get_ticks() / 200.0
        
        # Côté gauche (limite x=1 / x=2)
        px, py = world_to_screen(1, self.y, camera_y)
        for i in range(4):
            offset = math.sin(t + i * 0.5) * 4
            rect = pygame.Rect(px + TILE_SIZE - 8 + offset, py + i * (TILE_SIZE/4) + 4, 8, 10)
            pygame.draw.rect(screen, (255, 255, 255, 200), rect)

        # Côté droit (limite x=GRID_WIDTH-2 / x=GRID_WIDTH-3)
        px, py = world_to_screen(GRID_WIDTH - 2, self.y, camera_y)
        for i in range(4):
            offset = math.sin(t + i * 0.5) * 4
            rect = pygame.Rect(px + offset, py + i * (TILE_SIZE/4) + 4, 8, 10)
            pygame.draw.rect(screen, (255, 255, 255, 200), rect)

class LogLane(RiverLane):
    def __init__(self, y_index):
        super().__init__(y_index)
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.5, 3.5)
        self.logs = []  # liste de [position_x, longueur]
        self.generate_logs()

    def generate_logs(self):
        x = -3
        while x < GRID_WIDTH + 3:
            length = random.choice([1, 2, 3])
            self.logs.append([x, length])
            x += length + random.randint(2, 4) # espace entre les bûches

    def update(self, dt):
        for log in self.logs:
            log[0] += dt * self.speed * self.direction
            
            # Gestion de la sortie d'écran (wrap-around)
            if self.direction == 1 and log[0] > GRID_WIDTH + 2:
                log[0] = -log[1] - 2
            elif self.direction == -1 and log[0] + log[1] < -2:
                log[0] = GRID_WIDTH + 2

    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        for x, length in self.logs:
            px, py = world_to_screen(x, self.y, camera_y)
            # Dessin buche
            rect = pygame.Rect(px, py + 10, length * TILE_SIZE, TILE_SIZE - 20)
            pygame.draw.rect(screen, (101, 67, 33), rect, border_radius=10)
            
            # details buche
            wood_dark = (85, 55, 25)
            pygame.draw.line(screen, wood_dark, (px + 15, py + 20), (px + length * TILE_SIZE - 15, py + 20), 3)
            pygame.draw.line(screen, wood_dark, (px + 15, py + 35), (px + length * TILE_SIZE - 15, py + 35), 3)
    def check_collision(self, player_rect, camera_y):
        # Verification joueur sur une bûche
        # reduction hitbox du joueur pour qu'il soit sur la bûche
        feet_rect = player_rect.inflate(-30, -30)
        
        for x, length in self.logs:
            px, py = world_to_screen(x, self.y, camera_y)
            log_rect = pygame.Rect(px, py, length * TILE_SIZE, TILE_SIZE)
            if feet_rect.colliderect(log_rect):
                return False
        return True
    def get_speed(self, player_rect, camera_y):
        #retour vitesse buche pour avoir vitesse joueur
        return self.speed * self.direction

class LilypadLane(RiverLane):
    def __init__(self, y_index, previous_lane=None):
        super().__init__(y_index)
        self.pads = []
        self.generate_pads(previous_lane)

    def generate_pads(self, previous_lane):
        forbidden_x = set()
        # Si la ligne précédente est de l'herbe avec obstacles, on évite ces positions
        if previous_lane and isinstance(previous_lane, GrassLane):
            for x, _ in previous_lane.obstacles:
                forbidden_x.add(x)
        if previous_lane and isinstance(previous_lane, LilypadLane):
            # Pas de nenuphars dans le vide (chemin possible)
            possible_pads = previous_lane.pads
            for x in possible_pads:
                if random.random() < 0.6: #elimination de qq nenuphars
                    self.pads.append(x)

            if len(self.pads) > 4:
                self.pads = sorted(random.sample(self.pads, 4))
            
            # au moins 1 nenuphar sur la riviere
            if not self.pads and possible_pads:
                self.pads.append(random.choice(possible_pads))
        else:
            # generation normale mais pas derriere un obstacle grasslane
            valid_candidates = [x for x in range(2, GRID_WIDTH - 2) if x not in forbidden_x]

            for x in valid_candidates:
                dist = abs(x - GRID_WIDTH // 2)
                prob = 0.8 - (dist * 0.05)
                if random.random() < prob:
                    self.pads.append(x)
            if len(self.pads) > 4:
                self.pads = sorted(random.sample(self.pads, 4))
            
            # garantie au moins 1 nenuphar
            if not self.pads:
                if valid_candidates:
                    self.pads.append(random.choice(valid_candidates))
                else:
                    self.pads.append(GRID_WIDTH // 2)

    def update(self, dt):
        pass

    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        for x in self.pads:
            px, py = world_to_screen(x, self.y, camera_y)
            center_x = px + TILE_SIZE // 2
            center_y = py + TILE_SIZE // 2
            radius = (TILE_SIZE - 10) // 2
            pygame.draw.circle(screen, (34, 139, 34), (center_x, center_y), radius)
            
            water_color = (80, 80, 200)
            points = [
                (center_x, center_y),
                (center_x + radius, center_y - 8),
                (center_x + radius, center_y + 8)
            ]
            pygame.draw.polygon(screen, water_color, points)

    def check_collision(self, player_rect, camera_y):
        feet_rect = player_rect.inflate(-30, -30)
        for x in self.pads:
            px, py = world_to_screen(x, self.y, camera_y)
            pad_rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
            if feet_rect.colliderect(pad_rect):
                return False # Sauvé
        return True

class TrainLane(Lane):
    def __init__(self, y_index):
        super().__init__(y_index, (70, 70, 70))
        self.direction = random.choice([-1, 1]) # 1 va vers la droite part de la gauche
        if self.direction == 1:
            self.train_position_depart = -1
        else:
            self.train_position_depart = GRID_WIDTH + 1
        self.train_position = self.train_position_depart
        self.alert_time = 2
        self.alert_timer = self.alert_time
        self.cooldown = random.uniform(3, 6)
        self.train_timer = 1
        self.train_active = False
        self.train_longueur = 40
        self.train_speed = 100
        self.train_colors = [(253, 184, 19), (220, 50, 50), (50, 150, 220)]
        self.current_train_color = random.choice(self.train_colors)

    def update(self, dt):
        if self.train_active:
            self.train_position += dt * self.train_speed * self.direction
            if (self.direction == 1 and self.train_position - self.train_longueur > (GRID_WIDTH + 1)) or \
               (self.direction == -1 and self.train_position + self.train_longueur < -1):
                  # reinitialiser train apres passage
                self.train_position = self.train_position_depart
                self.train_active = False
                self.cooldown = random.uniform(4, 10)
        else:
            # En cooldown
            self.cooldown -= dt
            if self.cooldown <= self.alert_time and not self.train_active:

                self.alert_timer -= dt
                if self.alert_timer <= 0:
                    self.train_active = True  # Activer le train après l'alerte
                    self.current_train_color = random.choice(self.train_colors)
                    self.alert_timer = self.alert_time

    def check_collision(self, player_rect, camera_y):
        if self.train_active:
            px, py = world_to_screen(self.train_position, self.y, camera_y)
            if self.direction == 1:
                train_rect = pygame.Rect(px - TILE_SIZE * 100, py, TILE_SIZE * 100, TILE_SIZE)
            else:
                train_rect = pygame.Rect(px, py, TILE_SIZE * 100, TILE_SIZE)
            
            hitbox = train_rect.inflate(-20, -20)
            if player_rect.colliderect(hitbox):
                return True
        return False    

    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        if not self.train_active and self.cooldown <= self.alert_time and int(self.alert_timer * 8) % 2 == 0:  # Clignotement rouge
            color = (200, 0, 0) 
        else:
            color = (70, 70, 70)
        for tile in self.tiles:
            tile.color = color
            tile.draw(screen, camera_y)
        
        # Dessin des rails
        # planches
        for x in range(-5, GRID_WIDTH + 5):
            px, py = world_to_screen(x, self.y, camera_y)
            pygame.draw.rect(screen, (101, 67, 33), (px + TILE_SIZE // 2 - 4, py, 8, TILE_SIZE))
        
        # rails
        px_start, py = world_to_screen(-5, self.y, camera_y)
        px_end, _ = world_to_screen(GRID_WIDTH + 5, self.y, camera_y)
        width = px_end - px_start + TILE_SIZE
        
        pygame.draw.rect(screen, (190, 190, 190), (px_start, py + 6, width, 6))
        pygame.draw.rect(screen, (190, 190, 190), (px_start, py + TILE_SIZE - 12, width, 6))


        if self.train_active:
            # dessin du train sil est actif
            px, py = world_to_screen(self.train_position, self.y, camera_y)
            
            train_color = self.current_train_color
            visual_length = TILE_SIZE * self.train_longueur

            if self.direction == 1:
                # Vers la droite : le corps est a gauche de px
                rect = pygame.Rect(px - visual_length, py + 5, visual_length, TILE_SIZE - 10)
                light_rect = pygame.Rect(px - 5, py + 10, 5, TILE_SIZE - 20)
            else:
                # Vers la gauche : le corps est a droite de px
                rect = pygame.Rect(px, py + 5, visual_length, TILE_SIZE - 10)
                light_rect = pygame.Rect(px, py + 10, 5, TILE_SIZE - 20)

            pygame.draw.rect(screen, train_color, rect, border_radius=5)
            # Bande décorative
            pygame.draw.rect(screen, (255, 255, 255), (rect.x, rect.y + 12, rect.width, 6))
            # Phare jaune
            pygame.draw.rect(screen, (255, 255, 0), light_rect)

        self.draw_side_shading(screen, camera_y)


class CarLane(Lane):
    def __init__(self, y_index, previous_lane=None):
        super().__init__(y_index, (70, 70, 70))
        self.is_continuation = isinstance(previous_lane, CarLane)
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.5, 3)
        self.cars = [] # Liste de [x, length, color]
        self.generate_cars()

    def generate_cars(self):
        x = -4
        while x < GRID_WIDTH + 4:
            if random.random() < 0.3:
                length = 2.2 # Camion
                color = (200, 200, 200)
            else:
                length = random.choice([1, 1.5]) # Voiture
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            
            self.cars.append([x, length, color])
            x += length + random.uniform(2, 5)

    def update(self, dt):
        for car in self.cars:
            car[0] += dt * self.speed * self.direction
            if self.direction == 1 and car[0] > GRID_WIDTH + 4:
                car[0] = -4 - car[1]
            elif self.direction == -1 and car[0] + car[1] < -4:
                car[0] = GRID_WIDTH + 4


    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)

        if self.is_continuation:
            px_start, py = world_to_screen(-5, self.y, camera_y)
            px_end, _ = world_to_screen(GRID_WIDTH + 5, self.y, camera_y)
            
            line_y = py + TILE_SIZE
            dash_width = 20
            gap_width = 20
            current_x = px_start
            while current_x < px_end:
                pygame.draw.rect(screen, (200, 200, 200), (current_x, line_y - 2, dash_width, 4))
                current_x += dash_width + gap_width

        for x, length, color in self.cars:
            px, py = world_to_screen(x, self.y, camera_y)
            
            car_w = length * TILE_SIZE - 10
            car_h = TILE_SIZE - 20
            car_x = px + 5
            car_y = py + 10
            
            pygame.draw.rect(screen, color, (car_x, car_y, car_w, car_h), border_radius=5)
            
            roof_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
            pygame.draw.rect(screen, roof_color, (car_x + 5, car_y + 5, car_w - 10, car_h - 10), border_radius=3)
            
            if self.direction == 1:
                pygame.draw.rect(screen, (255, 255, 0), (car_x + car_w - 4, car_y + 5, 4, 6))
                pygame.draw.rect(screen, (255, 255, 0), (car_x + car_w - 4, car_y + car_h - 11, 4, 6))
                pygame.draw.rect(screen, (200, 0, 0), (car_x, car_y + 5, 2, 6))
                pygame.draw.rect(screen, (200, 0, 0), (car_x, car_y + car_h - 11, 2, 6))
            else: # Vers la gauche
                pygame.draw.rect(screen, (255, 255, 0), (car_x, car_y + 5, 4, 6))
                pygame.draw.rect(screen, (255, 255, 0), (car_x, car_y + car_h - 11, 4, 6))
                pygame.draw.rect(screen, (200, 0, 0), (car_x + car_w - 2, car_y + 5, 2, 6))
                pygame.draw.rect(screen, (200, 0, 0), (car_x + car_w - 2, car_y + car_h - 11, 2, 6))

        self.draw_side_shading(screen, camera_y)

    def check_collision(self, player_rect, camera_y):
        for x, length, _ in self.cars:
            px, py = world_to_screen(x, self.y, camera_y)
            car_rect = pygame.Rect(px + 5, py + 10, length * TILE_SIZE - 10, TILE_SIZE - 20)
            if player_rect.colliderect(car_rect.inflate(-10, -10)):
                return True
        return False