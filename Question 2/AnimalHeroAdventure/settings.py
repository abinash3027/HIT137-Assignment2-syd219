import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Level dimensions
LEVEL_WIDTH = 3000
LEVEL_HEIGHT = SCREEN_HEIGHT

# Difficulty levels
DIFFICULTY_SETTINGS = {
    'Easy': {'enemy_count': 10},
    'Medium': {'enemy_count': 20},
    'Hard': {'enemy_count': 30},
}
