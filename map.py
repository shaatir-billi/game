import pygame
import math
from globals import *


class GameMap:
    def __init__(self, sky_image_path):
        """
        Initialize the game map.
        :param sky_image_path: Path to the background image
        """
        # Load and scale the background image
        self.sky_image = pygame.image.load(sky_image_path).convert()
        self.sky_image = pygame.transform.scale(
            self.sky_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.sky_width = self.sky_image.get_width()

    def draw(self, screen):
        """
        Draw the map's repeating background based on the screen width.
        :param screen: The game window surface to draw on
        """
        tiles = math.ceil(SCREEN_WIDTH / self.sky_width) + 1

        # Draw the background repeatedly to cover the screen width
        for x in range(0, tiles):
            screen.blit(self.sky_image, (x * self.sky_width, 0))
