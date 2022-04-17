from random import randint
import pygame
from thequestlib import CRASH_SOUND, LEVEL_END_TEXT, LIVES, METEORITE_SPRITE, PLANET_SPRITE, POINTS_TO_PASS, ROCKET_SPRITE, SATELLITE_SPRITE, SPACESHIP_SPRITE, WHITE
from thequestlib.textscreenmode import TextScreen

class SpaceThing(pygame.sprite.Sprite):
    def __init__(self, level, screen : pygame.Surface, surface : pygame.Surface, position = [0,0], speed = 1):
        super().__init__()
        self.level = level
        self.screen = screen
        self.image = surface
        if self.level.scaling != 1:
            self.image = pygame.transform.rotozoom(self.image, 0, self.level.scaling)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = speed

    def update(self):
        if self.level.stopframes == 0:
            self.rect.x -= self.speed
            if ((self.rect.x + self.image.get_width()) <= 0) and (self.level.thislevelpoints < POINTS_TO_PASS * self.level.levelnumber):
                self.rect.x = self.screen.get_width() - 1
                self.rect.y = randint(0, self.screen.get_height() - 1)
                if isinstance(self, (Asteroid, Rocket, Satellite)):
                    self.level.points += 1
                    self.level.thislevelpoints += 1

class Star(SpaceThing):
    def __init__(self, level, screen : pygame.Surface, position = [0,0], speed = 1):
        super().__init__(level, screen, pygame.Surface((2, 2)) ,position, speed)
        self.image.fill(WHITE)
    def update(self):
        if self.level.stopframes == 0:
            self.rect.x -= self.speed
            if ((self.rect.x + self.image.get_width()) <= 0): 
                self.rect.x = self.screen.get_width() - 1
                self.rect.y = randint(0, self.screen.get_height() - 1)
    
class Rocket(SpaceThing):
    def __init__(self, level, screen : pygame.Surface, position = [0,0], speed = 6):
        self.animationcounter = 10
        super().__init__(level, screen, pygame.image.load(ROCKET_SPRITE.format(self.animationcounter // 10)) ,position, speed)
        self.rect.centerx += self.level.screencenter[0]

    def update(self):
        self.animationcounter += 1
        if self.animationcounter > 29:
            self.animationcounter = 10
        self.image = pygame.transform.rotozoom(pygame.image.load(ROCKET_SPRITE.format(self.animationcounter // 10)),0, self.level.scaling)
        super().update()

class Satellite(SpaceThing):
    def __init__(self, level, screen: pygame.Surface, position=[0, 0], speed = 5):
        super().__init__(level, screen, pygame.image.load(SATELLITE_SPRITE), position, speed)
        self.rect.centerx += self.screen.get_width()//2

class Asteroid(SpaceThing):
    def __init__(self, level, screen : pygame.Surface, position = [0,0], speed = 4):
        super().__init__(level, screen, pygame.image.load(METEORITE_SPRITE) ,position, speed)
        self.rect.centerx += self.screen.get_width()//2
       
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, level,  screen : pygame.Surface):
        super().__init__()
        self.level = level
        self.speed = 0
        self.screen = screen
        self.image = pygame.image.load(SPACESHIP_SPRITE)
        self.imagebackup = pygame.image.load(SPACESHIP_SPRITE)
        if self.level.scaling != 1:
            self.image = pygame.transform.rotozoom(self.image, 0, self.level.scaling)
            self.imagebackup = self.image
        self.rect = self.image.get_rect()
        self.collisionbox = pygame.Surface((0.85* self.image.get_width(), 0.67* self.image.get_height())).get_rect()
        self.rect.center = (self.screen.get_width()//20, self.level.screencenter[1])
        self.crashsound = pygame.mixer.Sound(CRASH_SOUND)
        self.totalrotation = 1

    def update(self):
        if self.level.autopilot == False:
            if self.level.stopframes == 0:    
                if 40 <= self.rect.topleft[1]: 
                    if pygame.key.get_pressed()[pygame.K_UP]:
                        self.speed += 0.1
                        self.rect.y -= self.speed
                                            
                if self.screen.get_height()- 40 >= self.rect.bottomleft[1]: 
                    if pygame.key.get_pressed()[pygame.K_DOWN]:
                        self.speed +=0.1 
                        self.rect.y += self.speed
                
                if not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.speed = 0
            else: 
                self.speed = 0
            self.collisionbox.center = self.rect.center
        else:
            if self.rect.centery > self.level.screencenter[1]:
                self.rect.centery -= 3
            elif self.rect.centery < self.level.screencenter[1]:
                self.rect.centery += 3
            elif self.totalrotation < 180:
                self.rotatespaceship() 
            elif self.rect.topright[0] < self.screen.get_width() *3 // 4:
                self.rect.centerx += 3
            if self.rect.topright[0] >= self.screen.get_width() *3 // 4 and self.totalrotation >= 180:
                self.level.finished = True
                self.level.points += 100 * self.level.levelnumber
                self.level.close = TextScreen(self.screen, LEVEL_END_TEXT, self.level.font, self.level.clock, self.level.levelnumber, self.level.scaling).mainloop()["close"]
              
    
    def rotatespaceship(self):
        savedcenter = self.rect.center
        self.image = pygame.transform.rotozoom(self.imagebackup, self.totalrotation, 1)
        self.rect = self.image.get_rect()
        self.rect.center = savedcenter
        self.totalrotation += 1

class Planet(SpaceThing):
    def __init__(self, level, screen: pygame.Surface, position=[0, 0], speed=1):
        super().__init__(level, screen, pygame.image.load(PLANET_SPRITE),position , speed)
        self.rect.x =  self.screen.get_width()
        self.rect.centery = self.level.screencenter[1]
    
    def update(self):
        if self.level.thislevelpoints >= POINTS_TO_PASS * self.level.levelnumber and self.rect.x > self.screen.get_width() * 3 // 4:
            self.rect.x -= self.speed
        if self.rect.x <= self.screen.get_width() * 3 // 4:
            self.level.stopstars()
            self.level.autopilot = True

class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, level, font : pygame.font.Font, text = "", position = [0,0]):
        super().__init__()
        self.font = font
        self.level = level
        self.position = position
        self.image = font.render(text, True, WHITE)
        if self.level.scaling != 1:
            self.image = pygame.transform.rotozoom(self.image, 0, self.level.scaling)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.text = text
    
    def update(self):
        self.image = self.font.render(self.text, True, WHITE)
        if self.level.scaling != 1:
            self.image = pygame.transform.rotozoom(self.image, 0, self.level.scaling)
        
class LivesText(TextDisplay):
    def __init__(self, level, font: pygame.font.Font):
        super().__init__(level, font, text = "LIFES: {}".format(LIVES), position = [0,0])
        
    def update(self):
        if self.level.lives > 0:
            self.text = "LIFES: {}".format(self.level.lives)
        else: 
            self.text = "LIFES: 0"        
        super().update()

class PointsText(TextDisplay):
    def __init__(self, level, font: pygame.font.Font, text= "{:0>10}".format(0), position=[0, 0]):
        super().__init__(level, font, text, position)

    def update(self):
        self.text = "{:0>10}".format(self.level.points)
        super().update()
