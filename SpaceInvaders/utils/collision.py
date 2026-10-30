import pygame
import random

class CombatSystem:
    def __init__(self, combo_timeout=1500):
        self.combo_count = 0
        self.combo_timeout = combo_timeout
        self.last_kill_time = 0

    def update_combo(self):
        if self.combo_count > 0:
            if pygame.time.get_ticks() - self.last_kill_time > self.combo_timeout:
                self.combo_count = 0

    def calculate_kill_score(self, base_score):
        """
        Combo
        """
        now = pygame.time.get_ticks()
        self.last_kill_time = now
        self.combo_count += 1
        
        bonus = 0
        if self.combo_count >= 3 and self.combo_count % 3 == 0:
            bonus = 10 # Thưởng bonus
            
        multiplier = 1.0
        if self.combo_count >= 3:
            multiplier = 1.5
        elif self.combo_count == 2:
            multiplier = 1.2
            
        return int(base_score * multiplier) + bonus

combat_system = CombatSystem()

def handle_all_collisions(player, bullet_manager, enemy_manager, powerup_manager=None, sound_manager=None):
    score_gained = 0
    combat_system.update_combo()

    # ========================================================
    # 1. VA CHẠM: Player Bullet <-> Enemy
    # ========================================================
    for bullet in bullet_manager.player_bullets[:]:
        for enemy in enemy_manager.enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                # Xóa đạn
                if bullet in bullet_manager.player_bullets:
                    bullet_manager.player_bullets.remove(bullet)

                # Trừ HP của quái
                damage = getattr(bullet, 'damage', 1)
                enemy.health -= damage

                # Quái bị tiêu diệt
                if enemy.health <= 0:
                    base_score = getattr(enemy, 'score', 10)
                    score_gained += combat_system.calculate_kill_score(base_score)

                    # Kích hoạt vụ nổ tại vị trí quái chết
                    bullet_manager.add_explosion(enemy.rect.centerx, enemy.rect.centery)

                    # Phát âm thanh nổ
                    if sound_manager and hasattr(sound_manager, 'play_explosion'):
                        sound_manager.play_explosion()

                    # Rơi Power-up
                    if powerup_manager and hasattr(powerup_manager, 'spawn_powerup'):
                        if random.random() < 0.20:
                            powerup_manager.spawn_powerup(enemy.rect.centerx, enemy.rect.centery)

                    # Xóa quái khỏi manager
                    if hasattr(enemy_manager, 'remove_enemy'):
                        enemy_manager.remove_enemy(enemy)
                    elif enemy in enemy_manager.enemies:
                        enemy_manager.enemies.remove(enemy)

                break

    # ========================================================
    # 2. VA CHẠM: Enemy Bullet <-> Player
    # ========================================================
    for bullet in bullet_manager.enemy_bullets[:]:
        if bullet.rect.colliderect(player.rect):
            bullet_manager.enemy_bullets.remove(bullet)
            bullet_manager.add_explosion(player.rect.centerx, player.rect.centery)
            if hasattr(player, 'take_damage'):
                player.take_damage()

    # ========================================================
    # 3. VA CHẠM: Enemy <-> Player (Quái đâm thẳng vào tàu)
    # ========================================================
    for enemy in enemy_manager.enemies[:]:
        if enemy.rect.colliderect(player.rect):
            bullet_manager.add_explosion(enemy.rect.centerx, enemy.rect.centery)
            if hasattr(enemy_manager, 'remove_enemy'):
                enemy_manager.remove_enemy(enemy)
            elif enemy in enemy_manager.enemies:
                enemy_manager.enemies.remove(enemy)
            
            if hasattr(player, 'take_damage'):
                player.take_damage()

    # ========================================================
    # 4. VA CHẠM: Power-up <-> Player (Người chơi nhặt đồ)
    # ========================================================
    if powerup_manager and hasattr(powerup_manager, 'powerups'):
        for item in powerup_manager.powerups[:]:
            if item.rect.colliderect(player.rect):
                if hasattr(item, 'apply_effect'):
                    item.apply_effect(player)
                powerup_manager.powerups.remove(item)

    return score_gained, combat_system.combo_count