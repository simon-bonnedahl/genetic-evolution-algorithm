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
    def __init__(self, game, brain=None, mutate=False, color=WHITE):
        self.groups = game.allObjects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if isinstance(brain, NeuralNetwork):
            self.brain = brain.copy()
            if mutate:
                self.brain.mutate(mutate_function)
                self.color = color
            self.color = color
        else:
            self.brain = NeuralNetwork(4, 8, 1)
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.score = 0
        self.fitness = 0

        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.pos = vec(WIDTH//2, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.image = pg.Surface((self.width, self.height))

        pg.draw.circle(self.image, self.color, (self.width//2, self.height//2), self.width//2, 4)

        self.image.set_alpha(125)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.deathtime = 20


    def copy(self, mutate=True):

        if mutate:
            red = max(0, min(255, self.color[0] + random.randint(-50, 50)))
            blue = max(0, min(255, self.color[1] + random.randint(-50, 50)))
            green =  max(0, min(255, self.color[2] + random.randint(-50, 50)))
            return Player(self.game, self.brain, mutate=True, color=(red, blue, green))

        else:
            return Player(self.game, self.brain, color=self.color)

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
            self.inputs.append(0.5)



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
            if len(self.game.activePlayers) >= 1:
                self.game.bestPlayer = self
            self.game.activePlayers.remove(self)
            self.kill()

        if self.pos.y > HEIGHT - self.height/2:
            self.pos.y = HEIGHT - self.height/2
            self.vel.y = 0

        if self.pos.x < 0 + self.width/2:
            self.pos.x = 0 + self.width/2
            if self.deathtime <= 0:
                if len(self.game.activePlayers) >= 1:
                    self.game.bestPlayer = self
                self.game.activePlayers.remove(self)
                self.kill()
            else:
                self.deathtime -= 1

        if self.pos.x > WIDTH - self.width/2:
            self.pos.x = WIDTH - self.width/2
            if self.deathtime <= 0:
                if len(self.game.activePlayers) >= 1:
                    self.game.bestPlayer = self
                self.game.activePlayers.remove(self)
                self.kill()
            else:
                self.deathtime -= 1


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
