import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from os import path
import sys
from random import randint

'''
Goals: Collected all of the coins without touching the mobs before the timer ends.
Freedom: You can move around freely
Rules: You have to collect the coins without touching mobs.
Feedback: You touch mob, then you die

CHATGPT AI: 
1.) Question: With this code(inserted code), can you explain how to add a score tally. 
2.) Question: With this code(inserted code), can you explain how to fix my timer, as it does not work)
3.) Question: Can you help me fix the walls, as the player is just going through them. 
4.) Question: What is wrong with my code, as the when the player collides with the mob, it 



'''
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.start_time = pg.time.get_ticks()  # Timer start time
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Vivaan's Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0  # Initialize score
        self.all_coins = pg.sprite.Group()
        self.coins_collected = 0  # Track coins collected

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level1.txt'))

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.start_time = pg.time.get_ticks()  # Reset timer on new game

        for row, tiles in enumerate(self.map.data):
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
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()

        # Check for collision with mobs
        if pg.sprite.spritecollide(self.player, self.all_mobs, False):
            self.show_game_over_screen()  # End game if player touches mob

        # Check if player has collected 7 coins
        if self.coins_collected >= 7:
            self.show_game_over_screen()  # End game when player reaches score of 7

        # Update coins collected from player
        self.coins_collected = self.player.coins_collected

        # Check elapsed time
        elapsed_time = (pg.time.get_ticks() - self.start_time) / 1000
        if elapsed_time > 30:  # Timer ends after 30 seconds
            self.show_game_over_screen()

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        # Display the score and coins collected
        self.draw_text(self.screen, f"Score: {self.coins_collected}", 24, BLACK, WIDTH / 2, 10)

        # Display the countdown timer
        elapsed_time = (pg.time.get_ticks() - self.start_time) / 1000
        remaining_time = max(0, 30 - int(elapsed_time))  # Ensure no negative time
        self.draw_text(self.screen, f"Time: {remaining_time}s", 24, BLACK, WIDTH / 2 + 100, 10)

        pg.display.flip()

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def show_game_over_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "GAME OVER", 72, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text(self.screen, f"Your Score: {self.coins_collected}", 36, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press R to Restart or Q to Quit", 24, WHITE, WIDTH / 2, HEIGHT / 1.5)
        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.new()  # Restart the game
                        waiting = False
                    if event.key == pg.K_q:
                        self.running = False
                        waiting = False







if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
