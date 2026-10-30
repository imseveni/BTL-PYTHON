import os
import sys

# Thêm thư mục SpaceInvaders vào sys.path để Python tìm thấy managers, entities, utils khi chạy
current_dir = os.path.dirname(os.path.abspath(__file__))
space_invaders_dir = os.path.join(current_dir, "SpaceInvaders")
if space_invaders_dir not in sys.path:
    sys.path.insert(0, space_invaders_dir)

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import random
import pygame

# Import các module chính thức của Thành viên 4
from managers.bullet_manager import BulletManager
from utils.collision import handle_all_collisions

# ----------------- GIẢ LẬP ĐỐI TƯỢNG ĐỂ TEST ĐỘC LẬP -----------------
class DummyPlayer:
    def __init__(self):
        self.rect = pygame.Rect(380, 530, 40, 25)
        self.speed = 6
        self.lives = 3

    def take_damage(self):
        self.lives -= 1
        print(f"-> PLAYER BI TRUNG DAN! Con {self.lives} mang.")

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x = max(10, self.rect.x - self.speed)
        if keys[pygame.K_RIGHT]:
            self.rect.x = min(750, self.rect.x + self.speed)

    def draw(self, screen):
        # Vẽ phi thuyền hình tam giác màu xanh ngọc
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(screen, (0, 255, 180), points)

class DummyEnemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.enemy_type = enemy_type
        if enemy_type == "tank":
            self.rect = pygame.Rect(x, y, 45, 35)
            self.health = 3
            self.score = 30
            self.color = (60, 150, 255) # Xanh biển
        elif enemy_type == "fast":
            self.rect = pygame.Rect(x, y, 30, 25)
            self.health = 1
            self.score = 20
            self.color = (255, 80, 255) # Tím hồng
        else:
            self.rect = pygame.Rect(x, y, 35, 25)
            self.health = 1
            self.score = 10
            self.color = (255, 60, 60) # Đỏ

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=4)

class DummyEnemyManager:
    def __init__(self):
        self.enemies = []
        self.spawn()

    def spawn(self):
        # Hàng 1: Tank quái máu trâu
        for i in range(5):
            self.enemies.append(DummyEnemy(120 + i * 130, 80, "tank"))
        # Hàng 2: Normal quái
        for i in range(7):
            self.enemies.append(DummyEnemy(80 + i * 95, 140, "normal"))
        # Hàng 3: Fast quái
        for i in range(8):
            self.enemies.append(DummyEnemy(60 + i * 85, 190, "fast"))

# ----------------- KHỞI CHẠY VÒNG LẶP TEST -----------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("DEMO CHÍNH THỨC PHẦN 4: COMBAT, COLLISION, COMBO & EXPLOSION")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22, bold=True)

player = DummyPlayer()
bullet_manager = BulletManager(player_cooldown=200)
enemy_manager = DummyEnemyManager()

total_score = 0
last_enemy_shot = 0

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    # 1. Player bắn đạn
    if keys[pygame.K_SPACE]:
        bullet_manager.shoot_player(player.rect.centerx, player.rect.top)

    # 2. Quái bắn trả ngẫu nhiên mỗi 1 giây (Enemy shooting)
    now = pygame.time.get_ticks()
    if now - last_enemy_shot > 1000 and len(enemy_manager.enemies) > 0:
        shooter = random.choice(enemy_manager.enemies)
        bullet_manager.shoot_enemy(shooter.rect.centerx, shooter.rect.bottom)
        last_enemy_shot = now

    # 3. Cập nhật đạn và vụ nổ
    bullet_manager.update(600)

    # 4. Xử lý va chạm, tính điểm và chuỗi combo
    gained, combo = handle_all_collisions(player, bullet_manager, enemy_manager)
    total_score += gained

    # 5. Vẽ giao diện
    screen.fill((12, 14, 25))
    player.draw(screen)
    bullet_manager.draw(screen)
    for e in enemy_manager.enemies:
        e.draw(screen)

    # Hiển thị HUD thông tin
    score_txt = font.render(f"SCORE: {total_score}", True, (255, 255, 255))
    lives_txt = font.render(f"LIVES: {player.lives}", True, (0, 255, 150))
    combo_txt = font.render(f"COMBO: x{combo}" if combo > 1 else "", True, (255, 215, 0))

    screen.blit(score_txt, (20, 20))
    screen.blit(lives_txt, (200, 20))
    if combo > 1:
        screen.blit(combo_txt, (350, 20))

    pygame.display.flip()

pygame.quit()