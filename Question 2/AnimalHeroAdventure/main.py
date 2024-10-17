# main.py

import pygame
import sys
import random

# Initialize pygame and set up display before importing modules
pygame.init()

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, LEVEL_WIDTH, LEVEL_HEIGHT, DIFFICULTY_SETTINGS

# Set up the display and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animal Hero Adventure")
clock = pygame.time.Clock()

# Now import modules that load images
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.platform import Platform
from sprites.coin import Coin
from utils.functions import draw_gradient_background

def main_menu():
    font = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    # Buttons
    easy_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 250, 200, 50)
    medium_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 320, 200, 50)
    hard_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 390, 200, 50)
    about_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 460, 200, 50)  # About button

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    main_game('Easy')
                if medium_button.collidepoint(mouse_pos):
                    main_game('Medium')
                if hard_button.collidepoint(mouse_pos):
                    main_game('Hard')
                if about_button.collidepoint(mouse_pos):
                    about_screen()

        # Draw gradient background
        draw_gradient_background(screen)

        # Render Title
        title_text = font.render("Animal Hero Adventure", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))

        # Draw buttons
        # Easy button
        pygame.draw.rect(screen, (0, 255, 0), easy_button)
        easy_text = font_small.render("Easy", True, (0, 0, 0))
        screen.blit(easy_text, (easy_button.x + 75, easy_button.y + 10))
        # Medium button
        pygame.draw.rect(screen, (255, 255, 0), medium_button)
        medium_text = font_small.render("Medium", True, (0, 0, 0))
        screen.blit(medium_text, (medium_button.x + 60, medium_button.y + 10))
        # Hard button
        pygame.draw.rect(screen, (255, 0, 0), hard_button)
        hard_text = font_small.render("Hard", True, (0, 0, 0))
        screen.blit(hard_text, (hard_button.x + 75, hard_button.y + 10))
        # About button
        pygame.draw.rect(screen, (0, 0, 255), about_button)
        about_text = font_small.render("About", True, (255, 255, 255))
        screen.blit(about_text, (about_button.x + 70, about_button.y + 10))

        pygame.display.flip()

def about_screen():
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)

    # Prepare the text lines
    lines = [
        "Group Members:",
        "",
        "Name: Mohammed Sajid Salim",
        "Student ID: S372433",
        "",
        "Name: Abinash Kushwaha",
        "Student ID: S377464",
        "",
        "Name: Md. Iftakharul Alam Chowdhury",
        "Student ID: S372376",
        "",
        "Name: Albert Osemudiamhen Agbonkhese",
        "Student ID: S373500",
    ]

    # Back button
    back_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 70, 200, 50)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return  # Return to main menu

        # Draw gradient background
        draw_gradient_background(screen)

        # Calculate the total height of the text block
        line_height = 40
        total_text_height = line_height * len(lines)
        starting_y = (SCREEN_HEIGHT - total_text_height - back_button.height - 20) // 2  # 20 pixels space

        # Render the lines of text
        y_offset = starting_y
        for line in lines:
            text = font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_offset))
            y_offset += line_height  # Move down for the next line

        # Draw back button
        pygame.draw.rect(screen, (128, 128, 128), back_button)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_button.x + back_button.width//2 - back_text.get_width()//2,
                                back_button.y + back_button.height//2 - back_text.get_height()//2))

        pygame.display.flip()


def main_game(level_name):
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    # Create player instance
    player = Player()
    all_sprites.add(player)

    # Create level
    create_level(level_name, all_sprites, platforms, enemies, coins, player)

    # Camera variables
    camera_x = 0
    camera_y = 0

    font = pygame.font.SysFont(None, 30)

    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player controls
            if not player.is_dead:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    if event.key == pygame.K_RIGHT:
                        player.move_right()
                    if event.key == pygame.K_SPACE:
                        player.jump()
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT and player.speed_x < 0) or \
                       (event.key == pygame.K_RIGHT and player.speed_x > 0):
                        player.stop()

        # Update sprites
        player.update(platforms)
        enemies.update()
        coins.update()

        # Update camera position
        camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        camera_y = player.rect.centery - SCREEN_HEIGHT // 2

        # Limit camera scrolling to level size
        camera_x = max(0, min(camera_x, LEVEL_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, LEVEL_HEIGHT - SCREEN_HEIGHT))

        # Draw gradient background
        draw_gradient_background(screen)

        # Draw sprites
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

        # Check for coin collection
        coin_hits = pygame.sprite.spritecollide(player, coins, True)
        for coin in coin_hits:
            player.score += 10

        # Check for enemy collision
        enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
        if enemy_hits and not player.is_dead:
            player.health -= 1  # Decrease health upon touching enemy
            if player.health <= 0:
                player.lose_life()
                player.trigger_death()

        # Check if game over
        if player.game_over:
            game_over_screen()
            return  # Exit the main_game function

        # Display HUD
        display_hud(screen, font, player)

        # Update display
        pygame.display.flip()

    pygame.quit()

def create_level(level_name, all_sprites, platforms, enemies, coins, player):
    # Clear existing sprites
    all_sprites.empty()
    platforms.empty()
    enemies.empty()
    coins.empty()

    # Add player to all_sprites
    all_sprites.add(player)

    # Create ground platform
    ground = Platform(0, SCREEN_HEIGHT - 50, width=LEVEL_WIDTH, height=50)
    all_sprites.add(ground)
    platforms.add(ground)

    # Improved platform placement
    x = 0
    y = SCREEN_HEIGHT - 150
    last_platform_y = y
    for _ in range(50):
        x += random.randint(80, 150)
        y_variation = random.choice([-1, 1]) * random.randint(30, 60)
        y = last_platform_y + y_variation

        # Keep platforms within vertical bounds
        y = max(100, min(y, SCREEN_HEIGHT - 150))

        platform = Platform(x, y)
        all_sprites.add(platform)
        platforms.add(platform)

        last_platform_y = y

        # Stop generating platforms if we reach the level width
        if x > LEVEL_WIDTH - 200:
            break

    # Get enemy count based on difficulty level
    enemy_count = DIFFICULTY_SETTINGS[level_name]['enemy_count']

    # Create enemies on random platforms
    for _ in range(enemy_count):
        platform = random.choice(platforms.sprites())
        enemy = Enemy(platform.rect.x + random.randint(0, platform.rect.width - 50),
                      platform.rect.y - 70)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Create coins on random platforms
    for _ in range(25):
        platform = random.choice(platforms.sprites())
        coin = Coin(platform.rect.x + random.randint(0, platform.rect.width - 30),
                    platform.rect.y - 30)
        all_sprites.add(coin)
        coins.add(coin)

def display_hud(screen, font, player):
    lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(health_text, (10, 70))

    # Draw health bar
    max_health_bar_width = 100
    health_bar_width = (player.health / 100) * max_health_bar_width
    health_bar = pygame.Rect(10, 100, health_bar_width, 10)
    pygame.draw.rect(screen, (255, 0, 0), health_bar)
    pygame.draw.rect(screen, (255, 255, 255), (10, 100, max_health_bar_width, 10), 2)

def game_over_screen():
    font = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    # Buttons
    retry_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
    exit_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(mouse_pos):
                    main_menu()
                    return
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Draw gradient background
        draw_gradient_background(screen)

        # Render "Game Over" text
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2,
                                     SCREEN_HEIGHT//2 - 100))

        # Draw buttons
        # Retry button
        pygame.draw.rect(screen, (0, 128, 0), retry_button)
        retry_text = font_small.render("Retry", True, (255, 255, 255))
        screen.blit(retry_text, (retry_button.x + 70, retry_button.y + 10))
        # Exit button
        pygame.draw.rect(screen, (128, 0, 0), exit_button)
        exit_text = font_small.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (exit_button.x + 80, exit_button.y + 10))

        pygame.display.flip()

if __name__ == '__main__':
    main_menu()
