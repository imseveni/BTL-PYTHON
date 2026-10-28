import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE
)


class Menu:
    def __init__(self):

        self.title_font = pygame.font.Font(
            None,
            72
        )

        self.font = pygame.font.Font(
            None,
            36
        )

    def draw(self, screen):

        # =========================
        # TITLE
        # =========================

        title = self.title_font.render(
            "SPACE INVADERS",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                200
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # =========================
        # START
        # =========================

        start = self.font.render(
            "Press ENTER to Play",
            True,
            WHITE
        )

        start_rect = start.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                330
            )
        )

        screen.blit(
            start,
            start_rect
        )

        # =========================
        # EXIT
        # =========================

        exit_text = self.font.render(
            "Press ESC to Exit",
            True,
            WHITE
        )

        exit_rect = exit_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                380
            )
        )

        screen.blit(
            exit_text,
            exit_rect
        )