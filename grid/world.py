from grid.lane import Lane
from random import randint

class World:
    def __init__(self):
        self.lanes = []
        self.generate_initial()

    def generate_initial(self):
        for y in range(15):
            self.lanes.append(Lane(y, (randint(0,150), randint(0,150), randint(0,150))))

    def update(self, camera_y):
        # Générer vers le haut
        while self.lanes[-1].y * 64 - camera_y < 640:
            new_y = self.lanes[-1].y + 1
            self.lanes.append(Lane(new_y, (randint(0,150), randint(0,150), randint(0,150))))

        # Supprimer en bas
        self.lanes = [
            lane for lane in self.lanes
            if lane.y * 64 - camera_y < 700
        ]

    def draw(self, screen, camera_y):
        for lane in self.lanes:
            lane.draw(screen, camera_y)
