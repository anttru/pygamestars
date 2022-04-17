import pygame

from thequestlib import BLACK, FRAME_RATE, TEXT_SECONDS, WHITE


class Mode:
    def __init__(self):
        pass
    def eventloop(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.close = True

class TextScreen(Mode):
    def __init__(self, screen : pygame.Surface, text : list, font : pygame.font.Font, clock : pygame.time.Clock, levelnumber = None, durationinsecs = TEXT_SECONDS, black = False):
        self.screen = screen
        self.black = False
        self.exit = False
        self.close = False
        self.clock = clock
        self.images = []
        self.textinfo = {"level": levelnumber, "points": levelnumber*100}
        for line in text:
            self.images.append(font.render(line.format(**self.textinfo), True, WHITE))
        self.framecounter = 0
        self.duration = FRAME_RATE * durationinsecs

        self.linecoordinates = []
        self.calculatecoordinates()
        
        self.mainloop()

    def mainloop(self):
        while self.framecounter < self.duration and self.exit == False and self.close == False:
            self.clock.tick(FRAME_RATE)
            self.eventloop()
            if self.black == True:
                self.screen.fill(BLACK)
            for image, coordinates in zip(self.images, self.linecoordinates):
                self.screen.blit(image, coordinates)
            pygame.display.flip()
            self.framecounter += 1
        return {
            "close" : self.close,
        }
    
    def calculatecoordinates(self):
        textheight = self.images[0].get_height()
        totalheight = len(self.images) * (textheight + 30)
        for i in range (len(self.images)):
            coordinates = (self.screen.get_width()//2 - self.images[i].get_width()//2, self.screen.get_height()//2 - totalheight//2 + i * textheight)
            self.linecoordinates.append(coordinates)
        
    def eventloop(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.exit = True
            if event.type == pygame.QUIT:
                self.close = True