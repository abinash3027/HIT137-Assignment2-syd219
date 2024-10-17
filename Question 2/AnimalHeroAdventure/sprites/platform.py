import pygame
from pygame.sprite import Sprite

class Platform(Sprite):
    def __init__(self, x, y, width=100, height=20):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((139, 69, 19))  # Brown color for the platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
