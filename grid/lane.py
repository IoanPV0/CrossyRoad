from grid.tile import Tile
from utils.coords import world_to_screen
from constants import TILE_SIZE, GRID_WIDTH
import pygame
import random

class Lane:
    def __init__(self, y_index, tile_color):
        self.y = y_index
        self.tiles = [
            Tile(x, y_index, tile_color)
            for x in range(11)
        ]

    def draw(self, screen, camera_y):
        for tile in self.tiles:
            tile.draw(screen, camera_y)

class GrassLane(Lane):
    def __init__(self, y_index):
        super().__init__(y_index, (70, 170, 70))  # Vert pour l'herbe
    def update(self, dt):
        pass

class RiverLane(Lane):
    def __init__(self, y_index):
        super().__init__(y_index, (80, 80, 200))  # Bleu pour la rivière
        self.logs = self.generate_logs()

    def generate_logs(self):
        return [random.randint(0, 10) for _ in range(3)]  # Exemple de positions de troncs

    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        # Dessiner les troncs
        for log in self.logs:
            # Exemple : dessiner des rectangles pour les troncs
            pass

    def update(self, dt):
        # Exemple : les troncs pourraient se déplacer ici
        pass

class TrainLane(Lane):
    def __init__(self, y_index):
        super().__init__(y_index, (70, 70, 70))  # Gris pour la voie ferrée
        self.direction = random.choice([-1, 1]) # 1 va vers la droite part de la gauche
        if self.direction == 1:
            self.train_position_depart = -1
        else:
            self.train_position_depart = GRID_WIDTH + 1
        self.train_position = self.train_position_depart
        self.alert_time = 2  # Temps d'alerte en secondes
        self.alert_timer = self.alert_time
        self.cooldown = random.uniform(2, 5)
        self.train_timer = 1
        self.train_active = False
        self.train_longueur = 100
        self.train_speed = 100

    def update(self, dt):
        if self.train_active:
            self.train_position += dt * self.train_speed * self.direction # Exemple de mouvement du train
            if (self.direction == 1 and self.train_position - self.train_longueur > (GRID_WIDTH + 1)) or \
               (self.direction == -1 and self.train_position + self.train_longueur < -1):
                  # Réinitialiser le train
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
                    self.alert_timer = self.alert_time

        

    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        if not self.train_active and self.cooldown <= self.alert_time and int(self.alert_timer * 8) % 2 == 0:  # Clignotement rouge
            color = (200, 0, 0)  # Rouge pour l'alerte
        else:
            color = (70, 70, 70)  # Gris pour la voie ferrée
        for tile in self.tiles:
            tile.color = color
            tile.draw(screen, camera_y)

        if self.train_active:
            # Dessiner le train uniquement s'il est actif
            px, py = world_to_screen(self.train_position, self.y, camera_y)
            if self.direction == 1:
                rect = pygame.Rect(px - TILE_SIZE * 100, py , TILE_SIZE * 100, TILE_SIZE)   # Train vers la gauche
            else:
                rect = pygame.Rect(px, py, TILE_SIZE * 100, TILE_SIZE)
            pygame.draw.rect(screen, (255, 255, 0), rect)  # Jaune pour le train


class CarLane(Lane):
    def __init__(self, y_index):
        super().__init__(y_index, (128, 128, 128))  # Rouge pour la route
        self.cars = self.generate_cars()
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(1, 4)

    def generate_cars(self):
        return [random.randint(0, 10) for _ in range(2)]  # Exemple de positions de voitures

    def update(self, dt):
        # Déplacer les voitures dans la direction définie
        for i in range(len(self.cars)):
            self.cars[i] += dt * self.speed * self.direction  # Vitesse de 5 unités par seconde
            if self.direction == 1 and self.cars[i] > 10:  # Réinitialiser si hors écran à droite
                self.cars[i] = -1
            elif self.direction == -1 and self.cars[i] < -1:  # Réinitialiser si hors écran à gauche
                self.cars[i] = 10

    def draw(self, screen, camera_y):
        super().draw(screen, camera_y)
        # Dessiner les voitures
        for car in self.cars:
            px, py = world_to_screen(car, self.y, camera_y)
            rect = pygame.Rect(px + 5, py + 10, TILE_SIZE - 10, TILE_SIZE - 20)  # Rectangle rouge
            pygame.draw.rect(screen, (200, 0, 0), rect)