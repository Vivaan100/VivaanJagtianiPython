# This file was created by: Vivaan Jagtiani

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from os import *
import sys
from random import randint
'''
GOALS: Get to the middle square without touching any enemies
RULES: Get a find a powerup to not get eating by an enemy
FEEDBACK: collide with enemy before eat powerup you die
FREEDOM: Move around





'''



# Game class to organize the various parts of the game
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Vivaan's Game")
        self.clock = pg.time.Clock()
        self.running = True

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

    def new(self):
        self.load_data()# Loads all of the sprites 
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()

        # Parse the map data and create game objects
        for row, tiles in enumerate(self.map.data):# connects to level1.txt
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000# the amount of time
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False# Ends the game

    def update(self):
        self.all_sprites.update()

    def draw_text(self, surface, text, size, color, x, y):# the font, colors, size, of the words that show up on the screen
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(int(self.dt * 1000)), 24, WHITE, WIDTH / 30, HEIGHT / 30)
        self.draw_text(self.screen, "This game is sooooo...awesome...", 24, BLACK, WIDTH / 2, HEIGHT / 24)
        pg.display.flip()

# Checks file name and creates a game object
if __name__ == "__main__":
    g = Game()
    g.new()  # Initialize game elements
    g.run()  # Start the game
