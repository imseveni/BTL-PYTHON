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
            80
        )

        self.font = pygame.font.Font(
            None,
            48
        )

        self.normal_color = WHITE
        self.hover_color = (255, 255, 0)

        # ==========================================
        # BUTTON RECT
        # ==========================================

        button_width = 320
        button_height = 60

        center_x = SCREEN_WIDTH // 2

        self.play_rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height
        )

        self.play_rect.center = (
            center_x,
            int(SCREEN_HEIGHT * 0.58)
        )

        self.high_score_rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height
        )

        self.high_score_rect.center = (
            center_x,
            int(SCREEN_HEIGHT * 0.70)
        )

        self.quit_rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height
        )

        self.quit_rect.center = (
            center_x,
            int(SCREEN_HEIGHT * 0.82)
        )

    # ==========================================
    # DRAW BUTTON
    # ==========================================

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

    # ==========================================
    # DRAW MENU
    # ==========================================

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        # TITLE
        title = self.title_font.render(
            "SPACE INVADERS",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                int(SCREEN_HEIGHT * 0.35)
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # PLAY
        self.draw_button(
            screen,
            "PLAY",
            self.play_rect,
            mouse_pos
        )

        # HIGH SCORE
        self.draw_button(
            screen,
            "HIGH SCORE",
            self.high_score_rect,
            mouse_pos
        )

        # QUIT
        self.draw_button(
            screen,
            "QUIT",
            self.quit_rect,
            mouse_pos
        )

    # ==========================================
    # HANDLE CLICK
    # ==========================================

    def handle_click(self, mouse_pos):

        if self.play_rect.collidepoint(mouse_pos):
            return "PLAY"

        if self.high_score_rect.collidepoint(mouse_pos):
            return "HIGH_SCORE"

        if self.quit_rect.collidepoint(mouse_pos):
            return "QUIT"

        return None