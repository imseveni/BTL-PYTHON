import pygame

from config import (
    PLAYER_IMAGE,
    PLAYER_SPEED,
    PLAYER_LIVES,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_INVINCIBLE_TIME,
    SCREEN_WIDTH
)


class Player:
    def __init__(self):

        # =========================
        # IMAGE
        # =========================

        self.image = pygame.image.load(
            str(PLAYER_IMAGE)
        ).convert_alpha()

        # =========================
        # POSITION
        # =========================

        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y

        # =========================
        # MOVEMENT
        # =========================

        self.speed = PLAYER_SPEED

        self.x_change = 0

        # =========================
        # LIFE
        # =========================

        self.lives = PLAYER_LIVES

        # Thời điểm hết bất tử
        self.invincible_until = 0

        # =========================
        # RECT
        # =========================

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
    # UPDATE
    # ==================================================

    def update(self):

        self.x += self.x_change

        # Không cho đi ra trái
        if self.x < 0:
            self.x = 0

        # Không cho đi ra phải
        max_x = SCREEN_WIDTH - self.image.get_width()

        if self.x > max_x:
            self.x = max_x

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

        # Nếu đang bất tử
        if current_time < self.invincible_until:
            return False

        self.lives -= 1

        # Bất tử tạm thời
        self.invincible_until = (
            current_time
            + PLAYER_INVINCIBLE_TIME
        )

        self.reset_position()

        return True

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

        self.reset_position()