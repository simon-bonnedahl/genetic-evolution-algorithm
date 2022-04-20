import pygame as pg
from settings import *
import random
import math
import sys
sys.path.append("..")
from libs.neural_network import *
vec = pg.math.Vector2

def mutate_function(x):
    if random.random() < MUTATE_PRECENTAGE:
        offset = random.gauss(0, STD_DEV)
        newX = x + offset
        return newX
    else:
        return x

def normalize(value, min, max):
    return (value - min) / (max - min)


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.allObjects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
       
        self.color = WHITE
        self.score = 0


        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.pos = vec(WIDTH//2, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.image = pg.Surface((self.width, self.height))
        self.image.set_colorkey(BLACK)
        pg.draw.circle(self.image, self.color, (self.width//2, self.height//2), self.width//2, 4)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos



    def update(self):
        self.acc = vec(0, 0)
        self.score += 1

        self.getInputs()
        self.acc.y = GRAVITY
        self.vel += self.acc
        self.vel *= FRICTION
        self.pos += self.vel + 0.5 * self.acc
        
      
        self.rect.centery = self.pos.y
        self.collideWithBlocks('y') 
        self.rect.centerx = self.pos.x
        self.collideWithBlocks('x')
        
        


        if self.pos.y < 0:
            self.kill()
            self.game.restart()

        if self.pos.y > HEIGHT - self.height/2:
            self.pos.y = HEIGHT - self.height/2
            self.vel.y = 0            

        if self.pos.x < 0 + self.width/2:
            self.pos.x = 0 + self.width/2

        if self.pos.x > WIDTH - self.width/2:
            self.pos.x = WIDTH - self.width/2



    def getInputs(self):
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_d] or self.keys[pg.K_RIGHT]:
            self.right()
        if self.keys[pg.K_a] or self.keys[pg.K_LEFT]:
            self.left()


    def right(self):
        self.acc.x = 1

    def left(self):
        self.acc.x = -1



    def collideWithBlocks(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.centerx = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:

                self.pos.y = hits[0].rect.top - self.rect.height / 2 

                self.vel.y = hits[0].vel.y
                self.rect.centery = self.pos.y
            