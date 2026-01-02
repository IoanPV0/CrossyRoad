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
    px = x * TILE_SIZE
    py = SCREEN_HEIGHT - (y * TILE_SIZE - camera_y)
    return px, py
