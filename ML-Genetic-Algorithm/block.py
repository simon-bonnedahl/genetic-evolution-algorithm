import pygame as pg
from settings import *

vec = pg.math.Vector2

class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.allObjects, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(LIGHTGREY)
        pg.draw.rect(self.image, (0, 0, 0), (0, 0, self.width, self.height), 3)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
