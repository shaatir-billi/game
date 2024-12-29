import pygame


class HidingSpot:
    def __init__(self, x, y, width, height, scale=1):
        self.image = pygame.image.load(
            'assets/menu/Grass1.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(width * scale), int(height * scale)))
        self.rect = pygame.Rect(x, y, int(width * scale), int(height * scale))
        self.font = pygame.font.Font(None, 24)  # Font for the message
        self.message = "Hidden!"  # Message to display
        self.message_surface = self.font.render(
            self.message, True, (255, 255, 255))  # Rendered message surface

    def draw(self, screen, camera, is_hidden):
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))
        if is_hidden:
            message_rect = self.message_surface.get_rect(
                center=(self.rect.x + self.rect.width // 2 - camera.x_offset, self.rect.y - 20))
            screen.blit(self.message_surface, message_rect)
