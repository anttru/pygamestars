import pygame as pg
from thequestlib import FONT_SIZE, GAME_FONT, LIVES
from thequestlib.modes import Level

class Game:
    def __init__(self):
        self.displayinfo = pg.display.Info()
        self.screen = pg.display.set_mode((self.displayinfo.current_w, self.displayinfo.current_h))
        self.font = pg.font.Font(GAME_FONT, FONT_SIZE)
        self.flags = {
            "game_over": False,
            "next_level": True
        }
        
        self.lives = LIVES
        self.points = 0
        self.levelnumber = 1
        self.levels = {1: (), 
                       2:(5,11,17,23,29,35,41), 
                       3: (5,11,17,23,29,35,41,6,7,8,9,10,18,19,20,21,22,30,31,32,33,34)
                       }
        self.clock = pg.time.Clock()
    
    def mainloop(self):
        
        level = Level(self.screen, self.font, self.clock, self.lives, self.points, self.levelnumber)
        
        