import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE
)


class GameOverUI:
    def __init__(self):

        self.title_font = pygame.font.Font(
            None,
            72
        )

        self.font = pygame.font.Font(
            None,
            36
        )

    def draw(
        self,
        screen,
        score
    ):

        # =========================
        # GAME OVER
        # =========================

        title = self.title_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 80
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # =========================
        # SCORE
        # =========================

        score_text = self.font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        score_rect = score_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )
        )

        screen.blit(
            score_text,
            score_rect
        )

        # =========================
        # RESTART
        # =========================

        restart_text = self.font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        restart_rect = restart_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 60
            )
        )

        screen.blit(
            restart_text,
            restart_rect
        )