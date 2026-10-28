class Bullet:
    def __init__(
        self,
        image,
        x,
        y,
        speed
    ):

        self.image = image

        self.speed = speed

        self.rect = self.image.get_rect()

        # Đạn xuất hiện ở giữa player
        self.rect.midbottom = (
            int(x),
            int(y)
        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        self.rect.y -= self.speed

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )

    # ==================================================
    # CHECK OUTSIDE
    # ==================================================

    def is_outside(self):

        return self.rect.bottom < 0