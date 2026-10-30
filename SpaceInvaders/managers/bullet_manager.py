import pygame
from entities.bullet import Bullet
from entities.explosion import Explosion

class BulletManager:
    def __init__(self, player_cooldown=250):
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        
        self.player_cooldown = player_cooldown
        self.last_player_shot = 0
        self.bullet_image = None
        self.enemy_bullet_image = None

    def shoot_player(self, x, y, sound_manager=None):
        now = pygame.time.get_ticks()
        if now - self.last_player_shot >= self.player_cooldown:
            bullet = Bullet(x, y, direction=-1, speed=9, damage=1, image=self.bullet_image)
            self.player_bullets.append(bullet)
            self.last_player_shot = now
            if sound_manager and hasattr(sound_manager, 'play_shoot'):
                sound_manager.play_shoot()
            return True
        return False

    def shoot_enemy(self, x, y, sound_manager=None):
        bullet = Bullet(x, y, direction=1, speed=5, damage=1, color=(255, 60, 60), image=self.enemy_bullet_image)
        self.enemy_bullets.append(bullet)
        return True

    def add_explosion(self, x, y):
        self.explosions.append(Explosion(x, y))

    def update(self, screen_height=600):
        # 1. Cập nhật và dọn dẹp đạn người chơi
        for b in self.player_bullets:
            b.update()
        self.player_bullets = [b for b in self.player_bullets if not b.is_outside(screen_height)]

        # 2. Cập nhật và dọn dẹp đạn kẻ địch
        for b in self.enemy_bullets:
            b.update()
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.is_outside(screen_height)]

        # 3. Cập nhật các hiệu ứng nổ
        for exp in self.explosions:
            exp.update()
        self.explosions = [exp for exp in self.explosions if not exp.is_finished()]

    def draw(self, screen):
        # Vẽ toàn bộ đạn và hiệu ứng nổ
        for b in self.player_bullets:
            b.draw(screen)
        for b in self.enemy_bullets:
            b.draw(screen)
        for exp in self.explosions:
            exp.draw(screen)

    def reset(self):
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.explosions.clear()
        self.last_player_shot = 0