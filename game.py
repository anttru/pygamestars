import pygame as pg

class Game:
    def __init__(self, width = 600, height = 800):
        self.screen = pg.display.set_mode((width, height))
        self.ball = Ball(self.screen, (255,255,0))
        self.racket = Racket(self.screen, self.ball)
        self.background = pg.image.load(r".\resources\background.jpg")
        self.balls = []
        self.bricks = []
        self.generateBricks()
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