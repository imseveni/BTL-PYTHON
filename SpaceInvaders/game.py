import random

import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,

    BACKGROUND_IMAGE,
    ICON_IMAGE,

    HEALTH_POWERUP_IMAGE,
    SHIELD_POWERUP_IMAGE,

    GAME_OVER_Y,
    HIGH_SCORE_FILE,
    LEVEL_SCORE_STEP,

    STATE_MENU,
    STATE_PLAYING,
    STATE_PAUSED,
    STATE_GAME_OVER,
    STATE_HIGH_SCORE,

    BLACK,
)

from entities.player import Player
from entities.powerup import PowerUp

from managers.enemy_manager import EnemyManager
from managers.bullet_manager import BulletManager
from managers.powerup_manager import PowerUpManager
from managers.sound_manager import SoundManager

from ui.menu import Menu
from ui.hud import HUD
from ui.pause import PauseUI
from ui.game_over import GameOverUI
from ui.high_score import HighScoreUI

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
        # POWERUP IMAGE
        # ==================================================

        self.health_powerup_image = pygame.image.load(
            str(HEALTH_POWERUP_IMAGE)
        ).convert_alpha()

        self.shield_powerup_image = pygame.image.load(
            str(SHIELD_POWERUP_IMAGE)
        ).convert_alpha()

        # ==================================================
        # CLOCK
        # ==================================================

        self.clock = pygame.time.Clock()

        # ==================================================
        # GAME OBJECT
        # ==================================================

        self.player = Player()

        self.enemy_manager = EnemyManager()

        self.bullet_manager = BulletManager()

        self.power_up_manager = PowerUpManager()

        self.sound_manager = SoundManager()

        # ==================================================
        # UI
        # ==================================================

        self.menu = Menu()

        self.hud = HUD()

        self.pause_ui = PauseUI()

        self.game_over_ui = GameOverUI()

        self.high_score_ui = HighScoreUI()

        # ==================================================
        # GAME DATA
        # ==================================================

        self.score = 0

        self.level = 1

        self.high_score = self.load_high_score()

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

        # Khi rời khỏi PLAYING
        # thì dừng Player
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
    # END GAME
    # ==================================================

    def end_game(self):

        self.update_high_score()

        self.change_state(
            STATE_GAME_OVER
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

    def handle_events(self):

        for event in pygame.event.get():

            # ==================================================
            # QUIT WINDOW
            # ==================================================

            if event.type == pygame.QUIT:

                self.running = False

                continue

            # ==================================================
            # MENU
            # ==================================================

            if self.state == STATE_MENU:

                # -------------------------
                # KEYBOARD
                # -------------------------

                if event.type == pygame.KEYDOWN:

                    # ENTER -> PLAY
                    if event.key == pygame.K_RETURN:

                        self.start_game()

                    # ESC -> QUIT
                    elif event.key == pygame.K_ESCAPE:

                        self.running = False

                # -------------------------
                # MOUSE
                # -------------------------

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        action = self.menu.handle_click(
                            event.pos
                        )

                        if action == "PLAY":

                            self.start_game()

                        elif action == "HIGH_SCORE":

                            self.change_state(
                                STATE_HIGH_SCORE
                            )

                        elif action == "QUIT":

                            self.running = False

                continue

            # ==================================================
            # HIGH SCORE
            # ==================================================

            if self.state == STATE_HIGH_SCORE:

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        self.change_state(
                            STATE_MENU
                        )

                continue

            # ==================================================
            # GAME OVER
            # ==================================================

            if self.state == STATE_GAME_OVER:

                # -------------------------
                # KEYBOARD
                # -------------------------

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:

                        self.start_game()

                    elif event.key == pygame.K_m:

                        self.change_state(
                            STATE_MENU
                        )

                    elif event.key == pygame.K_ESCAPE:

                        self.running = False

                # -------------------------
                # MOUSE
                # -------------------------

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        action = (
                            self.game_over_ui.handle_click(
                                event.pos
                            )
                        )

                        if action == "RESTART":

                            self.start_game()

                        elif action == "MENU":

                            self.change_state(
                                STATE_MENU
                            )

                        elif action == "QUIT":

                            self.running = False

                continue

            # ==================================================
            # PAUSED
            # ==================================================

            if self.state == STATE_PAUSED:

                # -------------------------
                # KEYBOARD
                # -------------------------

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_p:

                        self.toggle_pause()

                    elif event.key == pygame.K_m:

                        self.change_state(
                            STATE_MENU
                        )

                    elif event.key == pygame.K_ESCAPE:

                        self.running = False

                # -------------------------
                # MOUSE
                # -------------------------

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        action = self.pause_ui.handle_click(
                            event.pos
                        )

                        if action == "CONTINUE":

                            self.change_state(
                                STATE_PLAYING
                            )

                        elif action == "MENU":

                            self.change_state(
                                STATE_MENU
                            )

                        elif action == "QUIT":

                            self.running = False

                continue

            # ==================================================
            # PLAYING
            # ==================================================

            if self.state == STATE_PLAYING:

                if event.type == pygame.KEYDOWN:

                    # P -> Pause
                    if event.key == pygame.K_p:

                        self.toggle_pause()

                    # ESC -> Quit
                    elif event.key == pygame.K_ESCAPE:

                        self.running = False

    # ==================================================
    # HANDLE PLAYER INPUT
    # ==================================================

    def handle_player_input(self):

        keys = pygame.key.get_pressed()

        # ==================================================
        # MOVEMENT
        # ==================================================

        left = (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        )

        right = (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        )

        if left and not right:

            self.player.move_left()

        elif right and not left:

            self.player.move_right()

        else:

            self.player.stop()

        # ==================================================
        # SHOOT
        # ==================================================

        if keys[pygame.K_SPACE]:

            shot = self.bullet_manager.shoot(
                self.player.rect.centerx,
                self.player.rect.top
            )

            if shot:

                self.sound_manager.play_shoot()

    # ==================================================
    # CREATE POWERUP
    # ==================================================

    def create_random_powerup(
        self,
        x,
        y
    ):

        # 10% khả năng xuất hiện PowerUp
        if random.randint(1, 10) != 8:

            return

        power_type = random.choice(
            [
                "HP",
                "DEFENSE"
            ]
        )

        if power_type == "HP":

            image = self.health_powerup_image

        else:

            image = self.shield_powerup_image

        powerup = PowerUp(
            image=image,
            x=x,
            y=y,
            power_type=power_type
        )

        self.power_up_manager.add(
            powerup
        )

    # ==================================================
    # BULLET - ENEMY COLLISION
    # ==================================================

    def handle_bullet_enemy_collision(self):

        for enemy in self.enemy_manager.enemies:

            for bullet in self.bullet_manager.bullets[:]:

                if check_collision(
                    enemy,
                    bullet
                ):

                    # ======================================
                    # REMOVE BULLET
                    # ======================================

                    self.bullet_manager.remove(
                        bullet
                    )

                    # ======================================
                    # DAMAGE ENEMY
                    # ======================================

                    dead = enemy.take_damage()

                    # ======================================
                    # ENEMY DEAD
                    # ======================================

                    if dead:

                        # Lưu vị trí trước khi respawn
                        enemy_x = enemy.rect.centerx
                        enemy_y = enemy.rect.centery

                        # ------------------------------
                        # SOUND
                        # ------------------------------

                        self.sound_manager.play_explosion()

                        # ------------------------------
                        # EXPLOSION
                        # ------------------------------

                        self.bullet_manager.add_explosion(
                            enemy_x,
                            enemy_y
                        )

                        # ------------------------------
                        # SCORE
                        # ------------------------------

                        self.score += enemy.score

                        # ------------------------------
                        # POWERUP
                        # ------------------------------

                        self.create_random_powerup(
                            enemy_x,
                            enemy_y
                        )

                        # ------------------------------
                        # RESPAWN
                        # ------------------------------

                        self.enemy_manager.respawn(
                            enemy
                        )

                    # Một bullet chỉ hit một enemy
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

                # take_damage() = False
                # khi Player đang bất tử
                if damaged:

                    # Lưu vị trí trước respawn
                    enemy_x = enemy.rect.centerx
                    enemy_y = enemy.rect.centery

                    # Sound
                    self.sound_manager.play_explosion()

                    # Explosion
                    self.bullet_manager.add_explosion(
                        enemy_x,
                        enemy_y
                    )

                    # Respawn enemy
                    self.enemy_manager.respawn(
                        enemy
                    )

                    # Player hết mạng
                    if self.player.lives <= 0:

                        self.end_game()

                        return

    # ==================================================
    # ENEMY BULLET - PLAYER COLLISION
    # ==================================================

    def handle_enemy_bullet_player_collision(
        self
    ):

        for bullet in (
            self.bullet_manager.enemy_bullets[:]
        ):

            if check_collision(
                bullet,
                self.player
            ):

                # Đạn chạm Player thì biến mất
                self.bullet_manager.remove_enemy_bullet(
                    bullet
                )

                # Lưu lives trước khi damage
                old_lives = self.player.lives

                damaged = self.player.take_damage()

                # Player đang bất tử
                if not damaged:

                    continue

                # Nếu thực sự mất mạng
                if self.player.lives < old_lives:

                    self.sound_manager.play_explosion()

                    self.bullet_manager.add_explosion(
                        self.player.rect.centerx,
                        self.player.rect.centery
                    )

                # Hết mạng
                if self.player.lives <= 0:

                    self.end_game()

                    return

    # ==================================================
    # PLAYER - POWERUP COLLISION
    # ==================================================

    def handle_player_powerup_collision(self):

        # Dùng copy vì sẽ xóa PowerUp
        for powerup in self.power_up_manager.powerups[:]:

            if check_collision(
                powerup,
                self.player
            ):

                # Player nhận item
                self.player.take_item(
                    powerup.power_type
                )

                # Xóa item sau khi nhận
                self.power_up_manager.remove(
                    powerup
                )

    # ==================================================
    # HANDLE COLLISIONS
    # ==================================================

    def handle_collisions(self):

        # ==================================================
        # PLAYER BULLET -> ENEMY
        # ==================================================

        self.handle_bullet_enemy_collision()

        if self.state != STATE_PLAYING:

            return

        # ==================================================
        # ENEMY -> PLAYER
        # ==================================================

        self.handle_enemy_player_collision()

        if self.state != STATE_PLAYING:

            return

        # ==================================================
        # ENEMY BULLET -> PLAYER
        # ==================================================

        self.handle_enemy_bullet_player_collision()

        if self.state != STATE_PLAYING:

            return

        # ==================================================
        # PLAYER -> POWERUP
        # ==================================================

        self.handle_player_powerup_collision()

    # ==================================================
    # UPDATE LEVEL
    # ==================================================

    def update_level(self):

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

        # ==================================================
        # PLAYER HẾT MẠNG
        # ==================================================

        if self.player.lives <= 0:

            self.end_game()

            return

        # ==================================================
        # ENEMY XUỐNG QUÁ THẤP
        # ==================================================

        if self.enemy_manager.has_enemy_reached_bottom():

            self.end_game()

            return

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if self.state != STATE_PLAYING:

            return

        # ==================================================
        # INPUT
        # ==================================================

        self.handle_player_input()

        # ==================================================
        # PLAYER
        # ==================================================

        self.player.update()

        # ==================================================
        # ENEMY
        # ==================================================

        self.enemy_manager.update()

        # Enemy thử bắn
        self.enemy_manager.try_shoot(
            self.bullet_manager
        )

        # ==================================================
        # BULLET + EXPLOSION
        # ==================================================

        self.bullet_manager.update()

        # ==================================================
        # POWERUP
        # ==================================================

        self.power_up_manager.update()

        # ==================================================
        # COLLISION
        # ==================================================

        self.handle_collisions()

        # Collision có thể làm Game Over
        if self.state != STATE_PLAYING:

            return

        # ==================================================
        # LEVEL
        # ==================================================

        self.update_level()

        # ==================================================
        # GAME OVER
        # ==================================================

        self.check_game_over()

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

        # Bullet + Explosion
        self.bullet_manager.draw(
            self.screen
        )

        # PowerUp
        self.power_up_manager.draw(
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

        # ==================================================
        # CLEAR
        # ==================================================

        self.screen.fill(
            BLACK
        )

        # ==================================================
        # BACKGROUND
        # ==================================================

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
        # HIGH SCORE
        # ==================================================

        elif self.state == STATE_HIGH_SCORE:

            self.high_score_ui.draw(
                self.screen,
                self.high_score
            )

        # ==================================================
        # GAME
        # ==================================================

        else:

            self.draw_game()

            # ==============================================
            # PAUSED
            # ==============================================

            if self.state == STATE_PAUSED:

                self.pause_ui.draw(
                    self.screen
                )

            # ==============================================
            # GAME OVER
            # ==============================================

            elif self.state == STATE_GAME_OVER:

                self.game_over_ui.draw(
                    self.screen,
                    self.score
                )

        # ==================================================
        # UPDATE DISPLAY
        # ==================================================

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

        self.power_up_manager.reset()

    # ==================================================
    # LOAD HIGH SCORE
    # ==================================================

    def load_high_score(self):

        try:

            with open(
                HIGH_SCORE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read().strip()

                if content == "":

                    return 0

                return int(content)

        except (
            FileNotFoundError,
            ValueError
        ):

            return 0

    # ==================================================
    # SAVE HIGH SCORE
    # ==================================================

    def save_high_score(self):

        HIGH_SCORE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            HIGH_SCORE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                str(self.high_score)
            )

    # ==================================================
    # UPDATE HIGH SCORE
    # ==================================================

    def update_high_score(self):

        if self.score > self.high_score:

            self.high_score = self.score

            self.save_high_score()

    # ==================================================
    # GAME LOOP
    # ==================================================

    def run(self):

        while self.running:

            # FPS
            self.clock.tick(
                FPS
            )

            # Events
            self.handle_events()

            # Logic
            self.update()

            # Render
            self.draw()