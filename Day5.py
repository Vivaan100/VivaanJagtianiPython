# This file was created by: Vivaan Jagtiani

# this code was created by: ChatGPT

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
player_img = pygame.Surface((50, 30))
player_img.fill(WHITE)
bullet_img = pygame.Surface((5, 15))
bullet_img.fill(RED)
enemy_img = pygame.Surface((50, 30))
enemy_img.fill(RED)

# Game variables
player_pos = [WIDTH // 2, HEIGHT - 50]
player_speed = 5
bullet_speed = 7
enemy_speed = 2
bullets = []
enemies = [[random.randint(0, WIDTH - 50), random.randint(-150, -50)] for _ in range(5)]

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE]:
        bullets.append([player_pos[0] + 22, player_pos[1]])

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
    bullets = [b for b in bullets if b[1] > 0]

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemy[0] = random.randint(0, WIDTH - 50)
            enemy[1] = random.randint(-150, -50)
    
    # Check for collisions
    for bullet in bullets:
        for enemy in enemies:
            if (bullet[0] in range(enemy[0], enemy[0] + 50) and 
                bullet[1] in range(enemy[1], enemy[1] + 30)):
                enemies.remove(enemy)
                bullets.remove(bullet)
                enemies.append([random.randint(0, WIDTH - 50), random.randint(-150, -50)])
                break

    # Draw everything
    screen.fill(BLACK)
    screen.blit(player_img, player_pos)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    
    pygame.display.flip()
    clock.tick(30)