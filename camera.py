class Camera:
    def __init__(self, screen_size, map_width):
        """
        Initialize the camera object.
        :param screen_size: The dimensions of the screen (width, height)
        :param map_width: The total width of the map in pixels
        """
        self.screen_width = screen_size[0]
        self.map_width = map_width
        self.x_offset = 0  # Initial horizontal offset

    def follow_sprite(self, sprite):
        """
        Center the camera horizontally on the sprite, clamped to the map bounds.
        :param sprite: The sprite to follow
        """
        target_x_offset = sprite.rect.centerx - self.screen_width // 2
        self.x_offset = max(
            0, min(target_x_offset, self.map_width - self.screen_width)
        )
