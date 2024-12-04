import pygame
from globals import *


class Sprite:
    def __init__(self, image_path, x, y):
        # Load the sprite image and set its position
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera):
        # Draw the sprite adjusted for the camera's horizontal position
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))

    def move(self, dx, dy):
        # Move the sprite by a given amount
        self.rect.x += dx
        self.rect.y += dy
