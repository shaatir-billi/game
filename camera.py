class Camera:
    def __init__(self, screen_size, map_width, map_height, tile_size):
        """
        Initialize the camera object.
        :param screen_size: The dimensions of the screen (width, height)
        :param map_width: The number of tiles in the map's width
        :param map_height: The number of tiles in the map's height
        :param tile_size: The size of each tile in pixels
        """
        self.screen_width, self.screen_height = screen_size  # Screen dimensions in pixels
        self.map_width = map_width * tile_size  # Total map width in pixels
        self.map_height = map_height * tile_size  # Total map height in pixels
        # Initial camera position (top-left corner)
        self.x_offset, self.y_offset = 0, 0

    def move(self, dx, dy):
        """
        Move the camera by a specified amount.
        :param dx: Amount to move in the x-direction
        :param dy: Amount to move in the y-direction
        """
        # Adjust the camera's position
        self.x_offset += dx
        self.y_offset += dy

        # Clamp the camera position to ensure it doesn't go out of bounds
        self.x_offset = max(
            0, min(self.x_offset, self.map_width - self.screen_width))
        self.y_offset = max(
            0, min(self.y_offset, self.map_height - self.screen_height))
        
        
    def follow_sprite(self, sprite):
        # Calculate the potential offsets to center the sprite
        target_x_offset = sprite.rect.centerx - self.screen_width // 2
        target_y_offset = sprite.rect.centery - self.screen_height // 2

        # Clamp the x_offset, ensuring the entire sprite remains visible
        self.x_offset = max(0, min(target_x_offset, self.map_width - self.screen_width))

        # Ensure the right edge of the sprite doesn’t go off-screen
        if sprite.rect.right > self.map_width:
            self.x_offset = self.map_width - self.screen_width

        # Clamp the y_offset similarly
        self.y_offset = max(0, min(target_y_offset, self.map_height - self.screen_height))


