import pygame

from config import (
    PLAYER_IMAGE,
    PLAYER_SPEED,
    PLAYER_LIVES,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_INVINCIBLE_TIME,
    SCREEN_WIDTH
)


HP_image = pygame.image.load('assets/images/heart_full.png')
HP_image = pygame.transform.scale(HP_image, (20, 20))
defensePlayer = 'assets/images/player_defense.png'

class Player:
    def __init__(self):
        self.image = pygame.image.load(PLAYER_IMAGE)
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.HP = PLAYER_LIVES
        self.invincibleTime = PLAYER_INVINCIBLE_TIME
        self.defenseTime = 0
        self.rect = self.image.get_rect()
        self.update_rect()
        

    # Nhan sat thuong
    def take_dame(self):
        print(self.invincibleTime)
        if(self.invincibleTime != 0): return True
        if(self.defenseTime != 0):
            self.defenseTime = 0
            return True
        else:
            self.HP -= 1
            self.reset_position()

            pygame.mouse.set_pos(
                self.x + self.image.get_width()//2, self.y + self.image.get_height()//2
            )    
        return self.HP > 0
        

    # Nhan duoc Item
    def take_item(self, details):
        if(details == 'HP'):
            if(self.HP == self.maxHP): pass
            else:
                self.HP += 1
        if(details == 'Defense'):
            self.defenseTime = 1000

    # Di chuyen
    # Di chuyen bang chuot
    def move_by_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width()/2
        self.y = mouse_y - self.image.get_height()/2


    # Di chuyen bang ban phim
    def move_by_keyboard(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
    # In ra man hinh
    def draw(self, screen):

        self.checkInvincibleTime()
        self.checkdefense()

        for i in range(self.HP):
            x = 20 + i*25
            y = 20
            screen.blit(HP_image, (x, y))

        print(self.x, self. y)
        if self.x <= 0: self.x = 0
        if self.x >= 736: self.x = 736
        if self.y <= 0: self.y = 0
        if self.y >= 536: self.y = 536

        self.update_rect()
        screen.blit(self.image, (self.x, self.y))

    # Cap nhat khoi
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)


    # Cap nhat ve vi tri ban dau
    def reset_position(self):

        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.invincibleTime = PLAYER_INVINCIBLE_TIME

    # reset player
    def reset(self):

        self.lives = PLAYER_LIVES
        self.reset_position()

    #Kiem tra bat tu
    def checkInvincibleTime(self):
        if(self.invincibleTime == 0): pass
        else: self.invincibleTime -= 1

    #Kiem tra khien
    def checkdefense(self):
        if(self.defenseTime == 0): 
            self.image = pygame.image.load(PLAYER_IMAGE)
            pass
        else:
            self.image = pygame.image.load(defensePlayer) 
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.defenseTime -= 1