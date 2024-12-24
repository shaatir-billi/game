import pygame
from utils.globals import SCREEN_HEIGHT
from screens.game_over_screen import game_over


class Sprite:
    def __init__(self, sprite_sheet_path, x, y, frame_width, frame_height, scale=1, ground_level=SCREEN_HEIGHT):
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
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_rect = self.rect.inflate(
            -self.rect.width * 0.3, -self.rect.height * 0.3)
        self.is_moving = False
        self.is_jumping = False
        self.jump_velocity = -20  # Improved jump velocity for smoother arc
        self.gravity = 1.2  # Adjusted gravity for better jump
        self.max_fall_speed = 15  # Limit falling speed
        self.y_velocity = 0
        self.ground_level = ground_level

        self.health = 5
        self.is_invincible = False
        self.invincibility_timer = 0
        self.blink_interval = 200  # milliseconds
        self.blink_timer = 0
        self.visible = True
        self.is_hidden = False

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
            # Set animation speed to zero if idle
            if row == 0:  # Assuming row 0 is the idle animation
                self.animation_speed = 0
            else:
                self.animation_speed = 0.15

    def update(self, delta_time=0):
        self.timer += self.animation_speed
        if self.timer >= 1:
            self.timer = 0
            self.current_frame = (self.current_frame +
                                  1) % len(self.frames[self.current_row])

        frame = self.frames[self.current_row][self.current_frame]
        if self.flipped:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

        if self.is_jumping:
            self.y_velocity = min(
                self.y_velocity + self.gravity, self.max_fall_speed)
            self.rect.y += self.y_velocity

            # Check for landing
            if self.rect.bottom >= self.ground_level:
                self.rect.bottom = self.ground_level
                self.is_jumping = False
                self.y_velocity = 0
        else:
            self.y_velocity = 0  # Reset y-velocity when not jumping

        if self.is_invincible:
            self.invincibility_timer -= delta_time
            self.blink_timer += delta_time
            if self.blink_timer >= self.blink_interval:
                self.visible = not self.visible
                self.blink_timer = 0
            if self.invincibility_timer <= 0:
                self.is_invincible = False
                self.visible = True

        self.collision_rect.topleft = self.rect.topleft

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = self.jump_velocity
            self.set_animation(8)  # Set to jump animation row

    def move(self, dx, dy):
        if not self.is_hidden:
            self.rect.x += dx
            self.rect.y += dy
            self.is_moving = dx != 0
            if dx < 0:
                self.flipped = True
            elif dx > 0:
                self.flipped = False

            if self.is_moving and not self.is_jumping:
                self.set_animation(5)  # Set to walking animation
            elif not self.is_moving and not self.is_jumping:
                self.set_animation(0)  # Set to idle animation

            self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen, camera):
        if self.visible:
            screen.blit(self.image, (self.rect.x -
                        camera.x_offset, self.rect.y))

    def take_damage(self):
        if not self.is_invincible and not self.is_hidden:
            self.health -= 1
            self.set_invincible()
            if self.health <= 0:
                self.die()

    def set_invincible(self):
        self.is_invincible = True
        self.invincibility_timer = 4000  # 4 seconds
        self.blink_timer = 0

    def die(self):
        # Gane over logic
        from screens.play_screen import play
        game_over(pygame.display.get_surface(), play)

    def hide(self):
        self.is_hidden = True
        self.visible = False

    def unhide(self):
        self.is_hidden = False
        self.visible = True
