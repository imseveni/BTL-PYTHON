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

        self.score_font = pygame.font.Font(
            None,
            42
        )

        self.font = pygame.font.Font(
            None,
            38
        )

        self.normal_color = WHITE
        self.hover_color = (255, 255, 0)

        # =========================
        # BUTTON
        # =========================

        button_width = 300
        button_height = 55

        center_x = SCREEN_WIDTH // 2

        # RESTART
        self.restart_rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height
        )

        self.restart_rect.center = (
            center_x,
            SCREEN_HEIGHT // 2 + 80
        )

        # MAIN MENU
        self.menu_rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height
        )

        self.menu_rect.center = (
            center_x,
            SCREEN_HEIGHT // 2 + 145
        )

        # QUIT
        self.quit_rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height
        )

        self.quit_rect.center = (
            center_x,
            SCREEN_HEIGHT // 2 + 210
        )

    # ==================================================
    # DRAW BUTTON
    # ==================================================

    def draw_button(
        self,
        screen,
        text,
        rect,
        mouse_pos
    ):

        if rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.normal_color

        text_surface = self.font.render(
            text,
            True,
            color
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    # ==================================================
    # DRAW
    # ==================================================

    def draw(
        self,
        screen,
        score
    ):

        mouse_pos = pygame.mouse.get_pos()

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
                SCREEN_HEIGHT // 2 - 100
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # =========================
        # SCORE
        # =========================

        score_text = self.score_font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        score_rect = score_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 15
            )
        )

        screen.blit(
            score_text,
            score_rect
        )

        # =========================
        # BUTTON
        # =========================

        self.draw_button(
            screen,
            "RESTART",
            self.restart_rect,
            mouse_pos
        )

        self.draw_button(
            screen,
            "MAIN MENU",
            self.menu_rect,
            mouse_pos
        )

        self.draw_button(
            screen,
            "QUIT",
            self.quit_rect,
            mouse_pos
        )

    # ==================================================
    # HANDLE CLICK
    # ==================================================

    def handle_click(self, mouse_pos):

        if self.restart_rect.collidepoint(
            mouse_pos
        ):
            return "RESTART"

        if self.menu_rect.collidepoint(
            mouse_pos
        ):
            return "MENU"

        if self.quit_rect.collidepoint(
            mouse_pos
        ):
            return "QUIT"

        return None