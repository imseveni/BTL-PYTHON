import pygame
from entities.powerup import PowerUp

class PowerUpManager:
    def __init__(self):
        self.powerups = []

    def update(self):
        for i in self.powerups:
            if(i.y >= 800): self.powerups.remove(i)
            else: i.update()

    def draw(self, screen):
        for i in self.powerups:
            i.draw(screen)
    
    def reset(self):
        self.powerups.clear()