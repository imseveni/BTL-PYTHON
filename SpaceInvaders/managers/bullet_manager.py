import pygame

from entities.bullet import Bullet

from config import (
    BULLET_IMAGE,
    BULLET_SPEED,
    SHOOT_COOLDOWN
)


class BulletManager:
    def __init__(self):

        self.bullet_image = pygame.image.load(
            str(BULLET_IMAGE)
        ).convert_alpha()

        self.bullets = []

        self.last_shot_time = 0

    # ==================================================
    # SHOOT
    # ==================================================

    def shoot(self, x, y):

        current_time = pygame.time.get_ticks()

        # Cooldown
        if (
            current_time
            - self.last_shot_time
            < SHOOT_COOLDOWN
        ):
            return False

        bullet = Bullet(
            image=self.bullet_image,
            x=x,
            y=y,
            speed=BULLET_SPEED
        )

        self.bullets.append(
            bullet
        )

        self.last_shot_time = current_time

        return True

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        for bullet in self.bullets:
            bullet.update()

        # Xóa bullet ra ngoài màn hình
        self.bullets = [
            bullet
            for bullet in self.bullets
            if not bullet.is_outside()
        ]

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        for bullet in self.bullets:
            bullet.draw(screen)

    # ==================================================
    # REMOVE
    # ==================================================

    def remove(self, bullet):

        if bullet in self.bullets:
            self.bullets.remove(
                bullet
            )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.bullets.clear()

        self.last_shot_time = 0