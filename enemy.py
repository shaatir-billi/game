import pygame
import random

class Enemy:
    def __init__(self, sprite_sheet_path, x, y, frame_width, frame_height, scale=1):
        self.sprite_sheet_path = sprite_sheet_path
        self.x = x
        self.y = y
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.scaled_width = int(frame_width * scale)
        self.scaled_height = int(frame_height * scale)

        # Load sprite sheet and frames
        self.sprite_sheet = pygame.image.load(self.sprite_sheet_path).convert_alpha()
        self.frames = self._load_frames()

        self.current_row = 4  # Fixed to 5th row for walking animation (index 4)
        self.current_frame = 0
        self.animation_speed = 0.15
        self.timer = 0

        # Movement control
        self.start_timer = 0  # Timer to delay movement
        self.movement_started = False
        self.speed = 2  # Speed of walking

        # Direction control
        self.direction = random.choice(["right", "left"])  # Random direction at start
        
        # Initialize image and rect
        self.image = self.frames[self.current_row][self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def _load_frames(self):
        """
        Load and scale all frames from the sprite sheet.
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
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                scaled_frame = pygame.transform.scale(frame, (self.scaled_width, self.scaled_height))
                frames.append(scaled_frame)
            rows.append(frames)
        return rows

    def update(self, dt):
        """
        Start movement after 2 seconds and play walking animation.
        """
        self.start_timer += dt  # Timer for delay

        if not self.movement_started and self.start_timer >= 2:
            self.movement_started = True

        if self.movement_started:
            # Move the enemy in the current direction
            if self.direction == "right":
                self.x += self.speed
            else:
                self.x -= self.speed

            # Update animation frames only for the 5th row (walking animation)
            self.timer += self.animation_speed
            if self.timer >= 1:
                self.timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.current_row])

            # Update the current image
            self.image = self.frames[self.current_row][self.current_frame]

            # Flip the image if moving left
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)
            
            # Update the rect position
            self.rect.x = self.x

            # Optionally change direction randomly after each movement
            if random.random() < 0.01:  # 1% chance to change direction
                self.direction = random.choice(["right", "left"])

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y - camera.y))
