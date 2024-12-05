import pygame
from map import GameMap
from sprite import Sprite
from camera import Camera
from globals import *

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shaatir Billi")

# Clock to control frames per second (FPS)
clock = pygame.time.Clock()

# Initialize the game map and camera
game_map = GameMap(sky_image_path)
camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), map_width)

player = Sprite(
    sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
    x=100,
    y=300,
    frame_width=32,  # Replace with your frame's width
    frame_height=32,  # Replace with your frame's height
    scale=5
)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input for player movement
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_a]:  # Move left
        dx = -5
        player.set_animation(5)  # Set the animation row for left movement
    if keys[pygame.K_d]:  # Move right
        dx = 5
        player.set_animation(5)  # Set the animation row for right movement
    if keys[pygame.K_w]:  # Move up
        dy = -5
        player.set_animation(9)  # Set the animation row for up movement
    if keys[pygame.K_s]:  # Move down
        dy = 5
        player.set_animation(9)

    player.move(dx, dy)
    player.update()  # Update animation frame

    # Check if the sprite falls below the screen
    if player.rect.y > SCREEN_HEIGHT:
        screen.fill((255, 0, 0))  # Red screen for game over
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                           SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    camera.follow_sprite(player)  # Update camera position
    game_map.draw(screen, camera)  # Draw the map
    player.draw(screen, camera)  # Draw the player

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
