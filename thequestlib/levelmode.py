import pygame
from random import randint
from thequestlib import ASTEROIDS_AMOUNT, ASTEROIDS_SPEED, BACKGROUNDS, BACKGROUNDS_NUMBER, EXPLOSION_SPRITE, EXPLOSION_STOP_FRAMES, FRAME_RATE, LEVEL_MULTIPLIER, LEVEL_MUSIC, ROCKETS_AMOUNT, ROCKETS_SPEED, SATELLITES_AMOUNT, SATELLITES_SPEED, STAR_SPEEDS, STARS_AMOUNT
from thequestlib.textscreenmode import Mode
from thequestlib.sprites import Asteroid, LivesText, PointsText, Rocket, Satellite, Spaceship, Star, Planet 

class Level(Mode):
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font, clock : pygame.time.Clock, lives, points, levelnumber, scaling):
        self.screen = screen
        self.font = font
        self.levelnumber = levelnumber
        self.screencenter = [self.screen.get_width()//2, self.screen.get_height()//2]
        self.scaling = scaling
        self.lives = lives
        self.finished = False
        self.dead = False
        self.autopilot = False
        self.explosioncenter = None
        self.close = False
        self.lifetext = LivesText(self, self.font)
        self.lifetext.rect.topright = [self.screen.get_width() - 20, 0 + 10]
        self.points = points
        self.thislevelpoints = 0
        self.pointstext = PointsText(self, self.font)

        
        self.startlevel()
        self.stopframes = 0
                
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(BACKGROUNDS.format(self.levelnumber % BACKGROUNDS_NUMBER)).convert()
        if self.scaling != 1:
            self.background = pygame.transform.rotozoom(self.background, 0, self.scaling)
        pygame.mixer.music.load(LEVEL_MUSIC)
        pygame.mixer.music.play(-1)
    
    def startlevel(self):
        self.spaceship = Spaceship(self, self.screen)
        self.sprites = pygame.sprite.Group()
        self.planet = Planet(self, self.screen)
        for speed in STAR_SPEEDS:
            self.generateField(STARS_AMOUNT, self.sprites, Star, speed)
        self.generateField(LEVEL_MULTIPLIER[self.levelnumber % 3] * ASTEROIDS_AMOUNT, self.sprites, Asteroid, ASTEROIDS_SPEED + self.levelnumber // 3)
        self.generateField(LEVEL_MULTIPLIER[self.levelnumber % 3] * ROCKETS_AMOUNT, self.sprites, Rocket, ROCKETS_SPEED + self.levelnumber // 3)
        self.generateField(LEVEL_MULTIPLIER[self.levelnumber % 3] * SATELLITES_AMOUNT, self.sprites, Satellite, SATELLITES_SPEED + self.levelnumber // 3)
        self.sprites.add(self.spaceship)
        self.sprites.add(self.pointstext)
        self.sprites.add(self.planet)
        self.sprites.add(self.lifetext)

    def generateField(self, amount : int, container : pygame.sprite.Group, spritetype : pygame.sprite.Sprite, speed = 1):
        for i in range(amount):
            position = [randint(0, self.screen.get_width() - 1), randint(0, self.screen.get_height() - 1)]
            sprite = spritetype(self, self.screen, position = position, speed = speed)
            container.add(sprite)
        return container

    def explosion(self,position, framecounter):
        if self.explosioncenter != None:
            explosion = pygame.image.load(EXPLOSION_SPRITE.format(framecounter//10))
            position = (position[0] - explosion.get_width()//2, position[1] - explosion.get_height()//2)
            self.screen.blit(explosion, position)
        
    def detectCollisions(self):
        if self.stopframes == 0:
            for obstacle in self.sprites:
                if isinstance(obstacle, (Asteroid, Rocket, Satellite)):
                    if obstacle.rect.colliderect(self.spaceship.collisionbox):
                        self.lives -= 1
                        self.thislevelpoints -= LEVEL_MULTIPLIER[self.levelnumber % 3] * (ASTEROIDS_AMOUNT + ROCKETS_AMOUNT + SATELLITES_AMOUNT)
                        self.points -= LEVEL_MULTIPLIER[self.levelnumber % 3] * (ASTEROIDS_AMOUNT + ROCKETS_AMOUNT + SATELLITES_AMOUNT) 
                        if self.points < 0:
                            self.points = 0
                        if self.thislevelpoints < 0:
                            self.thislevelpoints = 0
                        self.explosioncenter = obstacle.rect.clip(self.spaceship.collisionbox).topleft
                        if self.lives < 0:
                            self.dead = True
                        self.stopframes += 1
                        self.spaceship.crashsound.play()

    def stopstars(self):
        for sprite in self.sprites:
            if isinstance(sprite, Star):
                sprite.speed = 0
            

    def handlestop(self):
        if self.stopframes > 0:
                self.stopframes += 1
        if self.stopframes >= EXPLOSION_STOP_FRAMES:
            if self.dead == True:
                self.game_over = True
            self.startlevel()
            self.stopframes = 0
            self.explosioncenter = None

    def mainloop(self):
        while not self.game_over and not self.finished and not self.close:
            self.clock.tick(FRAME_RATE* self.scaling)

            self.handlestop()

            self.eventloop()
           
            self.detectCollisions()
            self.sprites.update()
                                    
            self.screen.blit(self.background, [0,0])
            self.sprites.draw(self.screen)
            self.explosion(self.explosioncenter, self.stopframes)
            
            pygame.display.flip()
        return {
            "lives"    : self.lives,
            "points"   : self.points,
            "dead"     : self.dead,
            "close"    : self.close
        }