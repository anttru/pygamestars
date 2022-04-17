import pygame
from thequestlib import FONT_SIZE, GAME_FONT, LIVES, RESOLUTION_SCALES
from thequestlib.levelmode import Level

class Game:
    def __init__(self):
        self.displayinfo = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.displayinfo.current_w, self.displayinfo.current_h))
        self.font = pygame.font.Font(GAME_FONT, FONT_SIZE)
        if self.displayinfo.current_h in RESOLUTION_SCALES:
            self.scaling = RESOLUTION_SCALES[self.displayinfo.current_h]
        else: 
            self.scaling = 1
        self.flags = {
            "dead": False,
            "close" :  False
        }
        self.lives = LIVES
        self.points = 0
        self.levelnumber = 1
        
        self.clock = pygame.time.Clock()
    
    def mainloop(self):
        while not self.flags["dead"] and not self.flags["close"]:
            statusinfo = Level(self.screen, self.font, self.clock, self.lives, self.points, self.levelnumber, self.scaling).mainloop()
            self.lives = statusinfo["lives"]
            self.points = statusinfo["points"]
            self.flags["dead"] = statusinfo["dead"]
            self.flags["close"] = statusinfo["close"]
            self.levelnumber += 1

       
        