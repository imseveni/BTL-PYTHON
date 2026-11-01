import pygame

from config import (
    PLAYER_IMAGE,
    PLAYER_DEFENSE_IMAGE,
    PLAYER_SPEED,
    PLAYER_LIVES,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_INVINCIBLE_TIME,
    PLAYER_DEFENSE_TIME,
    SCREEN_WIDTH,
)


class Player:
    def __init__(self):

        # ==================================================
        # IMAGE
        # ==================================================

        self.base_image = pygame.image.load(
            str(PLAYER_IMAGE)
        ).convert_alpha()

        self.defense_image = pygame.image.load(
            str(PLAYER_DEFENSE_IMAGE)
        ).convert_alpha()

        # Giữ cùng kích thước Player
        self.defense_image = pygame.transform.scale(
            self.defense_image,
            self.base_image.get_size()
        )

        self.image = self.base_image

        # ==================================================
        # POSITION
        # ==================================================

        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y

        # ==================================================
        # MOVEMENT
        # ==================================================

        self.speed = PLAYER_SPEED

        self.x_change = 0

        # ==================================================
        # LIFE
        # ==================================================

        self.lives = PLAYER_LIVES

        # ==================================================
        # INVINCIBLE
        # ==================================================

        # Thời điểm hết bất tử
        self.invincible_until = 0

        # ==================================================
        # DEFENSE
        # ==================================================

        # Thời điểm khiên hết tác dụng
        self.defense_until = 0

        # ==================================================
        # RECT
        # ==================================================

        self.rect = self.image.get_rect()

        self.update_rect()

    # ==================================================
    # MOVE LEFT
    # ==================================================

    def move_left(self):

        self.x_change = -self.speed

    # ==================================================
    # MOVE RIGHT
    # ==================================================

    def move_right(self):

        self.x_change = self.speed

    # ==================================================
    # STOP
    # ==================================================

    def stop(self):

        self.x_change = 0

    # ==================================================
    # UPDATE RECT
    # ==================================================

    def update_rect(self):

        self.rect.topleft = (
            int(self.x),
            int(self.y)
        )

    # ==================================================
    # UPDATE EFFECT
    # ==================================================

    def update_effects(self):

        current_time = pygame.time.get_ticks()

        # Nếu Defense còn thời gian
        if current_time < self.defense_until:

            self.image = self.defense_image

        else:

            self.image = self.base_image

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        # Di chuyển
        self.x += self.x_change

        # Không cho đi khỏi cạnh trái
        if self.x < 0:

            self.x = 0

        # Không cho đi khỏi cạnh phải
        max_x = (
            SCREEN_WIDTH
            - self.image.get_width()
        )

        if self.x > max_x:

            self.x = max_x

        # Effect
        self.update_effects()

        # Rect
        self.update_rect()

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )

    # ==================================================
    # TAKE DAMAGE
    # ==================================================

    def take_damage(self):

        current_time = pygame.time.get_ticks()

        # ==================================================
        # ĐANG BẤT TỬ
        # ==================================================

        if current_time < self.invincible_until:

            return False

        # ==================================================
        # CÓ KHIÊN
        # ==================================================

        if current_time < self.defense_until:

            # Khiên chặn 1 lần va chạm
            self.defense_until = 0

            self.image = self.base_image

            # Trả True để Game biết va chạm đã được xử lý
            # và có thể respawn enemy
            return True

        # ==================================================
        # MẤT MÁU
        # ==================================================

        self.lives -= 1

        # Bất tử tạm thời
        self.invincible_until = (
            current_time
            + PLAYER_INVINCIBLE_TIME
        )

        self.reset_position()

        return True

    # ==================================================
    # TAKE ITEM
    # ==================================================

    def take_item(self, power_type):

        current_time = pygame.time.get_ticks()

        # ==================================================
        # HP
        # ==================================================

        if power_type == "HP":

            # Không vượt quá số mạng tối đa
            if self.lives < PLAYER_LIVES:

                self.lives += 1

        # ==================================================
        # DEFENSE
        # ==================================================

        elif power_type == "DEFENSE":

            self.defense_until = (
                current_time
                + PLAYER_DEFENSE_TIME
            )

            self.image = self.defense_image

    # ==================================================
    # RESET POSITION
    # ==================================================

    def reset_position(self):

        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y

        self.x_change = 0

        self.update_rect()

    # ==================================================
    # RESET PLAYER
    # ==================================================

    def reset(self):

        self.lives = PLAYER_LIVES

        self.invincible_until = 0

        self.defense_until = 0

        self.image = self.base_image

        self.reset_position()