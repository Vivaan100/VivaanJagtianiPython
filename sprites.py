# This file was created by: Vivaan Jagtiani
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random

# Constants
WIDTH, HEIGHT = 800, 600
TILESIZE = 32
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)

class Player(Sprite):# creating the player class, which stores all of the data for it
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)# color of the player
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 200  # Speed in pixels per second
        self.vx, self.vy = 0, 0

    def get_keys(self):# movement of the player using the arrow keys
        keys = pg.key.get_pressed()
        self.vx, self.vy = 0, 0  # Reset velocity
        if keys[pg.K_UP]:
            self.vy -= self.speed
        if keys[pg.K_LEFT]:
            self.vx -= self.speed
        if keys[pg.K_DOWN]:
            self.vy += self.speed
        if keys[pg.K_RIGHT]:
            self.vx += self.speed

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vx > 0:  # Moving right
                    self.x = hits[0].rect.left - TILESIZE# all once the player hits the wall
                if self.vx < 0:  # Moving left
                    self.x = hits[0].rect.right
                self.vx = 0
            self.rect.x = self.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:  # Moving down
                    self.y = hits[0].rect.top - TILESIZE
                if self.vy < 0:  # Moving up
                    self.y = hits[0].rect.bottom
                self.vy = 0
            self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')
# player updates whenever there is a collision

class Mob(Sprite):# creating the mob class, which stores all of the information for it
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 100
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        self.rect.x += self.speed * self.direction * self.game.dt
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1  # when player hits the walls, it will change direction


class Wall(Sprite):# creating the wall sprites, which stores all of the data for it
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# making the game class
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()#time
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        
        self.player = Player(self, 5, 5) # Starts the  player at [position (5, 5)
        
        # Create walls
        for x in range(0, WIDTH // TILESIZE):
            Wall(self, x, HEIGHT // TILESIZE - 1)  
        for y in range(0, HEIGHT // TILESIZE):
            Wall(self, 0, y)  # Left wall
            Wall(self, WIDTH // TILESIZE - 1, y)  
        
        
        for x in range(5, 15):
            Wall(self, x, 10)

        # Create a mob
        self.mob = Mob(self, 3, 5)  # Start mob at the position (3, 5)

        self.running = True

    def run(self):# whatever happens while running the game
        while self.running:
            self.dt = self.clock.tick(60) / 1000  
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            
            self.all_sprites.update()  # Update all sprites
            self.screen.fill((0, 0, 0))  # Fill the screen with a background color(white)
            self.all_sprites.draw(self.screen)  # Draw all sprites so that we can see them on the screen
            pg.display.flip()  

    
    def collide_with_coins(self):
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        for hit in hits:
            self.coins += 1
            print(f"Coins collected: {self.coins}")

        pg.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
