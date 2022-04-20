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
    def __init__(self, game, brain=None, mutate=False, showPredicts=False):
        self.groups = game.allObjects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if isinstance(brain, NeuralNetwork):
            self.brain = brain.copy()
            if mutate:
                self.brain.mutate(mutate_function)
        else:
            self.brain = NeuralNetwork(4, 8, 1)

        self.showPredicts = showPredicts

        self.score = 0
        self.fitness = 0

        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.pos = vec(WIDTH//2, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.color = START_COLOR



        self.image = pg.Surface((self.width, self.height))
        self.image.set_colorkey(BLACK)

        pg.draw.circle(self.image, self.color, (self.width//2, self.height//2), self.width//2, 3)
    

        self.image.set_alpha(100)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos



    def copy(self, mutate=False):
        if mutate:
            return Player(self.game, self.brain, True)
        else:
            return Player(self.game, self.brain)

    def decide(self):
        closest = None 
        record = math.inf
        for layer in self.game.layers:
            diff = layer.y - self.pos.y
            if diff > 0 and diff < record:
                record = diff
                closest = layer
        self.inputs = []
        self.inputs.append(normalize(self.pos.x, 0, WIDTH))
        self.inputs.append(normalize(self.vel.x, -15, 15))
        if closest != None:
            self.inputs.append(normalize(closest.left, 0, WIDTH))
            self.inputs.append(normalize(closest.right, 0, WIDTH))
        else:
            self.inputs.append(0.5)
            self.inputs.append(0.6)
        

        if self.showPredicts:
            self.action = self.brain.predict_2(self.inputs)
        else:
            self.action = self.brain.predict(self.inputs)
        self.move(self.action[0])

        


    def update(self):
        self.acc = vec(0, 0)
        self.score += 1

        
        self.decide()
        self.acc.y = GRAVITY
        self.vel += self.acc
        self.vel *= FRICTION
        self.pos += self.vel + 0.5 * self.acc
        
      
        self.rect.centery = self.pos.y
        self.collideWithBlocks('y') 
        self.rect.centerx = self.pos.x
        self.collideWithBlocks('x')
        
        if self.pos.y < 0:
        	self.game.restart()
            

        if self.pos.y > HEIGHT - self.height/2:
            self.pos.y = HEIGHT - self.height/2
            self.vel.y = 0            

        if self.pos.x < 0 + self.width/2:
            self.pos.x = 0 + self.width/2

        if self.pos.x > WIDTH - self.width/2:
            self.pos.x = WIDTH - self.width/2




    def move(self, strength):
        self.acc.x = 1 * strength


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
