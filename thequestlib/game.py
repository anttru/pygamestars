import pygame as pg
from random import randint

class Game:
    def __init__(self):
        self.displayinfo = pg.display.Info()
        self.screen = pg.display.set_mode((self.displayinfo.current_w, self.displayinfo.current_h))
        
        #self.background = pg.image.load(r".\resources\background.jpg")
        
        self.newLevel = True
        self.level = 0
        self.font = None
        self.lives = 3
        self.levels = {1: (), 
                       2:(5,11,17,23,29,35,41), 
                       3: (5,11,17,23,29,35,41,6,7,8,9,10,18,19,20,21,22,30,31,32,33,34)
                       }
        self.game_over = False
        #self.clock = pg.time.Clock()

    def generateField(self, amount : int, container : list):
        for i in range(amount):
            position = [randint(0, self.displayinfo.current_w - 1), randint(0, self.displayinfo.current_h - 1)]
            container.append(position)



    def mainloop(self):
        while not self.game_over:
            eventList = pg.event.get()
            for event in eventList:
                if event.type == pg.QUIT:
                        self.game_over = True

            self.screen.fill((0,0,0))
            pg.display.flip()