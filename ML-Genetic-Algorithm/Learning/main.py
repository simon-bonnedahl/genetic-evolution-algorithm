import random
from settings import *
from player import *
from layer import *
import pygame as pg
from geneticAlgorithm import *
import pickle
import os
import pdb


class Main():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH + 300, HEIGHT))
        pg.display.set_caption("Learning")
        self.clock = pg.time.Clock()
        self.ga = GeneticAlgorithm(self)
        self.generation = 1

        self.totalPopulation = POPULATION_SIZE
        self.activePlayers = []
        self.allPlayers = []
        self.layers = []

        self.allObjects = pg.sprite.Group()
        self.blocks = pg.sprite.Group()

        self.timer = 0
        self.level = 0
        self.highScore = 0

        self.cycles = 1

        self.showWeights = False
        self.showText = False

        self.layer_spawning_speed = LAYER_SPAWNING_SPEED

        self.bestPlayer = None
        self.showBestPlayer = False


        start_layer = Layer(self)
        self.layers.append(start_layer)
        for i in range(self.totalPopulation):
            player = Player(self)
            self.activePlayers.append(player)
            self.allPlayers.append(player)


    def run(self):
        #pg.display.set_caption("FPS:{:.0f}".format(self.clock.get_fps()))
        self.dt = self.clock.tick(FPS) / 1000
        for i in range(self.cycles):
            self.update()

        self.events()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_w:
                    self.showWeights = not self.showWeights
                if event.key == pg.K_t:
                    self.showText = not self.showText
                if event.key == pg.K_SLASH:
                    self.cycles -= 1
                if event.key == pg.K_MINUS:
                    self.cycles += 1
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pg.mouse.get_pos()
                    if WIDTH + 20 < x < WIDTH + 120:
                        if 300 < y < 340:
                            if self.bestPlayer != None:
                                list = os.listdir("../RunBrains/SavedBrains")
                                number_files = len(list)
                                with open("../RunBrains/SavedBrains/Brain0{}".format(number_files), 'wb') as output:
                                    pickle.dump(self.bestPlayer.brain, output, pickle.HIGHEST_PROTOCOL)
                                    print("Saved the brain as Brain0{}".format(number_files))


    def update(self):
        if len(self.activePlayers) <= 0:
            self.restart()

        if self.activePlayers[0].score > self.highScore:
            self.highScore = self.activePlayers[0].score

        self.timer += 1
        if self.timer >= self.layer_spawning_speed:
            self.level += 1
            self.layer_spawning_speed -= 0.1


            self.timer = 0
            layer = Layer(self)
            layer.speed += self.level/100
            self.layers.append(layer)

        for player in self.activePlayers:
            player.update()

        for layer in self.layers:
            layer.update()

    def draw(self):
        self.screen.fill(BGCOLOR)
        pg.draw.line(self.screen, BLACK, (WIDTH, 0), (WIDTH, HEIGHT), 3)
        if self.drawText:
            self.drawText(("Generation: " + str(self.generation)), 'arial', 30, WHITE, WIDTH + 20, 20)
            try:
                self.drawText(("Score: " + str(self.activePlayers[0].score)), 'arial', 30, WHITE, WIDTH + 20, 60)
            except:
                self.drawText(("Score: " + str(0)), 'arial', 30, WHITE, WIDTH + 20, 60)

            self.drawText(("Highscore: " + str(self.highScore)), 'arial', 30, WHITE, WIDTH + 20, 100)
            self.drawText(("Speed: " + str(round(self.layers[0].speed, 2))), 'arial', 30, WHITE, WIDTH + 20, 140)
            #self.drawText(("Alive: " + str(len(self.activePlayers))), 'arial', 30, WHITE, WIDTH + 20, 180)
            #self.drawText(("Update Cycles: " + str(self.cycles)), 'arial', 30, WHITE, WIDTH + 20, 220)
            pg.draw.rect(self.screen, BLACK, (WIDTH + 20, 300, 100, 40), 1)
            self.drawText("Save", 'arial', 30, WHITE, WIDTH + 30, 300)
        else:
            pass
        if self.showWeights and self.bestPlayer != None:
            for i in range(len(self.bestPlayer.brain.weights_input_hidden.data)):
                for j in range(len(self.bestPlayer.brain.weights_input_hidden.data[i])):
                    self.drawText(str(round(self.bestPlayer.brain.weights_input_hidden.data[i][j],2)), 'arial', 14, WHITE, WIDTH + 20 + (50*j), 450 + (40 * i))
            for i in range(len(self.bestPlayer.brain.weights_hidden_output.data[0])):
                self.drawText(str(round(self.bestPlayer.brain.weights_hidden_output.data[0][i], 2)), 'arial', 14, WHITE, WIDTH + 250, 450 + (40 * i))

        self.allObjects.draw(self.screen)
        pg.display.flip()


    def quit(self):
        pg.quit()
        sys.exit(0)

    def restart(self):
        self.layer_spawning_speed = LAYER_SPAWNING_SPEED
        self.allObjects = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.timer = 0
        self.level = 0
        self.layers = []
        start_layer = Layer(self)
        self.layers.append(start_layer)
        self.allPlayers.remove(self.bestPlayer)
        self.ga.nextGeneration()
        self.bestPlayer = self.bestPlayer.copy(False)
        pg.draw.circle(self.bestPlayer.image, RED, (self.bestPlayer.width//2, self.bestPlayer.height//2), self.bestPlayer.width//4, 10)
        self.activePlayers.append(self.bestPlayer)
        self.allPlayers.append(self.bestPlayer)

    def drawText(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)



m = Main()

while True:
    m.run()
