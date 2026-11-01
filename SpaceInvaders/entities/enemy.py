import pygame

from config import (
    SCREEN_WIDTH,

    NORMAL_ENEMY_SCORE,
    FAST_ENEMY_SCORE,
    TANK_ENEMY_SCORE,

    FAST_ENEMY_SPEED_MULTIPLIER,
    TANK_ENEMY_SPEED_MULTIPLIER,

    TANK_ENEMY_HEALTH,
)


class Enemy:
    """Class cơ sở (Base Class) đại diện cho một Enemy trong game."""

    def __init__(
        self,
        image,
        x,
        y,
        speed,
        drop_distance,
        health=1,
        score=NORMAL_ENEMY_SCORE,
        enemy_type="normal",
        speed_multiplier=1.0,
    ):

        # ==================================================
        # IMAGE
        # ==================================================

        self.image = image
        self.x = float(x)
        self.y = float(y)

        # ==================================================
        # POSITION
        # ==================================================

        self.x = float(x)
        self.y = float(y)

        # ==================================================
        # TYPE
        # ==================================================

        self.enemy_type = enemy_type

        # ==================================================
        # SPEED
        # ==================================================

        self.speed_multiplier = speed_multiplier

        self.base_speed = speed

        self.speed = (
            self.base_speed
            * self.speed_multiplier
        )

        self.x_change = self.speed

        self.x_change = self.speed
        self.drop_distance = drop_distance

        # ==================================================
        # HEALTH
        # ==================================================

        self.health = health
        self.max_health = health

        # ==================================================
        # SCORE
        # ==================================================

        self.score = score

        # ==================================================
        # RECT
        # ==================================================

        self.rect = self.image.get_rect()
        self.update_rect()

    @staticmethod
    def tint_image(image, tint_color):
        """Tạo bản sao ảnh có phủ màu để phân biệt các loại Enemy trên màn hình."""
        tinted = image.copy()
        tinted.fill(tint_color, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted

    # ==================================================
    # UPDATE RECT
    # ==================================================

    def update_rect(self):
        self.rect.topleft = (int(self.x), int(self.y))

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):
        self.x += self.x_change

        max_x = (
            SCREEN_WIDTH
            - self.image.get_width()
        )

        # Chạm biên trái
        if self.x <= 0:
            self.x = 0
            self.x_change = abs(self.speed)
            self.y += self.drop_distance

        # Chạm biên phải
        elif self.x >= max_x:
            self.x = max_x
            self.x_change = -abs(self.speed)
            self.y += self.drop_distance

        self.update_rect()

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

        # Vẽ thanh máu nếu Enemy có nhiều hơn 1 HP (ví dụ: TankEnemy)
        if self.max_health > 1:
            self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = self.image.get_width()
        bar_height = 5
        bar_x = int(self.x)
        bar_y = max(0, int(self.y) - 8)

        health_ratio = max(0, self.health / self.max_health)
        current_bar_width = int(bar_width * health_ratio)

        # Nền đỏ (máu đã mất) và thanh xanh lá (máu hiện tại)
        pygame.draw.rect(
            screen, (180, 40, 40), (bar_x, bar_y, bar_width, bar_height)
        )
        pygame.draw.rect(
            screen, (40, 220, 80), (bar_x, bar_y, current_bar_width, bar_height)
        )

        # Chỉ Tank hoặc enemy nhiều HP mới hiện thanh máu
        if self.max_health > 1:

            self.draw_health_bar(
                screen
            )

    # ==================================================
    # HEALTH BAR
    # ==================================================

    def draw_health_bar(self, screen):

        bar_width = self.image.get_width()

        bar_height = 5

        bar_x = int(self.x)

        bar_y = max(
            0,
            int(self.y) - 8
        )

        health_ratio = max(
            0,
            self.health / self.max_health
        )

        current_bar_width = int(
            bar_width
            * health_ratio
        )

        # Nền đỏ
        pygame.draw.rect(
            screen,
            (180, 40, 40),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            )
        )

        # Máu hiện tại
        pygame.draw.rect(
            screen,
            (40, 220, 80),
            (
                bar_x,
                bar_y,
                current_bar_width,
                bar_height
            )
        )

    # ==================================================
    # TAKE DAMAGE
    # ==================================================

    def take_damage(
        self,
        damage=1
    ):

        self.health -= damage
        return self.health <= 0

    # ==================================================
    # RESPAWN
    # ==================================================

    def respawn(
        self,
        x,
        y
    ):

        self.x = float(x)
        self.y = float(y)

        self.health = self.max_health
        self.update_rect()

    # ==================================================
    # SET SPEED
    # ==================================================

    def set_speed(
        self,
        new_base_speed
    ):

        # Tốc độ gốc tăng theo level
        self.base_speed = new_base_speed

        # Mỗi loại giữ multiplier riêng
        self.speed = (
            self.base_speed
            * self.speed_multiplier
        )

        # Giữ nguyên hướng
        if self.x_change >= 0:

            self.x_change = abs(
                self.speed
            )

        else:

            self.x_change = -abs(
                self.speed
            )


# ==================================================
# NORMAL ENEMY
# ==================================================

class NormalEnemy(Enemy):
    def __init__(
        self,
        image,
        x,
        y,
        speed,
        drop_distance
    ):

        super().__init__(
            image=image,
            x=x,
            y=y,
            speed=speed,
            drop_distance=drop_distance,

            health=1,
            score=NORMAL_ENEMY_SCORE,

            enemy_type="normal",

            speed_multiplier=1.0
        )


# ==================================================
# FAST ENEMY
# ==================================================

class FastEnemy(Enemy):
    def __init__(
        self,
        image,
        x,
        y,
        speed,
        drop_distance
    ):

        super().__init__(
            image=image,
            x=x,
            y=y,
            speed=speed,
            drop_distance=drop_distance,

            health=1,
            score=FAST_ENEMY_SCORE,

            enemy_type="fast",

            speed_multiplier=(
                FAST_ENEMY_SPEED_MULTIPLIER
            )
        )


# ==================================================
# TANK ENEMY
# ==================================================

class TankEnemy(Enemy):
    def __init__(
        self,
        image,
        x,
        y,
        speed,
        drop_distance
    ):

        super().__init__(
            image=image,
            x=x,
            y=y,
            speed=speed,
            drop_distance=drop_distance,

            health=TANK_ENEMY_HEALTH,
            score=TANK_ENEMY_SCORE,

            enemy_type="tank",

            speed_multiplier=(
                TANK_ENEMY_SPEED_MULTIPLIER
            )
        )