import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND_IMAGE,
    ICON_IMAGE,
    GAME_OVER_Y,
<<<<<<< HEAD
    LEVEL_SCORE_STEP,
=======
    HIGH_SCORE_FILE,
    LEVEL_SCORE_STEP,

>>>>>>> 4159d45 (Upload)
    STATE_MENU,
    STATE_PLAYING,
    STATE_PAUSED,
    STATE_GAME_OVER,
<<<<<<< HEAD
=======
    STATE_HIGH_SCORE,

>>>>>>> 4159d45 (Upload)
    BLACK,
)


from entities.player import Player

from managers.enemy_manager import EnemyManager
from managers.bullet_manager import BulletManager
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

<<<<<<< HEAD
        # Dừng player khi rời khỏi trạng thái chơi,
        # tránh việc tàu tiếp tục trượt sau khi resume
        if new_state != STATE_PLAYING:

=======
        # Khi rời khỏi PLAYING
        # thì dừng chuyển động của Player
        if new_state != STATE_PLAYING:
>>>>>>> 4159d45 (Upload)
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
<<<<<<< HEAD
=======
    # END GAME
    # ==================================================

    def end_game(self):

        # Kiểm tra và lưu High Score
        self.update_high_score()

        self.change_state(
            STATE_GAME_OVER
        )

    # ==================================================
>>>>>>> 4159d45 (Upload)
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

            # ==================================================
            # QUIT WINDOW
            # ==================================================

            if event.type == pygame.QUIT:

                self.running = False

                continue

<<<<<<< HEAD
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
=======
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

                    # Chuột trái
                    if event.button == 1:

                        action = self.menu.handle_click(
                            event.pos
                        )

                        # PLAY
                        if action == "PLAY":

                            self.start_game()

                        # HIGH SCORE
                        elif action == "HIGH_SCORE":

                            self.change_state(
                                STATE_HIGH_SCORE
                            )

                        # QUIT
                        elif action == "QUIT":

                            self.running = False

                continue

            # ==================================================
            # HIGH SCORE
            # ==================================================

            if self.state == STATE_HIGH_SCORE:

                if event.type == pygame.KEYDOWN:

                    # ESC -> quay về Menu
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

                    # R -> Restart
                    if event.key == pygame.K_r:

                        self.start_game()

                    # M -> Main Menu
                    elif event.key == pygame.K_m:

                        self.change_state(
                            STATE_MENU
                        )

                    # ESC -> Quit
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

                        # Restart
                        if action == "RESTART":

                            self.start_game()

                        # Main Menu
                        elif action == "MENU":

                            self.change_state(
                                STATE_MENU
                            )

                        # Quit
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

                    # P -> Continue
                    if event.key == pygame.K_p:

                        self.toggle_pause()

                    # M -> Main Menu
                    elif event.key == pygame.K_m:

                        self.change_state(
                            STATE_MENU
                        )

                    # ESC -> Quit
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

                        # Continue
                        if action == "CONTINUE":

                            self.change_state(
                                STATE_PLAYING
                            )

                        # Main Menu
                        elif action == "MENU":

                            self.change_state(
                                STATE_MENU
                            )

                        # Quit
                        elif action == "QUIT":

                            self.running = False

                continue

            # ==================================================
            # PLAYING
            # ==================================================

            if self.state == STATE_PLAYING:

                # Các phím di chuyển và SPACE
                # được xử lý bằng pygame.key.get_pressed()
                # trong handle_player_input()

                if event.type == pygame.KEYDOWN:

                    # P -> Pause
                    if event.key == pygame.K_p:

                        self.toggle_pause()

                    # ESC -> Quit
                    elif event.key == pygame.K_ESCAPE:

                        self.running = False
>>>>>>> 4159d45 (Upload)

    # ==================================================
    # HANDLE PLAYER INPUT
    # ==================================================

    def handle_player_input(self):

        keys = pygame.key.get_pressed()

        # ==================================================
        # LEFT / RIGHT
        # ==================================================

        left = (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        )

        right = (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        )

        # Chỉ giữ LEFT
        if left and not right:

            self.player.move_left()

        # Chỉ giữ RIGHT
        elif right and not left:

            self.player.move_right()

        # Không giữ hoặc giữ cả hai
        else:

            self.player.stop()

        # ==================================================
        # SHOOT
        # ==================================================

        # Giữ SPACE để bắn liên tục.
        # BulletManager sẽ xử lý cooldown.

        if keys[pygame.K_SPACE]:

            shot = self.bullet_manager.shoot(
                self.player.rect.centerx,
                self.player.rect.top
            )

            # Chỉ phát âm thanh nếu bắn thành công
            if shot:

                self.sound_manager.play_shoot()

    # ==================================================
    # BULLET - ENEMY COLLISION
    # ==================================================

    def handle_bullet_enemy_collision(self):

        for enemy in self.enemy_manager.enemies:

            # Copy list vì có thể xóa bullet
            for bullet in self.bullet_manager.bullets[:]:

                if check_collision(
                    enemy,
                    bullet
                ):

                    # Xóa viên đạn
                    self.bullet_manager.remove(
                        bullet
                    )

                    # Enemy nhận damage
                    dead = enemy.take_damage()

                    # Enemy chết
                    if dead:

                        # Sound
                        self.sound_manager.play_explosion()

                        # Explosion
                        self.bullet_manager.add_explosion(
                            enemy.rect.centerx,
                            enemy.rect.centery
                        )

                        # Score
                        self.score += enemy.score

                        # Respawn enemy
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

                # Player đang bất tử thì
                # take_damage() trả về False
                if damaged:

                    self.sound_manager.play_explosion()

                    # Explosion
                    self.bullet_manager.add_explosion(
                        enemy.rect.centerx,
                        enemy.rect.centery
                    )

                    # Respawn enemy
                    self.enemy_manager.respawn(
                        enemy
                    )

                    # Hết mạng
                    if self.player.lives <= 0:

<<<<<<< HEAD
                        self.change_state(
                            STATE_GAME_OVER
                        )
=======
                        self.end_game()
>>>>>>> 4159d45 (Upload)

                        return

    # ==================================================
    # HANDLE COLLISIONS
    # ==================================================

    def handle_collisions(self):

        self.handle_bullet_enemy_collision()

        # Nếu collision bullet làm thay đổi state
        if self.state != STATE_PLAYING:
            return

        self.handle_enemy_player_collision()

    # ==================================================
    # UPDATE LEVEL
    # ==================================================

    def update_level(self):

<<<<<<< HEAD
        # Mỗi LEVEL_SCORE_STEP điểm = tăng 1 level
=======
        # Ví dụ:
        # 0 - 99     -> Level 1
        # 100 - 199  -> Level 2
        # 200 - 299  -> Level 3
>>>>>>> 4159d45 (Upload)

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

<<<<<<< HEAD
        # Hết mạng
        if self.player.lives <= 0:

            self.change_state(
                STATE_GAME_OVER
            )

            return

        # Enemy xuống quá thấp
=======
        # ==================================================
        # PLAYER HẾT MẠNG
        # ==================================================

        if self.player.lives <= 0:

            self.end_game()

            return

        # ==================================================
        # ENEMY XUỐNG QUÁ THẤP
        # ==================================================

>>>>>>> 4159d45 (Upload)
        for enemy in self.enemy_manager.enemies:

            if enemy.y > GAME_OVER_Y:

<<<<<<< HEAD
                self.change_state(
                    STATE_GAME_OVER
                )
=======
                self.end_game()
>>>>>>> 4159d45 (Upload)

                return

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

<<<<<<< HEAD
        # MENU / PAUSED / GAME_OVER: đứng yên, không update logic
        if self.state != STATE_PLAYING:
            return

        # Input (giữ phím)
        self.handle_player_input()

        # Player
=======
        # Menu / Pause / Game Over / High Score
        # thì gameplay không update

        if self.state != STATE_PLAYING:
            return

        # ==================================================
        # INPUT
        # ==================================================

        self.handle_player_input()

        # ==================================================
        # PLAYER
        # ==================================================

>>>>>>> 4159d45 (Upload)
        self.player.update()

        # ==================================================
        # ENEMY
        # ==================================================

        self.enemy_manager.update()

        # ==================================================
        # BULLET
        # ==================================================

        self.bullet_manager.update()

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
<<<<<<< HEAD
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
=======
>>>>>>> 4159d45 (Upload)
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

            # Player + Enemy + Bullet + HUD
            self.draw_game()

<<<<<<< HEAD
            # Pause
            if self.state == STATE_PAUSED:
=======
            # ==============================================
            # PAUSED
            # ==============================================
>>>>>>> 4159d45 (Upload)

            if self.state == STATE_PAUSED:

<<<<<<< HEAD
            # Game Over
=======
                self.pause_ui.draw(
                    self.screen
                )

            # ==============================================
            # GAME OVER
            # ==============================================

>>>>>>> 4159d45 (Upload)
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

        # Score
        self.score = 0

        # Level
        self.level = 1

        # Player
        self.player.reset()

        # Enemy
        self.enemy_manager.reset()

        # Bullet
        self.bullet_manager.reset()

        # KHÔNG reset high_score
        # vì High Score cần giữ qua các ván chơi

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

                # File rỗng
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

        # Đảm bảo thư mục data tồn tại
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

            # ==================================================
            # FPS
            # ==================================================

            self.clock.tick(
                FPS
            )

            # ==================================================
            # 1. EVENT
            # ==================================================

            self.handle_events()

            # ==================================================
            # 2. UPDATE
            # ==================================================

            self.update()

<<<<<<< HEAD
            # 3. Render
            self.draw()
=======
            # ==================================================
            # 3. DRAW
            # ==================================================

            self.draw()
>>>>>>> 4159d45 (Upload)
