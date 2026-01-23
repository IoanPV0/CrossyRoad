from grid.lane import GrassLane, RiverLane, TrainLane, CarLane
from random import randint, choice

class World:
    def __init__(self):
        self.lanes = []
        self.generate_initial()

    def generate_initial(self):
        for y in range(15):
            lane_type = choice([GrassLane, RiverLane, TrainLane, CarLane])
            self.lanes.append(lane_type(y))

    def update(self, camera_y, dt):
        while self.lanes[-1].y * 64 - camera_y < 640:
            new_y = self.lanes[-1].y + 1
            lane_type = choice([GrassLane, RiverLane, TrainLane, CarLane])
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