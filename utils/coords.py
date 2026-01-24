# utils/coords.py
from constants import TILE_SIZE, SCREEN_HEIGHT

def world_to_screen(x, y, camera_y):
    """
    Monde :
      y = 0 → bas
      y ↑   → avance du joueur

    Écran pygame :
      y = 0 → haut
      y ↓   → bas
    """
    camera_x = 0
    if isinstance(camera_y, (tuple, list)):
        camera_x = camera_y[0]
        camera_y = camera_y[1]

    px = x * TILE_SIZE - camera_x
    py = SCREEN_HEIGHT - (y * TILE_SIZE - camera_y)
    return px, py
