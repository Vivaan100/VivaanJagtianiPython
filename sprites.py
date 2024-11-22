import pygame as pg
from pygame.sprite import Sprite
import random

# Constants
WIDTH, HEIGHT = 800, 600
TILESIZE = 32
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Added yellow color
PINK = (255, 105, 180)

class Player(Sprite):
    def __init__(self, game, x, y):
        self.health = 100
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 700  # Speed of player in pixels per second, so 200 pixels per second
        self.vx, self.vy = 0, 0
        self.coins_collected = 0

    def get_keys(self):
        keys = pg.key.get_pressed()
        self.vx, self.vy = 0, 0  # using these to make the player move with the arrow keys
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
                    self.x = hits[0].rect.left - TILESIZE
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

    def collect_coins(self):
        # Check for collisions with coins and collect them
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)  # 'True' removes the coin
        for hit in hits:
            self.game.coins_collected += 1  # Increment coin count
            print(f"Coins collected: {self.game.coins_collected}")

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')

        self.collect_coins()  # Check for coin collection after moving


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 300
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        self.rect.x += self.speed * self.direction * self.game.dt
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1  # Change direction when Player hits wall
        self.collide_with_walls()

    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            if self.direction > 0:  # Move right when hit wall
                self.rect.right = hits[0].rect.left
            if self.direction < 0:  # Move left when hit wall
                self.rect.left = hits[0].rect.right
            self.direction *= -1 #change direction???

class Wall(Sprite):
    def __init__(self, game, x, y): # intialize sprites(wall)
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))# creating physical image of wall
        self.rect = self.image.get_rect()
        self.image.fill(BLUE) # creating the color of the wall(Blue)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def update(self):
            # Movement code here...
        
        # Check for collision with mobs
        if pg.sprite.spritecollide(self, self.game.all_mobs, False):
            self.health -= 10  # Reduce health
            print(f"Health: {self.health}")
            if self.health <= 0:
                self.game.running = False  # End game on death


class Coin(Sprite):
    def __init__(self, game, x, y): # initializing sprite(Coin)
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))# creating image of coin
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)# color of the coin
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Game:
    def __init__(self): # initializing game
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()  # Group for coins
        
        self.player = Player(self, 5, 5)  # Start player at (5, 5)
        
        # Create walls
        for x in range(0, WIDTH // TILESIZE):
            Wall(self, x, HEIGHT // TILESIZE - 1)  
        for y in range(0, HEIGHT // TILESIZE):
            Wall(self, 0, y)  # Left wall
            Wall(self, WIDTH // TILESIZE - 1, y)  # Right wall
        
        for x in range(5, 15):
            Wall(self, x, 10)  # Create horizontal wall

        # Create coins
        for x in range(7, 10):
            Coin(self, x, 5)  # Add coins at specific positions

        # Create a mob
        self.mob = Mob(self, 3, 5)  # Start mob at (3, 5)

        self.coins_collected = 0  # Initialize collected coins count
        self.running = True

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000  # Amount of seconds between each loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            
            self.all_sprites.update()  # Update all sprites
            
            self.screen.fill((0, 0, 0))  # Fill the screen with black
            self.all_sprites.draw(self.screen)  # Draw all sprites
            pg.display.flip()  # Update the display

        def new(self):
            self.load_data()  # Loads map data, etc.
            self.all_sprites = pg.sprite.Group()
            self.all_walls = pg.sprite.Group()  # Group for walls
            self.all_mobs = pg.sprite.Group()
            self.all_powerups = pg.sprite.Group()
            self.all_coins = pg.sprite.Group()

        pg.quit()  # Quit Pygame when done




if __name__ == "__main__":
    game = Game()
    game.run()
