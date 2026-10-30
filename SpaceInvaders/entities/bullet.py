import pygame

class Bullet:
    def __init__(self, x, y, direction=-1, speed=8, damage=1, color=None, image=None):
        self.direction = direction
        self.speed = speed
        self.damage = damage
        
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((4, 12))
            if color:
                self.image.fill(color)
            else:
                self.image.fill((255, 230, 0) if direction == -1 else (255, 80, 50))
            
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.speed * self.direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_outside(self, screen_height=600):
        return self.rect.bottom < 0 or self.rect.top > screen_height