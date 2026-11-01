import pygame
from pygame.locals import *


class PowerUp:
    def __init__(
        self,
        image,
        x,
        y,
        power_type,
        speed=3
    ):

        self.image = image

        self.power_type = power_type

        self.speed = speed

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        self.rect.y += self.speed

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):
        self.update_rect()
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.y += self.speed

    # ==================================================
    # CHECK OUTSIDE
    # ==================================================

    def is_outside(self, screen_height):

        return self.rect.top > screen_height