import pygame

from config import (
    WHITE,
    HEART_IMAGE,
    SCREEN_WIDTH
)


class HUD:
    def __init__(self):

        self.font = pygame.font.Font(
            None,
            32
        )

        self.heart_image = pygame.image.load(
            str(HEART_IMAGE)
        ).convert_alpha()

        self.heart_size = 24

        self.heart_image = pygame.transform.scale(
            self.heart_image,
            (
                self.heart_size,
                self.heart_size
            )
        )

    def draw(
        self,
        screen,
        score,
        lives,
        level
    ):

        # ==================================================
        # SCORE
        # ==================================================

        score_text = self.font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # ==================================================
        # LEVEL
        # ==================================================

        level_text = self.font.render(
            f"Level: {level}",
            True,
            WHITE
        )

        level_rect = level_text.get_rect(
            topright=(
                SCREEN_WIDTH - 10,
                10
            )
        )

        screen.blit(
            level_text,
            level_rect
        )

        # ==================================================
        # HEART
        # ==================================================

        spacing = 6

        total_width = (
            lives * self.heart_size
            + (lives - 1) * spacing
        )

        start_x = (
            SCREEN_WIDTH - total_width
        ) // 2

        y = 12

        for i in range(lives):

            x = start_x + i * (
                self.heart_size + spacing
            )

            screen.blit(
                self.heart_image,
                (
                    x,
                    y
                )
            )