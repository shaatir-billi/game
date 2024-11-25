import pygame


class GameMap:
    def __init__(self, width, height, tile_size, grass_color, dirt_color):
        """
        Initialize the game map.
        :param width: Number of tiles in width
        :param height: Number of tiles in height
        :param tile_size: Size of each tile in pixels (square)
        :param grass_color: Color of the grass tiles
        :param dirt_color: Color of the dirt tiles
        """
        self.width = width  # Width of the map in tiles
        self.height = height  # Height of the map in tiles
        self.tile_size = tile_size  # Pixel size of each square tile
        self.grass_color = grass_color  # Color used for grass tiles
        self.dirt_color = dirt_color  # Color used for dirt tiles

    def draw(self, screen, camera):
        """
        Draw the map on the screen.
        :param screen: The game window surface to draw on
        :param camera: The camera object to adjust tile positions
        """
        # Loop through all tiles in the map
        for row in range(self.height):
            for col in range(self.width):
                # Alternate between grass and dirt tiles
                color = self.grass_color if (
                    row + col) % 2 == 0 else self.dirt_color

                # Calculate the position of the tile relative to the camera
                rect = pygame.Rect(
                    col * self.tile_size - camera.x_offset,  # X position
                    row * self.tile_size - camera.y_offset,  # Y position
                    self.tile_size,  # Tile width
                    self.tile_size,  # Tile height
                )

                # Draw the tile as a filled rectangle
                pygame.draw.rect(screen, color, rect)
