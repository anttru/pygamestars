from random import randint
import pygame as pg
from thequestlib import METEORITE_SPRITE, SPACESHIP_SPRITE, WHITE

class SpaceThing(pg.sprite.Sprite):
    def __init__(self, game, screen : pg.display, surface : pg.Surface, position = [0,0], speed = 1):
        super().__init__()
        self.game = game
        self.screen = screen
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = speed

class Star(SpaceThing):
    def __init__(self, game, screen : pg.display, position = [0,0], speed = 1):
        super().__init__(game, screen, pg.Surface((2, 2)) ,position, speed)
        self.image.fill(WHITE)
                
    def update(self):
        if self.game.stop == False:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.rect.x = self.screen.get_width() - 1
                self.rect.y = randint(0, self.screen.get_height() - 1)
        

class Obstacle(SpaceThing):
    def __init__(self, game, screen : pg.display, position = [0,0], speed = 4):
        super().__init__(game, screen, pg.image.load(METEORITE_SPRITE) ,position, speed)
        self.rect.centerx += self.screen.get_height()//2
        
    def update(self):
        if self.game.stop == False:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.rect.x = self.screen.get_width() - 1
                self.rect.y = randint(0, self.screen.get_height() - 1)

class Spaceship(pg.sprite.Sprite):
    def __init__(self, game,  screen : pg.display):
        super().__init__()
        self.game = game
        self.speed = 0
        self.screen = screen
        self.image = pg.image.load(SPACESHIP_SPRITE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen.get_width()//20, self.screen.get_height()//2)
    
    def update(self):
        if self.game.stop == False:    
            if 40 <= self.rect.topleft[1]: 
                if pg.key.get_pressed()[pg.K_UP]:
                    self.speed += 0.1
                    self.rect.y -= self.speed
                                        
            if self.screen.get_height()- 40 >= self.rect.bottomleft[1]: 
                if pg.key.get_pressed()[pg.K_DOWN]:
                    self.speed +=0.1 
                    self.rect.y += self.speed
            
            if not pg.key.get_pressed()[pg.K_UP] and not pg.key.get_pressed()[pg.K_DOWN]:
                self.speed = 0
        else: 
            self.speed = 0

class TextDisplay(pg.sprite.Sprite):
    def __init__(self, font : pg.font.Font, text = "", position = [0,0]):
        super().__init__()
        self.font = font
        self.position = position
        self.image = font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.text = text
    
    def update(self, text):
        self.text = text
        self.position = (self.rect.x, self.rect.y)
        self.image = self.font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

         
