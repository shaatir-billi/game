import pygame

class Sprite:
    def __init__(self, image_path, x, y):
        # Load the sprite image and set its position
        self.image = pygame.image.load(image_path).convert_alpha()  # Load image with transparency
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Set the initial position of the sprite

    def draw(self, screen, camera):
        # Draw the sprite adjusted for the camera's position
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y - camera.y_offset))

    def move(self, dx, dy):
        # Move the sprite by a given amount
        self.rect.x += dx
        self.rect.y += dy
