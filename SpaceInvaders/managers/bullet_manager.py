import pygame

from entities.bullet import Bullet
from entities.explosion import Explosion

from config import (
    BULLET_IMAGE,
    BULLET_SPEED,
    SHOOT_COOLDOWN,
    ENEMY_BULLET_SPEED,
    SCREEN_HEIGHT
)


class BulletManager:
    def __init__(self):

        # ==================================================
        # IMAGE
        # ==================================================

        self.bullet_image = pygame.image.load(
            str(BULLET_IMAGE)
        ).convert_alpha()

        # Hiện tại chưa có ảnh riêng cho enemy bullet.
        # Nếu None, Bullet sẽ tự tạo Surface.
        self.enemy_bullet_image = None

        # ==================================================
        # BULLET LIST
        # ==================================================

        self.player_bullets = []

        self.enemy_bullets = []

        # ==================================================
        # EXPLOSION
        # ==================================================

        self.explosions = []

        # ==================================================
        # COOLDOWN
        # ==================================================

        self.last_player_shot = 0

    # ==================================================
    # COMPATIBILITY
    # ==================================================

    @property
    def bullets(self):
        """
        Giữ tương thích với game.py hiện tại.

        game.py cũ đang dùng:
            self.bullet_manager.bullets

        nên bullets sẽ đại diện cho player_bullets.
        """

        return self.player_bullets

    # ==================================================
    # SHOOT PLAYER
    # ==================================================

    def shoot_player(self, x, y):

        current_time = pygame.time.get_ticks()

        # Cooldown
        if (
            current_time
            - self.last_player_shot
            < SHOOT_COOLDOWN
        ):
            return False

        bullet = Bullet(
            image=self.bullet_image,
            x=x,
            y=y,
            speed=BULLET_SPEED,
            direction=-1,
            damage=1
        )

        self.player_bullets.append(
            bullet
        )

        self.last_player_shot = current_time

        return True

    # ==================================================
    # SHOOT - GIỮ TƯƠNG THÍCH CODE CŨ
    # ==================================================

    def shoot(self, x, y):

        """
        game.py hiện tại vẫn gọi:

            bullet_manager.shoot(x, y)

        nên giữ hàm này và chuyển tiếp sang shoot_player().
        """

        return self.shoot_player(
            x,
            y
        )

    # ==================================================
    # SHOOT ENEMY
    # ==================================================

    def shoot_enemy(
        self,
        x,
        y,
        speed=5,
        damage=1
    ):

        bullet = Bullet(
            image=self.enemy_bullet_image,
            x=x,
            y=y,
            speed=ENEMY_BULLET_SPEED,
            direction=1,
            damage=1,
            color=(255, 60, 60)
        )

        self.enemy_bullets.append(
            bullet
        )

        return True

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        # ==================================================
        # PLAYER BULLET
        # ==================================================

        for bullet in self.player_bullets:

            bullet.update()

        self.player_bullets = [
            bullet
            for bullet in self.player_bullets
            if not bullet.is_outside(
                SCREEN_HEIGHT
            )
        ]

        # ==================================================
        # ENEMY BULLET
        # ==================================================

        for bullet in self.enemy_bullets:

            bullet.update()

        self.enemy_bullets = [
            bullet
            for bullet in self.enemy_bullets
            if not bullet.is_outside(
                SCREEN_HEIGHT
            )
        ]

        # ==================================================
        # EXPLOSION
        # ==================================================

        for explosion in self.explosions:

            explosion.update()

        self.explosions = [
            explosion
            for explosion in self.explosions
            if not explosion.is_finished()
        ]

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        # Player bullets
        for bullet in self.player_bullets:

            bullet.draw(
                screen
            )

        # Enemy bullets
        for bullet in self.enemy_bullets:

            bullet.draw(
                screen
            )

        # Explosion
        for explosion in self.explosions:

            explosion.draw(
                screen
            )

    # ==================================================
    # REMOVE PLAYER BULLET
    # ==================================================

    def remove(self, bullet):

        if bullet in self.player_bullets:

            self.player_bullets.remove(
                bullet
            )

    # ==================================================
    # REMOVE ENEMY BULLET
    # ==================================================

    def remove_enemy_bullet(self, bullet):

        if bullet in self.enemy_bullets:

            self.enemy_bullets.remove(
                bullet
            )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.player_bullets.clear()

        self.enemy_bullets.clear()

        self.explosions.clear()

        self.last_player_shot = 0

    # ==================================================
    # ADD EXPLOSION
    # ==================================================

    def add_explosion(self, x, y):

        self.explosions.append(
            Explosion(x, y)
        )