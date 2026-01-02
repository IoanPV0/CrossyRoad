from constants import SCREEN_HEIGHT, TILE_SIZE

class Camera:
    def __init__(self, scroll_speed):
        self.y = 0  # pixels
        self.scroll_speed = scroll_speed

    def update(self, dt, player):
        # 1️⃣ pression constante
        self.y += self.scroll_speed * dt

        # 2️⃣ follow conditionnel
        FOLLOW_RATIO = 0.55
        follow_screen_y = SCREEN_HEIGHT * FOLLOW_RATIO

        player_pixel_y = player.grid_y * TILE_SIZE
        desired_y = player_pixel_y - (SCREEN_HEIGHT - follow_screen_y)

        # 3️⃣ on prend le max
        if desired_y > self.y:
            self.y = desired_y
