import pygame

class Fish():
    def __init__(self, sprite_sheet_path, frame_width, frame_height, scale=1):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.scaled_width = int(frame_width * scale * 0.5)  # Adjust scaling to a reasonable size
        self.scaled_height = int(frame_height * scale * 0.5)

        self.frames = self._load_frames()
        self.current_frame = 0
        self.animation_speed = 0.1
        self.timer = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

    def _load_frames(self):
        frames = []
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()
        num_cols = sheet_width // self.frame_width
        num_rows = sheet_height // self.frame_height

        for row in range(num_rows):
            for col in range(num_cols):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(x, y, self.frame_width, self.frame_height))
                scaled_frame = pygame.transform.scale(
                    frame, (self.scaled_width, self.scaled_height))
                frames.append(scaled_frame)
        return frames

    def update(self):
        self.timer += self.animation_speed
        if self.timer >= 1:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        self.image = self.frames[self.current_frame]

    def draw(self, screen, x, y, debug=False):
        self.rect.topleft = (x, y)
        screen.blit(self.image, self.rect)

        # Optional: Draw debug rectangle to see the boundaries of the scaled fish
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)  # Red border
