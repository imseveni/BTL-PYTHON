import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE
)


class HighScoreUI:
    def __init__(self):

        self.title_font = pygame.font.Font(
            None,
            72
        )

        self.score_font = pygame.font.Font(
            None,
            56
        )

        self.info_font = pygame.font.Font(
            None,
            32
        )

    def draw(self, screen, high_score):

        # TITLE
        title = self.title_font.render(
            "HIGH SCORE",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 120
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # SCORE
        score_text = self.score_font.render(
            str(high_score),
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

        # BACK
        back_text = self.info_font.render(
            "Press ESC to return",
            True,
            WHITE
        )

        back_rect = back_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 100
            )
        )

        screen.blit(
            back_text,
            back_rect
        )