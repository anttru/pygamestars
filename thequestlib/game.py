import pygame as pg
from random import randint
from thequestlib import BLACK, GAME_FONT, STARS_AMOUNT, STAR_SPEEDS
from thequestlib.sprites import Obstacle, Spaceship, Star, TextDisplay

class Game:
    def __init__(self):
        self.displayinfo = pg.display.Info()
        self.screen = pg.display.set_mode((self.displayinfo.current_w, self.displayinfo.current_h))
        self.font = pg.font.Font("freesansbold.ttf", 32)
        

        self.stars = pg.sprite.Group()
        self.meteorites = pg.sprite.Group()
        self.spaceships = pg.sprite.Group(Spaceship(self.screen))
        self.texts = pg.sprite.Group(TextDisplay(self.font, "V", (0,0)))

        for speed in STAR_SPEEDS:
            self.generateField(STARS_AMOUNT, self.stars, Star, speed)
        self.generateField(75, self.meteorites, Obstacle, 4)


        self.newLevel = True
        self.level = 0
        self.font = None
        self.lives = 3
        self.levels = {1: (), 
                       2:(5,11,17,23,29,35,41), 
                       3: (5,11,17,23,29,35,41,6,7,8,9,10,18,19,20,21,22,30,31,32,33,34)
                       }
        self.game_over = False
        self.clock = pg.time.Clock()

    def generateField(self, amount : int, container : pg.sprite.Group, spritetype : pg.sprite.Sprite, speed = 1):
        for i in range(amount):
            position = [randint(0, self.displayinfo.current_w - 1), randint(0, self.displayinfo.current_h - 1)]
            sprite = spritetype(self.screen, position = position, speed = speed)
            container.add(sprite)
        return container

    def mainloop(self):
        while not self.game_over:
            self.clock.tick(60)
            eventList = pg.event.get()
            for event in eventList:
                if event.type == pg.QUIT:
                        self.game_over = True

            self.screen.fill(BLACK)
            self.stars.update()
            self.meteorites.update()
            self.spaceships.update()

            self.stars.draw(self.screen)
            self.meteorites.draw(self.screen)
            self.spaceships.draw(self.screen)
            self.texts.draw(self.screen)
            
            pg.display.flip()