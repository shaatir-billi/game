import pygame
from globals import *


class Sprite:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera):
        # Adjust the sprite's position based on the camera
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))

    def move(self, dx, dy):
        # Move the sprite, clamping within the extended map bounds
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Clamp horizontal movement within the map
        if 0 <= new_x <= map_width - self.rect.width:
            self.rect.x = new_x

        # Clamp vertical movement to the screen height
        if new_y >= 0:
            self.rect.y = new_y
