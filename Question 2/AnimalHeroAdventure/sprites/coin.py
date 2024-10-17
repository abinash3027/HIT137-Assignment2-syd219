import pygame
from pygame.sprite import Sprite
from utils.functions import load_image

# Load assets
coin_img = load_image('assets/coin.png', 30, 30)

class Coin(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
