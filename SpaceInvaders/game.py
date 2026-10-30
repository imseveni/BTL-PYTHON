import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND_IMAGE,
    ICON_IMAGE,
    GAME_OVER_Y,
    LEVEL_SCORE_STEP,
    STATE_MENU,
    STATE_PLAYING,
    STATE_PAUSED,
    STATE_GAME_OVER,
    BLACK,
    WHITE
)

from entities.player import Player

from managers.enemy_manager import EnemyManager
from managers.bullet_manager import BulletManager
from managers.sound_manager import SoundManager

from ui.menu import Menu
from ui.hud import HUD
from ui.game_over import GameOverUI

from utils.collision import check_collision


class Game:
    def __init__(self):

        # ==================================================
        # SCREEN
        # ==================================================

        self.screen = pygame.display.set_mode(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

        pygame.display.set_caption(
            "Space Invaders"
        )

        # ==================================================
        # ICON
        # ==================================================

        icon = pygame.image.load(
            str(ICON_IMAGE)
        ).convert_alpha()

        pygame.display.set_icon(
            icon
        )

        # ==================================================
        # BACKGROUND
        # ==================================================

        self.background = pygame.image.load(
            str(BACKGROUND_IMAGE)
        ).convert()

        # ==================================================
        # CLOCK
        # ==================================================

        self.clock = pygame.time.Clock()

        # ==================================================
        # FONT (tạo 1 lần, không tạo lại mỗi frame)
        # ==================================================

        self.pause_font = pygame.font.Font(
            None,
            64
        )

        self.pause_sub_font = pygame.font.Font(
            None,
            32
        )

        # ==================================================
        # GAME OBJECT
        # ==================================================

        self.player = Player()

        self.enemy_manager = EnemyManager()

        self.bullet_manager = BulletManager()

        self.sound_manager = SoundManager()

        # ==================================================
        # UI
        # ==================================================

        self.menu = Menu()

        self.hud = HUD()

        self.game_over_ui = GameOverUI()

        # ==================================================
        # GAME DATA
        # ==================================================

        self.score = 0

        self.level = 1

        # ==================================================
        # GAME STATE
        # ==================================================

        self.running = True

        self.state = STATE_MENU

        # ==================================================
        # MUSIC
        # ==================================================

        self.sound_manager.play_music()

    # ==================================================
    # CHANGE STATE
    # ==================================================

    def change_state(self, new_state):

        self.state = new_state

        # Dừng player khi rời khỏi trạng thái chơi,
        # tránh việc tàu tiếp tục trượt sau khi resume
        if new_state != STATE_PLAYING:

            self.player.stop()

    # ==================================================
    # START GAME
    # ==================================================

    def start_game(self):

        self.reset_game()

        self.change_state(
            STATE_PLAYING
        )

    # ==================================================
    # TOGGLE PAUSE
    # ==================================================

    def toggle_pause(self):

        if self.state == STATE_PLAYING:

            self.change_state(
                STATE_PAUSED
            )

        elif self.state == STATE_PAUSED:

            self.change_state(
                STATE_PLAYING
            )

    # ==================================================
    # HANDLE EVENTS
    # ==================================================
    #
    # Chỉ xử lý các phím "bấm một lần" (chuyển trạng thái).
    # Di chuyển và bắn được xử lý ở handle_player_input()
    # vì cần biết phím nào đang được GIỮ.

    def handle_events(self):

        for event in pygame.event.get():

            # ==========================================
            # QUIT
            # ==========================================

            if event.type == pygame.QUIT:

                self.running = False

                continue

            if event.type != pygame.KEYDOWN:

                continue

            # ==========================================
            # ESC: thoát ở mọi trạng thái
            # ==========================================

            if event.key == pygame.K_ESCAPE:

                self.running = False

                continue

            # ==========================================
            # MENU: ENTER để chơi
            # ==========================================

            if self.state == STATE_MENU:

                if event.key == pygame.K_RETURN:

                    self.start_game()

            # ==========================================
            # GAME OVER: R để chơi lại
            # ==========================================

            elif self.state == STATE_GAME_OVER:

                if event.key == pygame.K_r:

                    self.start_game()

            # ==========================================
            # PLAYING / PAUSED: P để tạm dừng / tiếp tục
            # ==========================================

            elif event.key == pygame.K_p:

                self.toggle_pause()

    # ==================================================
    # HANDLE PLAYER INPUT
    # ==================================================

    def handle_player_input(self):

        keys = pygame.key.get_pressed()

        left = (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        )

        right = (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        )

        # Giữ cả 2 phím hoặc không giữ phím nào: đứng yên
        if left and not right:

            self.player.move_left()

        elif right and not left:

            self.player.move_right()

        else:

            self.player.stop()

        # Giữ SPACE để bắn liên tục (BulletManager có cooldown)
        if keys[pygame.K_SPACE]:

            shot = self.bullet_manager.shoot(
                self.player.rect.centerx,
                self.player.rect.top
            )

            # Chỉ phát sound nếu thực sự bắn
            if shot:

                self.sound_manager.play_shoot()

    # ==================================================
    # HANDLE BULLET - ENEMY COLLISION
    # ==================================================

    def handle_bullet_enemy_collision(self):

        for enemy in self.enemy_manager.enemies:

            for bullet in self.bullet_manager.bullets[:]:

                if check_collision(
                    enemy,
                    bullet
                ):

                    # Xóa bullet
                    self.bullet_manager.remove(
                        bullet
                    )

                    # Enemy nhận damage
                    dead = enemy.take_damage()

                    # Enemy chết
                    if dead:

                        self.sound_manager.play_explosion()

                        # Cộng điểm
                        self.score += enemy.score

                        # Respawn
                        self.enemy_manager.respawn(
                            enemy
                        )

                    # Một bullet chỉ va chạm 1 enemy
                    break

    # ==================================================
    # ENEMY - PLAYER COLLISION
    # ==================================================

    def handle_enemy_player_collision(self):

        for enemy in self.enemy_manager.enemies:

            if check_collision(
                enemy,
                self.player
            ):

                damaged = self.player.take_damage()

                # Chỉ xử lý nếu thực sự mất máu
                if damaged:

                    self.sound_manager.play_explosion()

                    self.enemy_manager.respawn(
                        enemy
                    )

                    if self.player.lives <= 0:

                        self.change_state(
                            STATE_GAME_OVER
                        )

                        return

    # ==================================================
    # HANDLE COLLISION
    # ==================================================

    def handle_collisions(self):

        self.handle_bullet_enemy_collision()

        self.handle_enemy_player_collision()

    # ==================================================
    # UPDATE LEVEL
    # ==================================================

    def update_level(self):

        # Mỗi LEVEL_SCORE_STEP điểm = tăng 1 level

        new_level = (
            self.score // LEVEL_SCORE_STEP
        ) + 1

        if new_level > self.level:

            self.level = new_level

            self.enemy_manager.increase_difficulty(
                self.level
            )

    # ==================================================
    # CHECK GAME OVER
    # ==================================================

    def check_game_over(self):

        # Hết mạng
        if self.player.lives <= 0:

            self.change_state(
                STATE_GAME_OVER
            )

            return

        # Enemy xuống quá thấp
        for enemy in self.enemy_manager.enemies:

            if enemy.y > GAME_OVER_Y:

                self.change_state(
                    STATE_GAME_OVER
                )

                return

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        # MENU / PAUSED / GAME_OVER: đứng yên, không update logic
        if self.state != STATE_PLAYING:
            return

        # Input (giữ phím)
        self.handle_player_input()

        # Player
        self.player.update()

        # Enemy
        self.enemy_manager.update()

        # Bullet
        self.bullet_manager.update()

        # Collision
        self.handle_collisions()

        # Level
        self.update_level()

        # Game Over
        self.check_game_over()

    # ==================================================
    # DRAW PAUSE
    # ==================================================

    def draw_pause(self):

        text = self.pause_font.render(
            "PAUSED",
            True,
            WHITE
        )

        rect = text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )
        )

        self.screen.blit(
            text,
            rect
        )

        sub_text = self.pause_sub_font.render(
            "Press P to continue",
            True,
            WHITE
        )

        sub_rect = sub_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 60
            )
        )

        self.screen.blit(
            sub_text,
            sub_rect
        )

    # ==================================================
    # DRAW GAME
    # ==================================================

    def draw_game(self):

        # Player
        self.player.draw(
            self.screen
        )

        # Enemy
        self.enemy_manager.draw(
            self.screen
        )

        # Bullet
        self.bullet_manager.draw(
            self.screen
        )

        # HUD
        self.hud.draw(
            self.screen,
            self.score,
            self.player.lives,
            self.level
        )

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self):

        # Clear
        self.screen.fill(
            BLACK
        )

        # Background
        self.screen.blit(
            self.background,
            (0, 0)
        )

        # ==================================================
        # MENU
        # ==================================================

        if self.state == STATE_MENU:

            self.menu.draw(
                self.screen
            )

        # ==================================================
        # GAME
        # ==================================================

        else:

            self.draw_game()

            # Pause
            if self.state == STATE_PAUSED:

                self.draw_pause()

            # Game Over
            elif self.state == STATE_GAME_OVER:

                self.game_over_ui.draw(
                    self.screen,
                    self.score
                )

        pygame.display.flip()

    # ==================================================
    # RESET GAME
    # ==================================================

    def reset_game(self):

        self.score = 0

        self.level = 1

        self.player.reset()

        self.enemy_manager.reset()

        self.bullet_manager.reset()

    # ==================================================
    # GAME LOOP
    # ==================================================

    def run(self):

        while self.running:

            # FPS
            self.clock.tick(
                FPS
            )

            # 1. Events
            self.handle_events()

            # 2. Logic
            self.update()

            # 3. Render
            self.draw()
