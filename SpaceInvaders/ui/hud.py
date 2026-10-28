import pygame

from config import WHITE


class HUD:
    def __init__(self):

        self.font = pygame.font.Font(
            None,
            36
        )

    def draw(
        self,
        screen,
        score,
        lives,
        level
    ):

        # =========================
        # SCORE
        # =========================

        score_text = self.font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # =========================
        # LIVES
        # =========================

        lives_text = self.font.render(
            f"Lives: {lives}",
            True,
            WHITE
        )

        screen.blit(
            lives_text,
            (310, 10)
        )

        # =========================
        # LEVEL
        # =========================

        level_text = self.font.render(
            f"Level: {level}",
            True,
            WHITE
        )

        screen.blit(
            level_text,
            (650, 10)
        )