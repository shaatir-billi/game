import pygame
from utils.globals import SCREEN_HEIGHT

# Guards cannot jump. They will remain on the same platform.


class Guard():
    def __init__(
        self, sprite_sheet_path, platform_rect, frame_width, frame_height, scale=1
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

        self.image = self.frames[self.current_row][self.current_frame]
        self.platform_rect = platform_rect
        self.rect = self.image.get_rect(
            topleft=(platform_rect.left, platform_rect.top - self.scaled_height))
        self.is_moving = False
        self.horizontal_velocity = 1  # Initial horizontal velocity
        self.collision_rect = self.rect.inflate(
            -self.rect.width * 0.5, -self.rect.height * 0.5)

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

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.is_moving = True
        if dx < 0:
            self.flipped = True
        elif dx > 0:
            self.flipped = False

        # Ensure the guard stays within the platform bounds
        if self.rect.left < self.platform_rect.left:
            self.rect.left = self.platform_rect.left
        elif self.rect.right > self.platform_rect.right:
            self.rect.right = self.platform_rect.right
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))
