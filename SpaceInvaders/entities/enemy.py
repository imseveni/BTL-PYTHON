from config import SCREEN_WIDTH


class Enemy:
    def __init__(
        self,
        image,
        x,
        y,
        speed,
        drop_distance,
        health=1,
        score=10
    ):

        self.image = image

        self.x = x
        self.y = y

        self.speed = speed

        self.x_change = speed

        self.drop_distance = drop_distance

        self.health = health

        self.max_health = health

        self.score = score

        self.rect = self.image.get_rect()

        self.update_rect()

    # ==================================================
    # UPDATE RECT
    # ==================================================

    def update_rect(self):

        self.rect.topleft = (
            int(self.x),
            int(self.y)
        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        self.x += self.x_change

        max_x = SCREEN_WIDTH - self.image.get_width()

        # Chạm bên trái
        if self.x <= 0:

            self.x = 0

            self.x_change = abs(
                self.speed
            )

            self.y += self.drop_distance

        # Chạm bên phải
        elif self.x >= max_x:

            self.x = max_x

            self.x_change = -abs(
                self.speed
            )

            self.y += self.drop_distance

        self.update_rect()

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )

    # ==================================================
    # TAKE DAMAGE
    # ==================================================

    def take_damage(self, damage=1):

        self.health -= damage

        return self.health <= 0

    # ==================================================
    # RESPAWN
    # ==================================================

    def respawn(self, x, y):

        self.x = x
        self.y = y

        self.health = self.max_health

        self.update_rect()

    # ==================================================
    # SET SPEED
    # ==================================================

    def set_speed(self, new_speed):

        # Giữ nguyên hướng hiện tại
        if self.x_change >= 0:
            self.x_change = new_speed
        else:
            self.x_change = -new_speed

        self.speed = new_speed