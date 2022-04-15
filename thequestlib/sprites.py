from random import randint
import pygame as pg
from thequestlib import CRASH_SOUND, LIVES, METEORITE_SPRITE, ROCKET_SPRITE, SATELLITE_SPRITE, SPACESHIP_SPRITE, WHITE


class SpaceThing(pg.sprite.Sprite):
    def __init__(self, level, screen : pg.Surface, surface : pg.Surface, position = [0,0], speed = 1):
        super().__init__()
        self.level = level
        self.screen = screen
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = speed

    def update(self):
        if self.level.stopframes == 0:
            self.rect.x -= self.speed
            if (self.rect.x + self.image.get_width()) <= 0:
                self.rect.x = self.screen.get_width() - 1
                self.rect.y = randint(0, self.screen.get_height() - 1)
                if isinstance(self, (Asteroid, Rocket, Satellite)):
                    self.level.points += 1

class Star(SpaceThing):
    def __init__(self, level, screen : pg.Surface, position = [0,0], speed = 1):
        super().__init__(level, screen, pg.Surface((2, 2)) ,position, speed)
        self.image.fill(WHITE)
       
class Rocket(SpaceThing):
    def __init__(self, level, screen : pg.Surface, position = [0,0], speed = 6):
        self.animationcounter = 10
        super().__init__(level, screen, pg.image.load(ROCKET_SPRITE.format(self.animationcounter // 10)) ,position, speed)
        self.rect.centerx += self.screen.get_width()//2

    def update(self):
        self.animationcounter += 1
        if self.animationcounter > 29:
            self.animationcounter = 10
        self.image = pg.image.load(ROCKET_SPRITE.format(self.animationcounter // 10))
        super().update()

class Satellite(SpaceThing):
    def __init__(self, level, screen: pg.Surface, position=[0, 0], speed = 5):
        super().__init__(level, screen, pg.image.load(SATELLITE_SPRITE), position, speed)
        self.rect.centerx += self.screen.get_width()//2

class Asteroid(SpaceThing):
    def __init__(self, level, screen : pg.Surface, position = [0,0], speed = 4):
        super().__init__(level, screen, pg.image.load(METEORITE_SPRITE) ,position, speed)
        self.rect.centerx += self.screen.get_width()//2
       
class Spaceship(pg.sprite.Sprite):
    def __init__(self, level,  screen : pg.Surface):
        super().__init__()
        self.level = level
        self.speed = 0
        self.screen = screen
        self.image = pg.image.load(SPACESHIP_SPRITE)
        self.rect = self.image.get_rect()
        self.collisionbox = pg.Surface((95,35)).get_rect()
        self.rect.center = (self.screen.get_width()//20, self.screen.get_height()//2)
        self.crashsound = pg.mixer.Sound(CRASH_SOUND)

    def update(self):
        if self.level.stopframes == 0:    
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
        self.collisionbox.center = self.rect.center
    

class TextDisplay(pg.sprite.Sprite):
    def __init__(self, level, font : pg.font.Font, text = "", position = [0,0]):
        super().__init__()
        self.font = font
        self.level = level
        self.position = position
        self.image = font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.text = text
    
    def update(self):
        self.image = self.font.render(self.text, True, WHITE)
        
class LivesText(TextDisplay):
    def __init__(self, level, font: pg.font.Font):
        super().__init__(level, font, text = "VIDAS: {}".format(LIVES), position = [0,0])
        
    def update(self):
        self.text = "VIDAS: {}".format(self.level.lives)
        super().update()

class PointsText(TextDisplay):
    def __init__(self, level, font: pg.font.Font, text= "{:0>10}".format(0), position=[0, 0]):
        super().__init__(level, font, text, position)

    def update(self):
        self.text = "{:0>10}".format(self.level.points)
        super().update()