import pygame
import random


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)

        self.radius = random.randint(2, 5)

        self.lifetime = random.randint(15, 25)

        self.color = random.choice([
            (255, 255, 200),
            (255, 180, 30),
            (255, 50, 20)
        ])

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.lifetime -= 1

        if (
            self.radius > 1
            and self.lifetime % 5 == 0
        ):
            self.radius -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(
                screen,
                self.color,
                (
                    int(self.x),
                    int(self.y)
                ),
                self.radius
            )


class Explosion:
    def __init__(
        self,
        x,
        y,
        particle_count=20
    ):

        self.particles = [
            Particle(x, y)
            for _ in range(particle_count)
        ]

    def update(self):

        for particle in self.particles:
            particle.update()

        self.particles = [
            particle
            for particle in self.particles
            if particle.lifetime > 0
        ]

    def draw(self, screen):

        for particle in self.particles:
            particle.draw(screen)

    def is_finished(self):

        return len(self.particles) == 0