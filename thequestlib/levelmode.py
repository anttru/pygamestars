import pygame
from random import randint
from thequestlib import ASTEROIDS_AMOUNT, ASTEROIDS_SPEED, BACKGROUNDS, BACKGROUNDS_NUMBER, EXPLOSION_STOP_FRAMES, FRAME_RATE, LEVEL_MULTIPLIER, LEVEL_MUSIC, PLANET_SPEED, POINTS_TO_PASS, ROCKETS_AMOUNT, ROCKETS_SPEED, SATELLITES_AMOUNT, SATELLITES_SPEED, STAR_SPEEDS, STARS_AMOUNT
from thequestlib.textscreenmode import Mode
from thequestlib.sprites import Asteroid, Explosion, LivesText, PointsText, Rocket, Satellite, Spaceship, Star, Planet 

class Level(Mode):
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font, clock : pygame.time.Clock, lives, points, levelnumber, scaling):
        self.screen = screen
        self.font = font
        self.levelnumber = levelnumber
        self.screencenter = [self.screen.get_width()//2, self.screen.get_height()//2]
        self.scaling = scaling
        self.lives = lives
        self.flags = {
            "dead"     : False,
            "close"    : False,
            "finished" : False,
            "gameover" : False
        }
        self.lifetext = LivesText(self, self.font)
        self.lifetext.rect.topright = [self.screen.get_width() - 20, 0 + 10]
        self.points = points
        self.thislevelpoints = 0
        self.startingpoints = self.points
        self.pointstext = PointsText(self, self.font)
                
        self.startlevel()
        self.stopframes = 0
        self.clock = clock
        self.background = pygame.image.load(BACKGROUNDS.format(self.levelnumber % BACKGROUNDS_NUMBER)).convert()
        if self.scaling != 1:
            self.background = pygame.transform.rotozoom(self.background, 0, self.scaling).convert()
        pygame.mixer.music.load(LEVEL_MUSIC)
        pygame.mixer.music.play(-1)
    
    def startlevel(self):
        self.spaceship = Spaceship(self, self.screen)
        self.sprites = pygame.sprite.Group()
        self.planet = Planet(self, self.screen, speed = PLANET_SPEED)
        self.explosion = Explosion(self, self.screen)
        for speed in STAR_SPEEDS:
            self.generateField(STARS_AMOUNT, self.sprites, Star, speed)
        self.generateField(LEVEL_MULTIPLIER[self.levelnumber % 3] * ASTEROIDS_AMOUNT, self.sprites, Asteroid, ASTEROIDS_SPEED + self.levelnumber // 3)
        self.generateField(LEVEL_MULTIPLIER[self.levelnumber % 3] * ROCKETS_AMOUNT, self.sprites, Rocket, ROCKETS_SPEED + self.levelnumber // 3)
        self.generateField(LEVEL_MULTIPLIER[self.levelnumber % 3] * SATELLITES_AMOUNT, self.sprites, Satellite, SATELLITES_SPEED + self.levelnumber // 3)
        self.sprites.add(self.spaceship)
        self.sprites.add(self.pointstext)
        self.sprites.add(self.planet)
        self.sprites.add(self.lifetext)
        self.sprites.add(self.explosion)

    def generateField(self, amount : int, container : pygame.sprite.Group, spritetype : pygame.sprite.Sprite, speed = 1):
        for i in range(amount):
            position = [randint(0, self.screen.get_width() - 1), randint(0, self.screen.get_height() - 1)]
            sprite = spritetype(self, self.screen, position = position, speed = speed)
            container.add(sprite)
        return container
       
    def detectCollisions(self):
        if self.stopframes == 0:
            for obstacle in self.sprites:
                if isinstance(obstacle, (Asteroid, Rocket, Satellite)):
                    if obstacle.rect.colliderect(self.spaceship.collisionbox):
                        self.lives -= 1
                        self.thislevelpoints -= LEVEL_MULTIPLIER[self.levelnumber % 3] * (ASTEROIDS_AMOUNT + ROCKETS_AMOUNT + SATELLITES_AMOUNT)
                        self.points -= LEVEL_MULTIPLIER[self.levelnumber % 3] * (ASTEROIDS_AMOUNT + ROCKETS_AMOUNT + SATELLITES_AMOUNT) 
                        if self.points < self.startingpoints:
                            self.points = self.startingpoints
                        if self.thislevelpoints < 0:
                            self.thislevelpoints = 0
                        self.explosion.position = obstacle.rect.clip(self.spaceship.collisionbox).topleft
                        if self.lives < 0:
                            self.flags["dead"] = True
                        self.stopframes += 1
                        self.spaceship.crashsound.play()

    def stopstars(self):
        for sprite in self.sprites:
            if isinstance(sprite, Star):
                sprite.speed = 0
    
    def handlestop(self):
        if self.stopframes > 0:
                self.stopframes += 1
        if self.stopframes >= EXPLOSION_STOP_FRAMES * self.scaling:
            if self.flags["dead"] == True:
                self.flags["gameover"] = True
            self.startlevel()
            self.stopframes = 0
    
    def mainloop(self):
        while not self.flags["gameover"] and not self.flags["finished"] and not self.flags["close"]:
            self.clock.tick(FRAME_RATE* self.scaling)

            self.handlestop()
            self.eventloop()
           
            self.detectCollisions()
            self.sprites.update()
                                    
            self.screen.blit(self.background, [0,0])
            self.sprites.draw(self.screen)
            pygame.display.flip()
        return {
            "lives"    : self.lives,
            "points"   : self.points,
            "dead"     : self.flags["dead"],
            "close"    : self.flags["close"]
        }