import random
from settings import *
from to_excel import *
import sys
sys.path.append("..")

class GeneticAlgorithm():
	"""doctring for GeneticAlgorithm"""
	def __init__(self, game):
		self.game = game
		self.data = {'Generation': [0], 'Best Score': [0], 'Average Score': [0]}
		self.writer, self.df = create_table(self.data)
		self.pow = POW
		
	def nextGeneration(self):
		self.calculateFitness()
		self.data['Generation'][0] = self.game.generation
		self.data['Best Score'][0] = self.game.highScore
		self.data['Average Score'][0] = round((self.totalSum/POPULATION_SIZE)**(1/self.pow))


		self.df = write_to_excel(self.df, self.writer, self.data)

		self.game.activePlayers = self.generate(self.game.allPlayers)

		self.game.allPlayers = self.game.activePlayers.copy()

		self.game.generation += 1


	def calculateFitness(self):
		self.totalSum = 0
		for player in self.game.allPlayers:
			player.score = player.score**self.pow

		for player in self.game.allPlayers:
			self.totalSum += player.score

		for player in self.game.allPlayers:
			player.fitness = player.score / self.totalSum


	def generate(self, oldPlayers):
		newPlayers = []
		for player in oldPlayers:
			player = self.poolSelection(oldPlayers)
			newPlayers.append(player)
		return newPlayers

	def poolSelection(self, players):
		index = 0
		r = random.random()

		while r > 0:
			r -= players[index].fitness
			index += 1

		index -= 1
		return players[index].copy()
