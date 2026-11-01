import random
import pygame

from entities.enemy import NormalEnemy, FastEnemy, TankEnemy
from config import (
    ENEMY_IMAGE,
    ENEMY_COUNT,
    ENEMY_SPEED,
    ENEMY_DROP_DISTANCE,
    ENEMY_MIN_Y,
    ENEMY_MAX_Y,
    GAME_OVER_Y,
    SCREEN_WIDTH
)


class EnemyManager:
    """Quản lý danh sách Enemy, sinh quái, cập nhật vị trí và độ khó theo Level."""

    MAX_ENEMIES = 14

    def __init__(self):
        # Load ảnh 1 lần duy nhất
        self.enemy_image = pygame.image.load(
            str(ENEMY_IMAGE)
        ).convert_alpha()

        self.enemies = []
        self.current_level = 1
        self.current_speed = ENEMY_SPEED
        self.current_enemy_count = ENEMY_COUNT

        self.spawn_enemies()

    # ==================================================
    # CHỌN LOẠI ENEMY THEO LEVEL
    # ==================================================

    def _choose_enemy_class(self):
        """Tăng dần tỷ lệ xuất hiện FastEnemy và TankEnemy khi Level tăng."""
        if self.current_level == 1:
            weights = [70, 20, 10]
        elif self.current_level == 2:
            weights = [55, 30, 15]
        else:
            weights = [40, 35, 25]

        return random.choices(
            [NormalEnemy, FastEnemy, TankEnemy],
            weights=weights,
            k=1
        )[0]

    def _random_position(self):
        max_x = SCREEN_WIDTH - self.enemy_image.get_width()
        x = random.randint(0, max_x)
        y = random.randint(ENEMY_MIN_Y, ENEMY_MAX_Y)
        return x, y

    # ==================================================
    # CREATE ENEMY
    # ==================================================

    def create_enemy(self, enemy_class=None):
        x, y = self._random_position()

        if enemy_class is None:
            enemy_class = self._choose_enemy_class()

        enemy = enemy_class(
            image=self.enemy_image,
            x=x,
            y=y,
            speed=self.current_speed,
            drop_distance=ENEMY_DROP_DISTANCE
        )

        # Ngẫu nhiên hướng di chuyển ban đầu (trái hoặc phải)
        if random.choice([True, False]):
            enemy.x_change = -abs(enemy.speed)

        return enemy

    # ==================================================
    # SPAWN
    # ==================================================

    def spawn_enemies(self):
        self.enemies.clear()

        for _ in range(self.current_enemy_count):
            enemy = self.create_enemy()
            self.enemies.append(enemy)

    # ==================================================
    # UPDATE & DRAW
    # ==================================================

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

    # ==================================================
    # REMOVE & RESPAWN
    # ==================================================

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def respawn(self, enemy):
        """Hồi sinh quái ở vị trí mới và có cơ hội đổi sang loại Enemy mới."""
        x, y = self._random_position()

        if enemy in self.enemies:
            idx = self.enemies.index(enemy)
            self.enemies[idx] = self.create_enemy()
        else:
            enemy.respawn(x, y)

    # ==================================================
    # INCREASE DIFFICULTY
    # ==================================================

    def increase_difficulty(self, level):
        self.current_level = max(1, level)

        # Tăng tốc độ cơ bản mỗi level (+0.4 mỗi level để không quá khó)
        self.current_speed = ENEMY_SPEED + (self.current_level - 1) * 0.4

        for enemy in self.enemies:
            enemy.set_speed(self.current_speed)

        # Tăng số lượng enemy mỗi khi lên level (+2 mỗi level, tối đa 14)
        target_count = min(
            ENEMY_COUNT + (self.current_level - 1) * 2,
            self.MAX_ENEMIES
        )
        self.current_enemy_count = target_count

        while len(self.enemies) < self.current_enemy_count:
            self.enemies.append(self.create_enemy())

    # ==================================================
    # CHECK BOTTOM LIMIT
    # ==================================================

    def has_enemy_reached_bottom(self, limit_y=GAME_OVER_Y):
        """Kiểm tra xem có enemy nào tràn xuống quá giới hạn Y hay không."""
        return any(enemy.y > limit_y for enemy in self.enemies)

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):
        self.current_level = 1
        self.current_speed = ENEMY_SPEED
        self.current_enemy_count = ENEMY_COUNT
        self.spawn_enemies()