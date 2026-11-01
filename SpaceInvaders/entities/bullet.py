import pygame

from config import SCREEN_HEIGHT


class Bullet:
    def __init__(
        self,
        image,
        x,
        y,
        speed,
        direction=-1,
        damage=1,
        color=None
    ):

        # ==================================================
        # BULLET DATA
        # ==================================================

        # -1: bay lên
        #  1: bay xuống
        self.direction = direction

        self.speed = speed

        self.damage = damage

        # ==================================================
        # IMAGE
        # ==================================================

        if image is not None:

            self.image = image

        else:

            # Nếu không có image thì tạo bullet đơn giản
            self.image = pygame.Surface(
                (4, 12)
            )

            if color is not None:

                self.image.fill(
                    color
                )

            else:

                # Player bullet
                if self.direction == -1:

                    self.image.fill(
                        (255, 230, 0)
                    )

                # Enemy bullet
                else:

                    self.image.fill(
                        (255, 80, 50)
                    )

        # ==================================================
        # RECT
        # ==================================================

        self.rect = self.image.get_rect()

        # Player bullet bay lên:
        # xuất hiện tại giữa phía trên Player
        if self.direction == -1:

            self.rect.midbottom = (
                int(x),
                int(y)
            )

        # Enemy bullet bay xuống:
        # xuất hiện tại giữa phía dưới Enemy
        else:

            self.rect.midtop = (
                int(x),
                int(y)
            )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        self.rect.y += (
            self.speed
            * self.direction
        )

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )

    # ==================================================
    # CHECK OUTSIDE
    # ==================================================

    def is_outside(
        self,
        screen_height=SCREEN_HEIGHT
    ):

        return (
            self.rect.bottom < 0
            or self.rect.top > screen_height
        )