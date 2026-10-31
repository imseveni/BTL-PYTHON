import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE
)


class PauseUI:
    def __init__(self):

        self.title_font = pygame.font.Font(
            None,
            72
        )

        self.font = pygame.font.Font(
            None,
            40
        )

        self.normal_color = WHITE
        self.hover_color = (255, 255, 0)

        # =========================
        # BUTTON
        # =========================

        button_width = 300
        button_height = 55

        center_x = SCREEN_WIDTH // 2

        # CONTINUE
        self.continue_rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height
        )

        self.continue_rect.center = (
            center_x,
            SCREEN_HEIGHT // 2 + 40
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
            SCREEN_HEIGHT // 2 + 110
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
            SCREEN_HEIGHT // 2 + 180
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

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        # =========================
        # OVERLAY TỐI
        # =========================

        overlay = pygame.Surface(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

        overlay.set_alpha(160)

        overlay.fill(
            (0, 0, 0)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # =========================
        # TITLE
        # =========================

        title = self.title_font.render(
            "PAUSED",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 70
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # =========================
        # BUTTONS
        # =========================

        self.draw_button(
            screen,
            "CONTINUE",
            self.continue_rect,
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

        if self.continue_rect.collidepoint(
            mouse_pos
        ):
            return "CONTINUE"

        if self.menu_rect.collidepoint(
            mouse_pos
        ):
            return "MENU"

        if self.quit_rect.collidepoint(
            mouse_pos
        ):
            return "QUIT"

        return None