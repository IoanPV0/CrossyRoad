from grid.lane import GrassLane, LogLane, LilypadLane, TrainLane, CarLane
from random import randint, choice
from constants import GRID_WIDTH

class World:
    def __init__(self):
        self.lanes = []
        self.generate_initial()

    def generate_initial(self):
        # 1. Les 2 voies du bas (0, 1) : GrassLane pleines d'arbres (sauf centre pour le spawn)
        for y in range(3):
            lane = GrassLane(y)
            lane.obstacles = []
            for x in range(GRID_WIDTH):
                lane.obstacles.append((x, 'tree'))
            self.lanes.append(lane)

        # 2. Les 3 voies suivantes (2, 3, 4) : GrassLane avec arbres sur les côtés
        for y in range(3, 7):
            lane = GrassLane(y)
            lane.obstacles = []
            for x in [0, 1, GRID_WIDTH-2, GRID_WIDTH-1]:
                lane.obstacles.append((x, 'tree'))
            self.lanes.append(lane)

        # 3. Le reste (5 à 14) : Génération aléatoire
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