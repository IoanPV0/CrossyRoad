from grid.tile import Tile

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
