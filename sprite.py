import pygame


class Sprite:
    def __init__(self, sprite_sheet_path, x, y, frame_width, frame_height, scale=1):
        """
        Initialize the sprite.
        :param sprite_sheet_path: Path to the sprite sheet
        :param x: Initial x position
        :param y: Initial y position
        :param frame_width: Width of each frame in the sprite sheet
        :param frame_height: Height of each frame in the sprite sheet
        :param scale: Scaling factor for the sprite
        """
        self.sprite_sheet = pygame.image.load(
            sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.scaled_width = int(frame_width * scale)
        self.scaled_height = int(frame_height * scale)

        self.frames = self._load_frames()
        self.current_row = 0
        self.current_frame = 0
        self.animation_speed = 0.15
        self.timer = 0

        self.image = self.frames[self.current_row][self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_moving = False  # Flag to track movement

    def _load_frames(self):
        """
        Load and scale all frames from the sprite sheet.
        :return: List of rows, each containing scaled frames.
        """
        rows = []
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()
        num_cols = sheet_width // self.frame_width
        num_rows = sheet_height // self.frame_height

        for row in range(num_rows):
            frames = []
            for col in range(num_cols):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(x, y, self.frame_width, self.frame_height))
                scaled_frame = pygame.transform.scale(
                    frame, (self.scaled_width, self.scaled_height))
                frames.append(scaled_frame)
            rows.append(frames)
        return rows

    def set_animation(self, row):
        """
        Set the animation row only if it is different from the current row.
        :param row: Row index for the animation in the sprite sheet
        """
        if self.current_row != row:
            self.current_row = row
            self.current_frame = 0  # Reset animation to the first frame

    def update(self):
        """
        Update the sprite's animation frame.
        """
        self.timer += self.animation_speed
        if self.timer >= 1:
            self.timer = 0
            self.current_frame = (self.current_frame +
                                  1) % len(self.frames[self.current_row])
        self.image = self.frames[self.current_row][self.current_frame]

    def move(self, dx, dy):
        """
        Move the sprite and set movement state.
        :param dx: Horizontal movement
        :param dy: Vertical movement
        """
        self.rect.x += dx
        self.rect.y += dy
        self.is_moving = dx != 0 or dy != 0  # Update movement state

    def draw(self, screen, camera):
        """
        Draw the sprite on the screen with camera adjustment.
        :param screen: The game window
        :param camera: Camera object
        """
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))
