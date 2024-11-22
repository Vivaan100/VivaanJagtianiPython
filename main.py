import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from os import *
import sys
from random import randint

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Vivaan's Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0  # Initialize the score to 0

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

    def new(self):
        self.load_data()  # Loads all of the sprites
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()

        # Parse the map data and create game objects
        for row, tiles in enumerate(self.map.data):  # Connects to level1.txt
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)
                elif tile == 'C':
                    Coin(self, col, row)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000  # The amount of time per frame
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False  # Ends the game

    def update(self):
        self.all_sprites.update()
        
    # Update player's position based on velocity and colliding with walls
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

   
        self.rect.x = self.x
        self.collide_with_walls

        self.rect.y = self.y
        self.collide_with_walls  

        self.rect.x = self.x
        self.rect.y = self.y

    def draw_text(self, surface, text, size, color, x, y):  # Font, colors, and position of the text
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        # Display the score
        self.draw_text(self.screen, f"Score: {self.score}", 24, BLACK, WIDTH / 2, 10)
        
        self.draw_text(self.screen, str(int(self.dt * 1000)), 24, WHITE, WIDTH / 30, HEIGHT / 30)
        self.draw_text(self.screen, "This game is sooooo...awesome...", 24, BLACK, WIDTH / 2, HEIGHT / 24)
        pg.display.flip()
        self.draw_text(self.screen, str(int(self.dt * 2000)), 24, BLACK, WIDTH / 30, HEIGHT / 30)
        self.draw_text(self.screen, "Health: ____", 24, BLACK, WIDTH / 200, HEIGHT / 40)
        pg.display.flip()


class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.speed = 500  # Adjust player speed

    def collide_with_walls(self, dir):
        # Horizontal collision handling (left/right)
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vx > 0:  # Moving right
                    self.x = hits[0].rect.left - TILESIZE
                if self.vx < 0:  # Moving left
                    self.x = hits[0].rect.right
                self.vx = 0  # Stop horizontal movement
            self.rect.x = self.x
         # Vertical collision handling (up/down)
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:  # Moving down
                    self.y = hits[0].rect.top - TILESIZE
                if self.vy < 0:  # Moving up
                    self.y = hits[0].rect.bottom
                self.vy = 0  # Stop vertical movement
            self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.rect.y = self.y

        self.collide_with_walls()
        self.collect_coins()

    def get_keys(self):
        keys = pg.key.get_pressed()
        self.vx, self.vy = 0, 0
        if keys[pg.K_UP]:
            self.vy = -self.speed
        if keys[pg.K_LEFT]:
            self.vx = -self.speed
        if keys[pg.K_DOWN]:
            self.vy = self.speed
        if keys[pg.K_RIGHT]:
            self.vx = self.speed

    def collide_with_walls(self):
        # Placeholder method to handle wall collisions
        pass

    def collect_coins(self):
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)  # Remove coin after collection
        for hit in hits:
            self.game.score += 1  # Increment the score when collecting a coin
            print(f"Coins Collected: {self.game.score}")


class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)  # Coin color
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Additional classes (Wall, Mob, etc.) will remain unchanged

if __name__ == "__main__":
    g = Game()
    g.new()  # Initialize game elements
    g.run()  # Start the game
