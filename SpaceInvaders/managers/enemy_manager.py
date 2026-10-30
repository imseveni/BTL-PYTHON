import random

import pygame

from entities.enemy import Enemy

from config import (
    ENEMY_IMAGE,
    ENEMY_COUNT,
    ENEMY_SPEED,
    ENEMY_DROP_DISTANCE,
    ENEMY_MIN_Y,
    ENEMY_MAX_Y,
    NORMAL_ENEMY_SCORE,
    SCREEN_WIDTH
)


class EnemyManager:
    def __init__(self):

        # Load ảnh 1 lần
        self.enemy_image = pygame.image.load(
            str(ENEMY_IMAGE)
        ).convert_alpha()

        self.enemies = []

        self.current_speed = ENEMY_SPEED

        self.spawn_enemies()

    # ==================================================
    # CREATE ENEMY
    # ==================================================

    def create_enemy(self):

        max_x = (
            SCREEN_WIDTH
            - self.enemy_image.get_width()
        )

        x = random.randint(
            0,
            max_x
        )

        y = random.randint(
            ENEMY_MIN_Y,
            ENEMY_MAX_Y
        )

        enemy = Enemy(
            image=self.enemy_image,
            x=x,
            y=y,
            speed=self.current_speed,
            drop_distance=ENEMY_DROP_DISTANCE,
            health=1,
            score=NORMAL_ENEMY_SCORE
        )

        return enemy

    # ==================================================
    # SPAWN
    # ==================================================

    def spawn_enemies(self):

        self.enemies.clear()

        for _ in range(ENEMY_COUNT):

            enemy = self.create_enemy()

            self.enemies.append(
                enemy
            )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        for enemy in self.enemies:
            enemy.update()

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        for enemy in self.enemies:
            enemy.draw(screen)

    # ==================================================
    # RESPAWN
    # ==================================================

    def respawn(self, enemy):

        max_x = (
            SCREEN_WIDTH
            - self.enemy_image.get_width()
        )

        x = random.randint(
            0,
            max_x
        )

        y = random.randint(
            ENEMY_MIN_Y,
            ENEMY_MAX_Y
        )

        enemy.respawn(
            x,
            y
        )

    # ==================================================
    # INCREASE DIFFICULTY
    # ==================================================

    def increase_difficulty(self, level):

        # Mỗi level tăng 0.5 tốc độ
        self.current_speed = (
            ENEMY_SPEED
            + (level - 1) * 0.5
        )

        for enemy in self.enemies:

            enemy.set_speed(
                self.current_speed
            )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.current_speed = ENEMY_SPEED

        self.spawn_enemies()