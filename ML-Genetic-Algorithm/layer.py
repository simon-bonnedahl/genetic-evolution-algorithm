from settings import *
from block import *
import random


class Layer():
	def __init__(self, game):
		self.game = game
		self.holeSize = LAYER_HOLE_SIZE
		self.content = []
		self.y = HEIGHT
		n = random.randint(0, BLOCK_WIDTH - self.holeSize)
		for i in range(n):
			self.content.append(1)
		for i in range(self.holeSize):
			self.content.append(0)
		for i in range(BLOCK_WIDTH - self.holeSize - n):
			self.content.append(1)

		for i in range(len(self.content)):
			if self.content[i] == 1:
				self.content[i] = Block(self.game, (i * BLOCK_SIZE), self.y, BLOCK_SIZE, BLOCK_SIZE)
		
		self.speed = LAYER_STARTING_SPEED

		self.left = n * BLOCK_SIZE
		self.right = self.left + self.holeSize * BLOCK_SIZE
		self.middle = self.left + ((self.holeSize/2) * BLOCK_SIZE)
		
	def update(self):
		for i in range(len(self.content)):
			if isinstance(self.content[i], Block):
				self.content[i].vel.y = -self.speed
				self.content[i].pos += self.content[i].vel
				self.content[i].rect.x, self.content[i].rect.y = self.content[i].pos

		self.y -= self.speed
		if self.y < 0:
			self.game.layers.remove(self)
			for i in range(len(self.content)):
				if isinstance(self.content[i], Block):
					self.content[i].kill()

