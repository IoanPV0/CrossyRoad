from constants import SCREEN_HEIGHT, TILE_SIZE, SCREEN_WIDTH

class Camera:
    def __init__(self, scroll_speed):
        self.y = 0  # y = pixel
        self.scroll_speed = scroll_speed

    def update(self, dt, player):
        self.y += self.scroll_speed * dt
        self.x = 0

        #suivi du joueur
        FOLLOW_RATIO = 0.55
        follow_screen_y = SCREEN_HEIGHT * FOLLOW_RATIO

        player_pixel_y = player.grid_y * TILE_SIZE
        desired_y = player_pixel_y - (SCREEN_HEIGHT - follow_screen_y)

        if desired_y > self.y:
            self.y = desired_y
        self.x = player.grid_x * TILE_SIZE - (SCREEN_WIDTH / 2 - TILE_SIZE / 2)
