import pygame
from thequestlib import BLACK, FONT_SIZE, GAME_FONT, GUITAR_MUSIC, MENU_SOUND, FRAME_RATE, WHITE
from thequestlib.DbManager import addScore
from thequestlib.textscreenmode import TextScreen

class InputName(TextScreen):
    def __init__(self, screen : pygame.Surface, text : list, clock : pygame.time.Clock, scaling = 1, points = 0):
        super().__init__(screen, text, pygame.font.Font(GAME_FONT, FONT_SIZE * 2), clock, scaling)
        self.savedtext = ""
        self.rendertext = "___"
        self.points = points
        pygame.mixer.music.load(GUITAR_MUSIC)
        pygame.mixer.music.play(-1)
        self.menusound = pygame.mixer.Sound(MENU_SOUND)


    def handlekeypresses(self, event):
        if len(self.savedtext) <3:
            if len(event.unicode) > 0:
                if (ord(event.unicode) in range(65, 91)) or (ord(event.unicode) in range(97, 123)): 
                    self.savedtext += event.unicode
                    self.menusound.play()
        if event.key == pygame.K_BACKSPACE:
            self.savedtext = self.savedtext[:-1]
            self.menusound.play()
        if event.key == pygame.K_SPACE and len(self.savedtext) >= 3:
            addScore(self.savedtext[0:3], self.points)
            self.flags["exit"] = True 
    
    def mainloop(self):
        while self.flags["exit"] == False and self.flags["close"] == False:
            self.clock.tick(FRAME_RATE * self.scaling)
            self.eventloop()
            self.updaterendertext()
            self.updateimages()
            self.updateframecounter()

            self.screen.fill(BLACK)
            for image, coordinates in zip(self.images, self.linecoordinates):
                self.screen.blit(image, coordinates)
            pygame.display.flip()
            self.framecounter += 1
        return {
            "close" : self.flags["close"],
        }

    def updateframecounter(self):
        if self.framecounter >= 90 * self.scaling:
            self.framecounter = 0
        else: 
            self.framecounter += 1
    
    def updaterendertext(self):
        if len(self.savedtext) == 0:
            self.addblinkspace()
            self.rendertext += "__"
        if len(self.savedtext) == 1:
            self.addblinkspace()
            self.rendertext += "_"
        if len(self.savedtext) == 2:
            self.addblinkspace()
        if len(self.savedtext) >= 3:
            self.rendertext = self.savedtext[0:3]
    
    def addblinkspace(self):
        self.rendertext = self.savedtext[0:2]
        if self.framecounter // (45 * self.scaling) == 0:
                self.rendertext += "_"
        else:
               self.rendertext += " "

    def updateimages(self):
        newline = "{}  {}  {}".format(self.rendertext[0], self.rendertext[1], self.rendertext[2])
        self.images[2] = pygame.transform.rotozoom(self.font.render(newline.format(**self.textinfo), True, WHITE), 0, self.scaling)