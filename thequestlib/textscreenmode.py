from operator import truediv
import pygame
from thequestlib import BLACK, FRAME_RATE, TEXT_SECONDS, WHITE


class Mode:
    def __init__(self):
        pass
    def eventloop(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                self.handlekeypresses(event)
            if event.type == pygame.QUIT:
                self.flags["close"] = True
    def handlekeypresses(self, event):
        pass

class TextScreen(Mode):
    def __init__(self, screen : pygame.Surface, text : list, font : pygame.font.Font, clock : pygame.time.Clock, levelnumber = 0, scaling = 1, durationinsecs = TEXT_SECONDS, black = False):
        self.screen = screen
        self.black = black
        self.font = font
        self.flags = {
            "exit"  : False,
            "close" : False
        }
        self.clock = clock
        self.images = []
        self.textinfo = {"level": levelnumber, "points": levelnumber*100}
        self.scaling = scaling
        for line in text:
            self.images.append(pygame.transform.rotozoom(font.render(line.format(**self.textinfo), True, WHITE), 0, self.scaling))
        
        if self.scaling != 1:
            for image in self.images:
                image = pygame.transform.rotozoom(image, 0, self.scaling)
                 
        self.framecounter = 0
        self.duration = FRAME_RATE * durationinsecs * scaling 

        self.linecoordinates = []
        self.calculatecoordinates()
        
    def mainloop(self):
        while self.framecounter < self.duration and self.flags["exit"] == False and self.flags["close"] == False:
            self.clock.tick(FRAME_RATE * self.scaling)
            self.eventloop()
            if self.black == True:
                self.screen.fill(BLACK)
            for image, coordinates in zip(self.images, self.linecoordinates):
                self.screen.blit(image, coordinates)
            pygame.display.flip()
            self.framecounter += 1
        return {
            "close" : self.flags["close"],
        }
    
    def calculatecoordinates(self):
        textheight = self.images[0].get_height() + 30* self.scaling
        totalheight = len(self.images) * (textheight)
        for i in range (len(self.images)):
            coordinates = (self.screen.get_width()//2 - self.images[i].get_width()//2, self.screen.get_height()//2 - totalheight//2 + i * textheight)
            self.linecoordinates.append(coordinates)

    def handlekeypresses(self, event):
        if event.key == pygame.K_SPACE:
            self.flags["exit"] = True    