import pygame


from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND_IMAGE,
    ICON_IMAGE,
    GAME_OVER_Y,
    BLACK,
    WHITE
)

from entities.player import Player
from entities.powerup import PowerUp
import random
from managers.power_up_manager import PowerUpManager
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
        # GAME OBJECT
        # ==================================================

        self.player = Player()

        self.enemy_manager = EnemyManager()

        self.bullet_manager = BulletManager()

        self.sound_manager = SoundManager()

        self.power_up_manager = PowerUpManager()
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

        self.state = "MENU"

        # ==================================================
        # MUSIC
        # ==================================================

        self.sound_manager.play_music()

    # ==================================================
    # HANDLE EVENTS
    # ==================================================

    def handle_events(self):

        for event in pygame.event.get():

            # ==========================================
            # QUIT
            # ==========================================

            if event.type == pygame.QUIT:

                self.running = False

            # ==========================================
            # KEY DOWN
            # ==========================================

            if event.type == pygame.KEYDOWN:

                # --------------------------------------
                # MENU
                # --------------------------------------

                if self.state == "MENU":

                    if event.key == pygame.K_RETURN:

                        self.reset_game()

                        self.state = "PLAYING"

                    elif event.key == pygame.K_ESCAPE:

                        self.running = False

                    continue

                # --------------------------------------
                # GAME OVER
                # --------------------------------------

                if self.state == "GAME_OVER":

                    if event.key == pygame.K_r:

                        self.reset_game()

                        self.state = "PLAYING"

                    elif event.key == pygame.K_ESCAPE:

                        self.running = False

                    continue

                # --------------------------------------
                # PAUSE
                # --------------------------------------

                if event.key == pygame.K_p:

                    if self.state == "PLAYING":

                        self.state = "PAUSED"

                        # self.player.stop()

                    elif self.state == "PAUSED":

                        self.state = "PLAYING"

                    continue

                # --------------------------------------
                # CHỈ XỬ LÝ GAMEPLAY KHI PLAYING
                # --------------------------------------

                if self.state != "PLAYING":
                    continue

                # LEFT
                # if (
                #     event.key == pygame.K_LEFT
                #     or event.key == pygame.K_a
                # ):

                #     self.player.move_left()

                # # RIGHT
                # elif (
                #     event.key == pygame.K_RIGHT
                #     or event.key == pygame.K_d
                # ):

                #     self.player.move_right()

                # SHOOT
                elif event.key == pygame.K_SPACE:

                    shot = self.bullet_manager.shoot(
                        self.player.rect.centerx,
                        self.player.rect.top
                    )

                    # Chỉ phát sound nếu thực sự bắn
                    if shot:
                        self.sound_manager.play_shoot()

                # ESC
                elif event.key == pygame.K_ESCAPE:

                    self.running = False

            # ==========================================
            # KEY UP
            # ==========================================

            # if event.type == pygame.KEYUP:

            #     if event.key in (
            #         pygame.K_LEFT,
            #         pygame.K_RIGHT,
            #         pygame.K_a,
            #         pygame.K_d
            #     ):

            #         self.player.stop()

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
                    # Nhan Item
                    n = random.randint(1, 10)
                    if(n == 8):
                        item = random.choice([
                            PowerUp('assets/images/health.png', enemy.x, enemy.y, 'HP'),
                            PowerUp('assets/images/shield.png', enemy.x, enemy.y, 'Defense')
                        ])
                        self.power_up_manager.powerups.append(item)

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

                        self.state = "GAME_OVER"

                        return

    # ==================================================
    # PLAYER - POWERUP COLLISION
    # ==================================================
    def handle_player_power_up_collision(self):
        for powerUp in self.power_up_manager.powerups:
            if check_collision(
                    powerUp,
                    self.player
                ):

                self.player.take_item(powerUp.details)
                self.power_up_manager.powerups.remove(powerUp)



    # ==================================================
    # HANDLE COLLISION
    # ==================================================

    def handle_collisions(self):

        self.handle_bullet_enemy_collision()

        self.handle_enemy_player_collision()

        self.handle_player_power_up_collision()

    # ==================================================
    # UPDATE LEVEL
    # ==================================================

    def update_level(self):

        # 100 điểm = tăng 1 level

        new_level = (
            self.score // 100
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

        for enemy in self.enemy_manager.enemies:

            if enemy.y > GAME_OVER_Y:

                self.state = "GAME_OVER"

                # self.player.stop()

                return

        if self.player.lives <= 0:

            self.state = "GAME_OVER"

            # self.player.stop()

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if self.state != "PLAYING":
            return

        # Player
        self.player.update()

        # Enemy
        self.enemy_manager.update()

        # Bullet
        self.bullet_manager.update()

        # Collision
        self.handle_collisions()

        # PowerUp 
        self.power_up_manager.update()

        # Level
        self.update_level()

        # Game Over
        self.check_game_over()

    # ==================================================
    # DRAW PAUSE
    # ==================================================

    def draw_pause(self):

        font = pygame.font.Font(
            None,
            64
        )

        text = font.render(
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

        sub_font = pygame.font.Font(
            None,
            32
        )

        sub_text = sub_font.render(
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

        # PowerUP
        self.power_up_manager.draw(self.screen)

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

        if self.state == "MENU":

            self.menu.draw(
                self.screen
            )

        # ==================================================
        # GAME
        # ==================================================

        else:

            self.draw_game()

            # Pause
            if self.state == "PAUSED":

                self.draw_pause()

            # Game Over
            elif self.state == "GAME_OVER":

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

        self.power_up_manager.reset()

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