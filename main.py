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
        self.score = 0  # Initialize the score to 0 at the beginning of every game.
        self.all_coins = pg.sprite.Group()
        self.coins_collected = 0

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

        # Check elapsed time
        elapsed_time = (pg.time.get_ticks() - self.start_time) / 1000
        if elapsed_time > 30:  # Timer ends
            self.show_game_over_screen()
     
    def game_over(self):
        self.screen.fill(BLACK)  # Fill the screen with a black background
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)  # Display the game-over message
        self.draw_text("Press a key to restart", 22, WHITE, WIDTH / 2, HEIGHT / 2)  # Instruction to restart

        pg.display.flip()  # Update the display

        # Wait for the user to press a key
        self.wait_for_key()
        self.new()  # Restart the game        

    def draw_text(self, surface, text, size, color, x, y):
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

        # Display the countdown timer
        elapsed_time = (pg.time.get_ticks() - self.start_time) / 1000
        remaining_time = max(0, 30 - int(elapsed_time))  # Ensure no negative time
        self.draw_text(self.screen, f"Time: {remaining_time}s", 24, BLACK, WIDTH / 2 + 100, 10)

        pg.display.flip()

    def show_game_over_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "GAME OVER", 72, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text(self.screen, f"Your Score: {self.score}", 36, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press R to Restart or Q to Quit", 24, WHITE, WIDTH / 2, HEIGHT / 1.5)
        pg.display.flip()

        waiting = True
        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    playing = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.new()
                        playing = False
                    if event.key == pg.K_q:
                        self.running = False
                        playing = False

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()

