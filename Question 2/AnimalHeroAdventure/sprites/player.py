import pygame
from pygame.sprite import Sprite
from settings import SCREEN_HEIGHT, LEVEL_HEIGHT
from utils.functions import load_image

# Load assets
player_img_right = load_image('assets/player_right.png', 50, 50)
player_img_left = load_image('assets/player_left.png', 50, 50)

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img_right
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_power = -12  # Regular jump
        self.long_jump_power = -16  # Long jump
        self.lives = 3
        self.health = 100  # Health starts at 100
        self.score = 0
        self.facing_right = True
        self.on_ground = False
        self.can_double_jump = False
        self.last_jump_time = 0
        self.is_dead = False
        self.death_timer = 0
        self.death_duration = 1000  # Duration of death animation in milliseconds
        self.game_over = False  # Initialize game over flag

    def update(self, platforms):
        if self.is_dead:
            current_time = pygame.time.get_ticks()
            if current_time - self.death_timer >= self.death_duration:
                self.is_dead = False
                self.respawn()
            return  # Skip the rest of the update while dead

        self.apply_gravity()
        self.handle_movement(platforms)
        self.check_world_bounds()
        self.update_image_direction()

    def apply_gravity(self):
        self.speed_y += self.gravity
        if self.speed_y > 10:
            self.speed_y = 10

    def handle_movement(self, platforms):
        # Move horizontally
        self.rect.x += self.speed_x
        self.check_horizontal_collisions(platforms)

        # Move vertically
        self.rect.y += self.speed_y
        self.check_vertical_collisions(platforms)

    def jump(self):
        current_time = pygame.time.get_ticks()
        if self.on_ground:
            self.speed_y = self.jump_power
            self.on_ground = False
            self.can_double_jump = True
            self.last_jump_time = current_time
        elif self.can_double_jump and current_time - self.last_jump_time < 500:
            self.speed_y = self.long_jump_power
            self.can_double_jump = False

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0

    def check_horizontal_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.speed_x > 0:
                self.rect.right = platform.rect.left
            elif self.speed_x < 0:
                self.rect.left = platform.rect.right

    def check_vertical_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.on_ground = False
        for platform in hits:
            if self.speed_y > 0:
                self.rect.bottom = platform.rect.top
                self.speed_y = 0
                self.on_ground = True
                self.can_double_jump = False
            elif self.speed_y < 0:
                self.rect.top = platform.rect.bottom
                self.speed_y = 0

    def check_world_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > LEVEL_HEIGHT:
            self.lose_life()
            self.trigger_death()

    def lose_life(self):
        self.lives -= 1
        self.health = 100  # Reset health upon losing a life
        if self.lives <= 0:
            self.game_over = True  # Set game over flag

    def respawn(self):
        # Player respawns at the starting position
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        self.speed_x = 0
        self.speed_y = 0
        self.health = 100

    def trigger_death(self):
        self.is_dead = True
        self.death_timer = pygame.time.get_ticks()

    def update_image_direction(self):
        if self.speed_x > 0:
            self.image = player_img_right
            self.facing_right = True
        elif self.speed_x < 0:
            self.image = player_img_left
            self.facing_right = False
