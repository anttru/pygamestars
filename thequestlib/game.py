import pygame
from thequestlib import FONT_SIZE, GAME_FONT, HIGHSCORE_SAVE_TEXT, LIVES, RESOLUTION_SCALES
from thequestlib.DbManager import getScores
from thequestlib.inputname import InputName
from thequestlib.levelmode import Level
from thequestlib.menumode import Mainmenu
from thequestlib.textscreenmode import TextScreen

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
        
        self.scoretobeat = getScores()[1][9][1]
        self.clock = pygame.time.Clock()
        
    def mainloop(self):
        while self.flags["close"] == False:
            statusinfo = Mainmenu(self.screen, self.font, self.scaling, self.clock).mainloop()
            self.flags["close"] = statusinfo["close"]
            
            while not self.flags["dead"] and not self.flags["close"]:
                self.flags["close"] = TextScreen(self.screen, ["LEVEL {}".format(self.levelnumber)], self.font, self.clock, scaling = self.scaling, durationinsecs = 2, black = True).mainloop()["close"]
                if self.flags["close"] == False:
                    statusinfo = Level(self.screen, self.font, self.clock, self.lives, self.points, self.levelnumber, self.scaling).mainloop()
                    self.lives = statusinfo["lives"]
                    self.points = statusinfo["points"]
                    self.flags["dead"] = statusinfo["dead"]
                    self.flags["close"] = statusinfo["close"]
                if statusinfo["dead"] == False and self.flags["close"] == False:
                    self.levelnumber += 1
                elif self.flags["close"] == False:
                    self.flags["close"] = TextScreen(self.screen, ["GAME OVER"], self.font, self.clock, scaling = self.scaling, durationinsecs = 2, black = True).mainloop()["close"]
                    self.levelnumber = 1
                    if (self.points > self.scoretobeat) and self.flags["close"] == False:
                        self.flags["close"] = InputName(self.screen, HIGHSCORE_SAVE_TEXT, self.clock, self.scaling, self.points).mainloop()["close"]
                    if self.flags["close"] == False:
                        self.flags["close"] = TextScreen(self.screen, getScores()[0], self.font, self.clock, scaling = self.scaling, black = True, durationinsecs= 8).mainloop()["close"]
            self.flags["dead"] = False
            self.points = 0
            self.lives = 3
        return self.flags    
       
        