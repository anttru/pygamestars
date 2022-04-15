import pygame as pg
from random import randint
from thequestlib import BACKGROUNDS, BACKGROUNDS_NUMBER, EXPLOSION_SPRITE, LEVEL_MUSIC, STAR_SPEEDS, STARS_AMOUNT
from thequestlib.sprites import Asteroid, LivesText, PointsText, Rocket, Satellite, Spaceship, Star 

class Level:
    def __init__(self, screen : pg.Surface, font : pg.font.Font, clock : pg.time.Clock, lives, points, levelnumber):
        self.screen = screen
        self.font = font
        self.levelnumber = levelnumber
        self.lives = lives
        self.dead = False
        self.explosioncenter = None

        self.lifetext = LivesText(self, self.font)
        self.lifetext.rect.topright = [self.screen.get_width() - 20, 0 + 10]
        self.points = points
        self.pointstext = PointsText(self, self.font)
        
        self.startlevel()
        self.stopframes = 0
                
        self.game_over = False
        self.clock = pg.time.Clock()
        self.background = pg.image.load(BACKGROUNDS.format(self.levelnumber % BACKGROUNDS_NUMBER)).convert()
        pg.mixer.music.load(LEVEL_MUSIC)
        pg.mixer.music.play(-1)

        self.mainloop()
    
    def startlevel(self):
        self.spaceship = Spaceship(self, self.screen)
        self.sprites = pg.sprite.Group()
        for speed in STAR_SPEEDS:
            self.generateField(STARS_AMOUNT, self.sprites, Star, speed)
        self.generateField(self.levelnumber * 25, self.sprites, Asteroid, 4)
        self.generateField(self.levelnumber, self.sprites, Rocket, 6)
        self.generateField(self.levelnumber, self.sprites, Satellite, 5)
        self.sprites.add(self.spaceship)
        self.sprites.add(self.lifetext)
        self.sprites.add(self.pointstext)

    def generateField(self, amount : int, container : pg.sprite.Group, spritetype : pg.sprite.Sprite, speed = 1):
        for i in range(amount):
            position = [randint(0, self.screen.get_width() - 1), randint(0, self.screen.get_height() - 1)]
            sprite = spritetype(self, self.screen, position = position, speed = speed)
            container.add(sprite)
        return container

    def explosion(self,position, framecounter):
        if self.explosioncenter != None:
            explosion = pg.image.load(EXPLOSION_SPRITE.format(framecounter//10))
            position = (position[0] - explosion.get_width()//2, position[1] - explosion.get_height()//2)
            self.screen.blit(explosion, position)
        
    def detectCollisions(self):
        if self.stopframes == 0:
            for obstacle in self.sprites:
                if isinstance(obstacle, (Asteroid, Rocket, Satellite)):
                    if obstacle.rect.colliderect(self.spaceship.collisionbox):
                        self.lives -= 1
                        self.explosioncenter = obstacle.rect.clip(self.spaceship.collisionbox).topleft
                        if self.lives < 0:
                            self.lives = 0
                            self.dead = True
                        self.stopframes += 1
                        self.spaceship.crashsound.play()
                        
    def handlestop(self):
        if self.stopframes > 0:
                self.stopframes += 1
        if self.stopframes >= 120:
            if self.dead == True:
                self.game_over = True
            self.startlevel()
            self.stopframes = 0
            self.explosioncenter = None

    def mainloop(self):
        while not self.game_over:
            self.clock.tick(60)

            self.handlestop()

            eventList = pg.event.get()
            for event in eventList:
                if event.type == pg.QUIT:
                        self.game_over = True
           
            self.detectCollisions()
            self.sprites.update()
                                    
            self.screen.blit(self.background, [0,0])
            self.sprites.draw(self.screen)
            self.explosion(self.explosioncenter, self.stopframes)
            
            pg.display.flip()
        return {
            "lives" : self.lives,
            "points": self.points
            
        }