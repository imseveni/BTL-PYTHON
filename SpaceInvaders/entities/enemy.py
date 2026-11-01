import pygame
from config import SCREEN_WIDTH, NORMAL_ENEMY_SCORE


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
            speed_multiplier=1.0
    ):
        self.image = image
        self.x = float(x)
        self.y = float(y)

        self.enemy_type = enemy_type
        self.speed_multiplier = speed_multiplier
        self.base_speed = speed
        self.speed = speed * self.speed_multiplier

        self.x_change = self.speed
        self.drop_distance = drop_distance

        self.health = health
        self.max_health = health
        self.score = score

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
        max_x = SCREEN_WIDTH - self.image.get_width()

        # Chạm biên trái -> đổi hướng sang phải và đi xuống
        if self.x <= 0:
            self.x = 0
            self.x_change = abs(self.speed)
            self.y += self.drop_distance

        # Chạm biên phải -> đổi hướng sang trái và đi xuống
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

    # ==================================================
    # TAKE DAMAGE
    # ==================================================

    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0

    # ==================================================
    # RESPAWN
    # ==================================================

    def respawn(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.health = self.max_health
        self.update_rect()

    # ==================================================
    # SET SPEED
    # ==================================================

    def set_speed(self, new_base_speed):
        self.base_speed = new_base_speed
        self.speed = new_base_speed * self.speed_multiplier

        # Giữ nguyên hướng di chuyển hiện tại
        if self.x_change >= 0:
            self.x_change = abs(self.speed)
        else:
            self.x_change = -abs(self.speed)


# ==================================================
# CÁC LOẠI ENEMY KẾ THỪA TỪ CLASS ENEMY (OOP)
# ==================================================


class NormalEnemy(Enemy):
    """Enemy cơ bản: HP = 1, Tốc độ bình thường, Điểm = 10."""

    def __init__(self, image, x, y, speed, drop_distance):
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


class FastEnemy(Enemy):
    """Enemy tốc độ cao: HP = 1, Tốc độ nhanh (x1.35), Điểm = 20."""

    def __init__(self, image, x, y, speed, drop_distance):
        fast_image = self.tint_image(image, (120, 240, 255))
        super().__init__(
            image=fast_image,
            x=x,
            y=y,
            speed=speed,
            drop_distance=drop_distance,
            health=1,
            score=20,
            enemy_type="fast",
            speed_multiplier=1.35
        )


class TankEnemy(Enemy):
    """Enemy trâu máu: HP = 3, Tốc độ chậm (x0.75), Điểm = 30."""

    def __init__(self, image, x, y, speed, drop_distance):
        tank_image = self.tint_image(image, (255, 130, 100))
        super().__init__(
            image=tank_image,
            x=x,
            y=y,
            speed=speed,
            drop_distance=drop_distance,
            health=3,
            score=30,
            enemy_type="tank",
            speed_multiplier=0.75
        )