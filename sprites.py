import pygame as pg
from pygame.sprite import Sprite
from settings import *

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
        self.coins_collected = 0  # Track coins collected

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
            self.coins_collected += 1  # Increment coins collected
            print(f"Coins collected: {self.coins_collected}")

    def check_mob_collision(self):
        # Check if player touches a mob
        if pg.sprite.spritecollide(self, self.game.all_mobs, False):
            self.game.show_game_over_screen()  # End game immediately

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')

        self.collect_coins()
        self.check_mob_collision()  # Check for mob collisions in each update cycle


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
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
        self.collide_with_walls()

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1  # Change direction when Mob hits wall

    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            if self.direction > 0:  # Moving right
                self.rect.right = hits[0].rect.left
            if self.direction < 0:  # Moving left
                self.rect.left = hits[0].rect.right
            self.direction *= -1  # Change direction when wall is hit


class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Wall image
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)  # Blue wall color
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass  # Static, no update needed


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Coin image
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)  # Yellow coin color
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
