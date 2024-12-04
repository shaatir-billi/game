class Camera:
    def __init__(self, screen_size, map_width):
        """
        Initialize the camera object.
        :param screen_size: The dimensions of the screen (width, height)
        :param map_width: The total width of the map in pixels
        """

        self.screen_width = screen_size[0]  # Screen width in pixels
        self.map_width = map_width  # Total map width in pixels
        self.x_offset = 0  # Initial horizontal offset
        self.y_offset = 0  # Vertical offset remains fixed

    def move(self, dx):
        """
        Move the camera horizontally.
        :param dx: Amount to move in the x-direction
        """
        self.x_offset += dx

        # Clamp the camera's x_offset to prevent scrolling out of bounds
        self.x_offset = max(
            0, min(self.x_offset, self.map_width - self.screen_width))

    def follow_sprite(self, sprite):
        """
        Center the camera horizontally on the sprite, clamped to the map bounds.
        :param sprite: The sprite to follow
        """
        target_x_offset = sprite.rect.centerx - self.screen_width // 2
        self.x_offset = max(
            0, min(target_x_offset, self.map_width - self.screen_width))
