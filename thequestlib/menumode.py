from email.mime import image
import pygame

from thequestlib import FRAME_RATE, MENU_IMAGES, MENU_SECONDS

class Mainmenu:
    def __init__(self, screen : pygame.surface.Surface, scaling, clock : pygame.time.Clock):
        self.images = []
        self.screen = screen
        self.scaling = scaling
        self.clock = clock
        self.close = False
        self.exit = False
        self.currentselection = 0
        self.framecounter = 0
        self.duration = MENU_SECONDS * FRAME_RATE
        for i in range(4):
            image = pygame.image.load(MENU_IMAGES.format(i))
            if scaling != 1:
                self.images.append(pygame.transform.rotozoom(image, 0, scaling))
            else:
                self.images.append(image)
    
    def mainloop(self):
        while self.framecounter < self.duration and self.close == False and self.exit == False:
            self.clock.tick(FRAME_RATE * self.scaling)
            self.eventloop()
            self.screen.blit(self.images[self.currentselection])           
            pygame.display.flip()
            self.framecounter += 1
        return {
            "close" : self.close,
        }
    def eventloop(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.exit = True
                if event.key == pygame.K_x:
                    self.close = True
            if event.type == pygame.QUIT:
                self.close = True
