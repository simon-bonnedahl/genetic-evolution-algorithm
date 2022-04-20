import pygame as pg
from settings import *
from libs.Matrix import *
class NetworkVisualisation(pg.sprite.Sprite):
    def __init__(self, game, player):
        pg.sprite.Sprite.__init__(self, )
        self.game = game
        self.player = player
        self.width = 260
        self.height = 240
        self.image = pg.Surface((self.width, self.height))

    def draw(self):

        for i in range(self.player.brain.inputNodes):
            for j in range(self.player.brain.hiddenNodes):
                pg.draw.line(self.image, (20 + Matrix.matrix_to_array(self.player.brain.hidden)[j]*175, 20 + Matrix.matrix_to_array(self.player.brain.hidden)[j]*175, 20 + Matrix.matrix_to_array(self.player.brain.hidden)[j]*175), (40, 50 + 50*i), (130, 15 + 30*j), 1)

        for i in range(self.player.brain.hiddenNodes):
            for j in range(self.player.brain.outputNodes):
                pg.draw.line(self.image, (20 + Matrix.matrix_to_array(self.player.brain.hidden)[i]*175, 20 + Matrix.matrix_to_array(self.player.brain.hidden)[i]*175, 20 + Matrix.matrix_to_array(self.player.brain.hidden)[i]*175), (130, 15 + 30*i), (220, 120 + 40*j), 1)

        for i in range(self.player.brain.inputNodes):
            pg.draw.circle(self.image, (LIGHTGREY), (40, 50 + 50*i), 15)
            
        for i in range(self.player.brain.hiddenNodes):
        	pg.draw.circle(self.image, (LIGHTGREY), (130, 15 + 30*i), 15)

        for i in range(self.player.brain.outputNodes):
        	pg.draw.circle(self.image, (LIGHTGREY), (220, 120 + 40*i), 20)



        for i in range(self.player.brain.inputNodes):
            self.game.drawText(str(round(self.player.inputs[i], 2)), 'arial', 12, WHITE, 40, 50 + 50*i, surface=self.image, align="center")

        for i in range(self.player.brain.hiddenNodes):
            self.game.drawText(str(round(Matrix.matrix_to_array(self.player.brain.hidden)[i], 2)), 'arial', 12, WHITE, 130, 15 + 30*i, surface=self.image, align="center")

        self.game.drawText(str(round(self.player.action[0], 2)), 'arial', 12, WHITE, 220, 120, surface=self.image, align="center")



    """ for i in range(self.player.brain.inputNodes):
            pg.draw.circle(self.image, (LIGHTGREY), (40, 40 + 40*i), 12)
            
        for i in range(self.player.brain.hiddenNodes):
            pg.draw.circle(self.image, (LIGHTGREY), (130, 12 + 25*i), 12)
        for i in range(self.player.brain.outputNodes):
            pg.draw.circle(self.image, (LIGHTGREY), (220, 100 + 40*i), 12)

        for i in range(self.player.brain.inputNodes):
            for j in range(self.player.brain.hiddenNodes):
                pg.draw.line(self.image, (LIGHTGREY), (40, 40 + 40*i), (130, 12 + 25*j), 1)

        for i in range(self.player.brain.hiddenNodes):
            for j in range(self.player.brain.outputNodes):
                pg.draw.line(self.image, (LIGHTGREY), (130, 12 + 25*i), (220, 100 + 40*j), 1)

        for i in range(self.player.brain.inputNodes):
            self.game.drawText(str(round(self.player.inputs[i], 2)), 'arial', 11, WHITE, 40, 40 + 40*i, surface=self.image, align="center")

        for i in range(self.player.brain.hiddenNodes):
            self.game.drawText(str(round(Matrix.matrix_to_array(self.player.brain.hidden)[i], 2)), 'arial', 11, WHITE, 130, 12 + 25*i, surface=self.image, align="center")

        self.game.drawText(str(round(self.player.action[0], 2)), 'arial', 11, WHITE, 220, 100, surface=self.image, align="center")
"""