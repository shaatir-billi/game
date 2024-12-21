import pygame
import math
from utils.globals import SCREEN_WIDTH, SCREEN_HEIGHT, map_width


class GameMap:
    def __init__(self, sky_image_path, upper_layer_image_path):
        """
        Initialize the game map.
        :param sky_image_path: Path to the background image
        :param upper_layer_image_path: Path to the upper layer image
        :param building_image_path: Path to the building/ground image
        """
        # Load and scale the background image
        self.sky_image = pygame.image.load(sky_image_path).convert()
        self.sky_image = pygame.transform.scale(
            self.sky_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.sky_width = self.sky_image.get_width()

        # Load and scale the upper layer image
        self.upper_layer_image = pygame.image.load(
            upper_layer_image_path).convert_alpha()
        self.upper_layer_image = pygame.transform.scale(
            self.upper_layer_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.upper_layer_width = self.upper_layer_image.get_width()

        self.ground_tile_height = 50  # Height of the ground tile
        self.ground_level = SCREEN_HEIGHT - self.ground_tile_height  # Ground level

    def draw(self, screen, camera):
        """
        Draw the map's repeating background, upper layer, and ground.
        :param screen: The game window surface to draw on
        :param camera: The camera for horizontal scrolling
        """
        tiles_sky = math.ceil(map_width / self.sky_width)
        tiles_upper = math.ceil(map_width / self.upper_layer_width)

        # Draw the background considering camera's offset
        for x in range(0, tiles_sky):
            screen.blit(self.sky_image,
                        ((x * self.sky_width) - camera.x_offset, 0))

        # Draw the upper layer considering camera's offset
        for x in range(0, tiles_upper):
            screen.blit(self.upper_layer_image,
                        ((x * self.upper_layer_width) - camera.x_offset, 0))


class Platform:
    def __init__(self, image_path, x, y, width, height):
        """
        Initialize the platform.
        :param image_path: Path to the platform image
        :param x: x-coordinate of the platform
        :param y: y-coordinate of the platform
        :param width: Width of the platform
        :param height: Height of the platform
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera):
        """
        Draw the platform on the screen with camera adjustment.
        :param screen: The game window
        :param camera: Camera object
        """
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))
