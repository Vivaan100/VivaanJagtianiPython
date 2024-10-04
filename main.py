# This file was created by: Vivaan Jagtiani

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from os import path
from random import randint


# created a game class to use later
# it will have all important parts for the game to run
# the class is needed to organize the different parts of the game
class Game:
    # The game init method initializes all the necessary components for the game which includes video and sound
    # this includes the game clock(sets framerate: what is a framerate???)
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Vivaan's Game")
        self.clock = pg.time.Clock()
        self.running = True
    # create player block, creates the all_sprites group so they can batch update and render, defines properties that can be seen in the game system
    #
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))
    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        # COMMENTED THIS PIECE OF CODE OUT(WE CAN USE IT LATER BY UNCOMMENTING IT)
        # self.player = Player(self, 1, 1)
        # instantiated a mob
        # self.mob = Mob(self, 100,100)
        # makes new mobs and walls using a for loop
        # for i in range(randint(10,20)):
        #     m = Mob(self, i*randint(0, 200), i*randint(0, 200))
        #     Wall(self, i*TILESIZE, i*TILESIZE)
        
        # takes map.data and parses(???) using enumerate, so that we can assign x,y values to object instances.
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
    # using self.running as a boolean to continue running the game
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        # input
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

        # pg.quit()
        # process
    def update(self):
        self.all_sprites.update()
        # output
        pass
    # CREATING THE FONT, TEXT SIZE, COLOR OF THE TEXT, ETC. 
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
        # CREATES TEXT WHEN YOU PRINT THE GAME, LIKE THE TIMER AND A HEADING AT THE TOP
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "This game is awesome...", 24, BLACK, WIDTH/2, HEIGHT/24)
        pg.display.flip()

# checks file name and creates a game object
if __name__ == "__main__":
    g = Game()
    # create all game elements with the new method (not function)
    g.new()
    # run the game...
    g.run()

        

    g.new()

    g.run()           




                
