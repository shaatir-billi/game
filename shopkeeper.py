import pygame
from utils.globals import SCREEN_HEIGHT


class Shopkeeper():
    def __init__(
        self, sprite_sheet_path, frame_width, frame_height, scale=1, ground_level=SCREEN_HEIGHT
    ):
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
        self.flipped = False
        self.moving_right = True  # Add moving_right attribute

        self.image = self.frames[self.current_row][self.current_frame]
        self.rect = self.image.get_rect()
        self.is_moving = False
        self.horizontal_velocity = 1  # Initial horizontal velocity
        self.collision_rect = self.rect.inflate(
            -self.rect.width * 0.5, -self.rect.height * 0.5)
        self.is_jumping = False
        self.jump_velocity = -20
        self.gravity = 1.2
        self.max_fall_speed = 15
        self.y_velocity = 0
        self.ground_level = ground_level

    def _load_frames(self):
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
        if self.current_row != row:
            self.current_row = row
            self.current_frame = 0

    def update(self):
        self.timer += self.animation_speed
        if self.timer >= 1:
            self.timer = 0
            self.current_frame = (self.current_frame +
                                  1) % len(self.frames[self.current_row])

        frame = self.frames[self.current_row][self.current_frame]
        if self.flipped:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame
        self.collision_rect.topleft = self.rect.topleft

        # Check if the shopkeeper is in the jumping state
        if self.is_jumping:
            # Apply gravity to the vertical velocity, but do not exceed the max fall speed
            self.y_velocity = min(
                self.y_velocity + self.gravity, self.max_fall_speed)
            # Update the vertical position based on the vertical velocity
            self.rect.y += self.y_velocity

            # Check if the shopkeeper has landed on the ground
            if self.rect.bottom >= self.ground_level:
                # Snap the shopkeeper to the ground level
                self.rect.bottom = self.ground_level
                # End the jumping state
                self.is_jumping = False
                # Reset the vertical velocity
                self.y_velocity = 0

            else:
                # Reset the vertical velocity when not jumping
                self.y_velocity = 0

    def move(self, dx, dy):
        # Update the horizontal position based on the horizontal velocity
        self.rect.x += dx
        # Update the vertical position based on the vertical velocity
        self.rect.y += dy
        # Set the moving state to True
        self.is_moving = True
        # Check the direction of movement to flip the sprite accordingly
        if dx < 0:
            self.flipped = True
        elif dx > 0:
            self.flipped = False

        # Update the collision rectangle's position to match the sprite's position
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))
