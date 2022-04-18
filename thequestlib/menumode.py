from tkinter import font
import pygame
from thequestlib import FRAME_RATE, INSTRUCTIONS_TEXT, MENU_IMAGES, MENU_MUSIC, MENU_SECONDS, MENU_SOUND, STORY_TEXT
from thequestlib.DbManager import ScoreGetter, ScoreGetter
from thequestlib.textscreenmode import Mode, TextScreen

class Mainmenu(Mode):
    def __init__(self, screen : pygame.surface.Surface, font, scaling, clock : pygame.time.Clock):
        self.images = []
        self.screen = screen
        self.scaling = scaling
        self.clock = clock
        self.font = font
        self.flags = {
            "close" : False,
            "play"  : False
        }
        self.currentselection = 0
        self.framecounter = 0
        self.duration = MENU_SECONDS * FRAME_RATE
        for i in range(4):
            image = pygame.image.load(MENU_IMAGES.format(i))
            if scaling != 1:
                self.images.append(pygame.transform.rotozoom(image, 0, scaling))
            else:
                self.images.append(image)
        pygame.mixer.music.load(MENU_MUSIC)
        pygame.mixer.music.play(-1)
        self.menusound = pygame.mixer.Sound(MENU_SOUND)
    
    def mainloop(self):
        while self.framecounter < self.duration and self.flags["close"] == False and self.flags["play"] == False:
            self.clock.tick(FRAME_RATE * self.scaling)
            self.eventloop()
            self.screen.blit(self.images[self.currentselection], [0 ,0])           
            pygame.display.flip()
            self.framecounter += 1
        return {
            "close" : self.flags["close"],
        }
    
    def handlekeypresses(self, event):
        if event.key == pygame.K_UP:
            self.currentselection = (self.currentselection - 1) % 4
            self.menusound.play()
        if event.key == pygame.K_DOWN:
            self.currentselection = (self.currentselection + 1) % 4
            self.menusound.play()                
        if event.key == pygame.K_x:
            self.flags["close"] = True
        if event.key == pygame.K_SPACE:
            if self.currentselection == 0:
                self.flags["play"] = True
            if self.currentselection == 1:
                self.flags["close"] = TextScreen(self.screen, STORY_TEXT, self.font, self.clock, scaling = self.scaling, black = True).mainloop()["close"]
            if self.currentselection == 2:
                self.flags["close"] =TextScreen(self.screen, ScoreGetter().createtext(), self.font, self.clock, scaling = self.scaling, black = True).mainloop()["close"]
            if self.currentselection == 3:
                self.flags["close"] = TextScreen(self.screen, INSTRUCTIONS_TEXT, self.font, self.clock,scaling = self.scaling, black = True).mainloop()["close"]
