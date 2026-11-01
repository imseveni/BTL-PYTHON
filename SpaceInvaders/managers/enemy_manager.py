import random
import pygame

from entities.enemy import (
    NormalEnemy,
    FastEnemy,
    TankEnemy,
)

from config import (
    NORMAL_ENEMY_IMAGE,
    FAST_ENEMY_IMAGE,
    TANK_ENEMY_IMAGE,

    ENEMY_COUNT,
    ENEMY_SPEED,
    ENEMY_DROP_DISTANCE,
    ENEMY_MIN_Y,
    ENEMY_MAX_Y,

    GAME_OVER_Y,
    SCREEN_WIDTH,

    MAX_ENEMIES,

    ENEMY_SPEED_INCREASE_PER_LEVEL,
    ENEMY_COUNT_INCREASE_PER_LEVEL,

    ENEMY_SHOOT_COOLDOWN,
    MAX_ENEMY_BULLETS,  
)


class EnemyManager:
    """Quản lý danh sách Enemy, sinh quái, cập nhật vị trí và độ khó theo Level."""

        # ==================================================
        # LOAD IMAGES
        # ==================================================

        self.normal_enemy_image = pygame.image.load(
            str(NORMAL_ENEMY_IMAGE)
        ).convert_alpha()

        self.fast_enemy_image = pygame.image.load(
            str(FAST_ENEMY_IMAGE)
        ).convert_alpha()

        self.tank_enemy_image = pygame.image.load(
            str(TANK_ENEMY_IMAGE)
        ).convert_alpha()

        # ==================================================
        # ENEMY DATA
        # ==================================================

        self.enemies = []

        self.current_level = 1

        self.current_speed = ENEMY_SPEED
        self.current_enemy_count = ENEMY_COUNT

        self.current_enemy_count = ENEMY_COUNT

        # ==================================================
        # SPAWN
        # ==================================================

        self.last_enemy_shot = 0

        self.spawn_enemies()

    # ==================================================
    # CHOOSE ENEMY TYPE
    # ==================================================

    def _choose_enemy_class(self):

        # Level 1
        if self.current_level == 1:

            weights = [
                70,  # Normal
                20,  # Fast
                10,  # Tank
            ]

        # Level 2
        elif self.current_level == 2:

            weights = [
                55,
                30,
                15,
            ]

        # Level >= 3
        else:

            weights = [
                40,
                35,
                25,
            ]

        return random.choices(
            [
                NormalEnemy,
                FastEnemy,
                TankEnemy,
            ],
            weights=weights,
            k=1
        )[0]

    # ==================================================
    # GET IMAGE
    # ==================================================

    def _get_enemy_image(
        self,
        enemy_class
    ):

        if enemy_class == FastEnemy:

            return self.fast_enemy_image

        if enemy_class == TankEnemy:

            return self.tank_enemy_image

        return self.normal_enemy_image

    # ==================================================
    # RANDOM POSITION
    # ==================================================

    def _random_position(
        self,
        image
    ):

        max_x = (
            SCREEN_WIDTH
            - image.get_width()
        )

    def create_enemy(self, enemy_class=None):
        x, y = self._random_position()

        if enemy_class is None:
            enemy_class = self._choose_enemy_class()

        return x, y

    # ==================================================
    # CREATE ENEMY
    # ==================================================

    def create_enemy(
        self,
        enemy_class=None
    ):

        # Chọn Enemy theo tỷ lệ
        if enemy_class is None:

            enemy_class = (
                self._choose_enemy_class()
            )

        # Chọn ảnh phù hợp
        image = self._get_enemy_image(
            enemy_class
        )

        # Random vị trí dựa theo kích thước ảnh
        x, y = self._random_position(
            image
        )

        enemy = enemy_class(
            image=image,
            x=x,
            y=y,
            speed=self.current_speed,
            drop_distance=ENEMY_DROP_DISTANCE
        )

        # 50% đi trái, 50% đi phải
        if random.choice(
            [True, False]
        ):

            enemy.x_change = -abs(
                enemy.speed
            )

        return enemy

    # ==================================================
    # SPAWN
    # ==================================================

    def spawn_enemies(self):
        self.enemies.clear()

        for _ in range(
            self.current_enemy_count
        ):

            self.enemies.append(
                self.create_enemy()
            )

    # ==================================================
    # UPDATE & DRAW
    # ==================================================

    def update(self):
        for enemy in self.enemies:

            enemy.update()

    # ==================================================
    # ENEMY SHOOT
    # ==================================================

    def try_shoot(
        self,
        bullet_manager
    ):

        # Không có Enemy
        if not self.enemies:

            return

        # Không cho quá nhiều đạn Enemy
        if (
            len(bullet_manager.enemy_bullets)
            >= MAX_ENEMY_BULLETS
        ):

            return

        current_time = pygame.time.get_ticks()

        # Level càng cao bắn càng nhanh
        cooldown = max(
            350,
            ENEMY_SHOOT_COOLDOWN
            - (self.current_level - 1) * 100
        )

        # Chưa hết cooldown
        if (
            current_time
            - self.last_enemy_shot
            < cooldown
        ):

            return

        # Chọn ngẫu nhiên một Enemy để bắn
        enemy = random.choice(
            self.enemies
        )

        bullet_manager.shoot_enemy(
            enemy.rect.centerx,
            enemy.rect.bottom
        )

        self.last_enemy_shot = (
            current_time
        )

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):
        for enemy in self.enemies:

            enemy.draw(
                screen
            )

    # ==================================================
    # REMOVE
    # ==================================================

    def remove_enemy(
        self,
        enemy
    ):

        if enemy in self.enemies:

            self.enemies.remove(
                enemy
            )

    # ==================================================
    # RESPAWN
    # ==================================================

    def respawn(
        self,
        enemy
    ):

        # Enemy chết sẽ có cơ hội
        # biến thành loại Enemy mới
        if enemy in self.enemies:

            index = self.enemies.index(
                enemy
            )

            self.enemies[index] = (
                self.create_enemy()
            )

    # ==================================================
    # INCREASE DIFFICULTY
    # ==================================================

    def increase_difficulty(
        self,
        level
    ):

        self.current_level = max(
            1,
            level
        )

        # ==================================================
        # SPEED
        # ==================================================

        self.current_speed = (
            ENEMY_SPEED
            + (
                self.current_level - 1
            )
            * ENEMY_SPEED_INCREASE_PER_LEVEL
        )

        # Cập nhật Enemy đang tồn tại
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
        # ENEMY COUNT
        # ==================================================

        target_count = min(
            ENEMY_COUNT
            + (
                self.current_level - 1
            )
            * ENEMY_COUNT_INCREASE_PER_LEVEL,

            MAX_ENEMIES
        )

        self.current_enemy_count = (
            target_count
        )

        # Thêm Enemy nếu level yêu cầu nhiều hơn
        while (
            len(self.enemies)
            < self.current_enemy_count
        ):

            self.enemies.append(
                self.create_enemy()
            )

    # ==================================================
    # CHECK BOTTOM
    # ==================================================

    def has_enemy_reached_bottom(
        self,
        limit_y=GAME_OVER_Y
    ):

        return any(
            enemy.y > limit_y
            for enemy in self.enemies
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.current_level = 1

        self.current_speed = ENEMY_SPEED

        self.current_enemy_count = (
            ENEMY_COUNT
        )

        self.last_enemy_shot = 0

        self.spawn_enemies()
        
