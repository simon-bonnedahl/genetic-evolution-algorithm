import random
from settings import *
from player import *
from layer import *
import pygame as pg
from geneticAlgorithm import *
from networkvisualisation import *
import pickle
import os


class Main():
    def __init__(self):
        pg.init()
        brains = os.listdir("SavedBrains")
        for brain in brains:
            print(brain)
        self.brain = input("What brain do you want to pick?")
        q =  "n" #input("Do you want to see how it thinks? (y/n)")
        if q == "y":
            self.printing = True
        elif q == "n":
            self.printing = False

        self.screen = pg.display.set_mode((WIDTH + 300, HEIGHT))
        pg.display.set_caption("Trained")

        self.clock = pg.time.Clock()
        self.fps = FPS

        self.layers = []

        self.allObjects = pg.sprite.Group()
        self.blocks = pg.sprite.Group()

        self.timer = 0
        self.level = 0
        self.highScore = 0


        self.layer_spawning_speed = LAYER_SPAWNING_SPEED

        start_layer = Layer(self)
        self.layers.append(start_layer)
        self.player = Player(self, showPredicts=self.printing)
        with open('SavedBrains/Brain{}'.format(self.brain), 'rb') as i:
            self.player.brain = pickle.load(i)

        self.networkVisualisation = NetworkVisualisation(self, self.player)

    def run(self):
        #pg.display.set_caption("FPS:{:.0f}".format(self.clock.get_fps()))
        self.dt = self.clock.tick(self.fps) / 1000
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
                if event.key == pg.K_LEFT:
                    self.fps -= 5

                if event.key == pg.K_SPACE:
                    print("switch")
                    self.player.showPredicts = not self.player.showPredicts


    def update(self):
        if self.player.score > self.highScore:
            self.highScore = self.player.score

        self.timer += 1
        if self.timer >= self.layer_spawning_speed:
            self.level += 1
            self.layer_spawning_speed -= 0.1
            self.timer = 0
            layer = Layer(self)
            layer.speed += self.level/100
            self.layers.append(layer)

        for layer in self.layers:
            layer.update()
        for obj in self.allObjects:
            obj.update()

    def draw(self):
        self.screen.fill(BGCOLOR)
        pg.draw.line(self.screen, BLACK, (WIDTH, 0), (WIDTH, HEIGHT), 3)
        self.drawText(("Score: " + str(self.player.score)), 'arial', 30, WHITE, WIDTH + 20, 20)
        self.drawText(("Highscore: " + str(self.highScore)), 'arial', 30, WHITE, WIDTH + 20, 60)
        self.drawText(("Speed: " + str(round(self.layers[0].speed, 2))), 'arial', 30, WHITE, WIDTH + 20, 100)
        self.screen.blit(self.networkVisualisation.image, (WIDTH + 20, 200))
        self.networkVisualisation.draw()


        self.allObjects.draw(self.screen)
        pg.display.flip()


    def quit(self):
        pg.quit()

    def restart(self):
        self.layer_spawning_speed = LAYER_SPAWNING_SPEED
        self.allObjects = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Player(self, showPredicts=self.printing)
        self.player.decide()
        with open('SavedBrains/Brain{}'.format(self.brain), 'rb') as i:
            self.player.brain = pickle.load(i)
        self.networkVisualisation = NetworkVisualisation(self, self.player)
        self.timer = 0
        self.level = 0
        self.layers = []
        start_layer = Layer(self)
        self.layers.append(start_layer)

    def drawText(self, text, font_name, size, color, x, y, align="topleft", surface=None):
        font = pg.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        if not surface:
            self.screen.blit(text_surface, text_rect)
        else:
            surface.blit(text_surface, text_rect)



m = Main()

while True:
    m.run()
