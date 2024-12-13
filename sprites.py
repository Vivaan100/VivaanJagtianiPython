import pygame as pg
from pygame.sprite import Sprite

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
        self.speed = 700
        self.vx, self.vy = 0, 0

    def get_keys(self):
        keys = pg.key.get_pressed()
        self.vx, self.vy = 0, 0
        if keys[pg.K_UP]:
            self.vy -= self.speed
        if keys[pg.K_LEFT]:
            self.vx -= self.speed
        if keys[pg.K_DOWN]:
            self.vy += self.speed
        if keys[pg.K_RIGHT]:
            self.vx += self.speed

    def collide_with_walls(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            if dir == 'x':  # Horizontal collisions
                if self.vx > 0:  # Moving right
                    self.rect.right = hits[0].rect.left
                elif self.vx < 0:  # Moving left
                    self.rect.left = hits[0].rect.right
                self.vx = 0  # Stop horizontal movement
                self.x = self.rect.x  # Update precise position
            elif dir == 'y':  # Vertical collisions
                if self.vy > 0:  # Moving down
                    self.rect.bottom = hits[0].rect.top
                elif self.vy < 0: 
                    self.rect.top = hits[0].rect.bottom
                self.vy = 0  # Stop vertical movement
                self.y = self.rect.y  
    def collect_coins(self):
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)  # Remove coins upon collision
        for hit in hits:
            self.game.coins_collected += 1  # Increment coins collected
            print(f"Coins collected: {self.game.coins_collected}")

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')

        self.collect_coins()
        # Check for collision with mobs
        if pg.sprite.spritecollide(self, self.game.all_mobs, False):  # If the player collides with a mob
            self.game.running = False  # Stop the game loop
            self.game.game_over()  # Call the game-over function


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

    def collide_with_walls(self):  # What happens to direction when the mobs collide with the wall
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            if self.direction > 0:  # Move right when hit wall
                self.rect.right = hits[0].rect.left
            if self.direction < 0:  # Move left when hit wall
                self.rect.left = hits[0].rect.right
            self.direction *= -1  # Change direction


class Wall(Sprite):  # Creating the wall sprite
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Creating physical image of wall
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)  # Creating the color of the wall(Blue)
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
    def __init__(self, game, x, y):  # Initializing sprite(Coin)
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Creating image of coin
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)  # Color of the coin
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
