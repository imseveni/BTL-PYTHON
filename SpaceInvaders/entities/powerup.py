import pygame
from pygame.locals import *


class PowerUp:
    def __init__(self, image_path, x, y, details):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.speed = 0.5
        self.details = details
        self.rect = self.image.get_rect()
        self.update_rect()

    def draw(self, screen):
        self.update_rect()
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.y += self.speed

    def update_rect(self):
        self.rect.center = (self.x, self.y)