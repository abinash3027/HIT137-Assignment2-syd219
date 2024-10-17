import pygame
import random
from pygame.sprite import Sprite
from utils.functions import load_image

# Load assets
enemy_img = load_image('assets/enemy.png', 50, 70)

class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.movement_range = 100
        self.initial_x = x

    def update(self):
        self.rect.x += self.speed_x
        if abs(self.rect.x - self.initial_x) > self.movement_range:
            self.speed_x *= -1
