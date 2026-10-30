class PowerUp:
    def __init__(
        self,
        image,
        x,
        y,
        power_type
    ):

        self.image = image

        self.power_type = power_type

        self.speed = 3

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):

        self.rect.y += self.speed

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )

    def is_outside(self, screen_height):

        return self.rect.top > screen_height