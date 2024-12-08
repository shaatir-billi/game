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
    frame_width=32,
    frame_height=32,
    scale=5
)

# Variables for jumping
gravity = 1
jump_force = -15
player_velocity_y = 0
is_jumping = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input for player movement
    keys = pygame.key.get_pressed()
    dx = 0

    if keys[pygame.K_a]:  # Move left
        dx = -5
        if not is_jumping:
            player.set_animation(5)  # Left movement animation
    elif keys[pygame.K_d]:  # Move right
        dx = 5
        if not is_jumping:
            player.set_animation(5)  # Right movement animation
    else:
        if not is_jumping:
            player.set_animation(1)  # Resting animation

    # Handle jumping
    if keys[pygame.K_w] and not is_jumping:
        player_velocity_y = jump_force
        is_jumping = True
        player.set_animation(7)  # Jump animation

    # Apply gravity
    player_velocity_y += gravity
    player.rect.y += player_velocity_y

    # Stop jumping when landing
    if player.rect.y >= 300:  # Ground level (adjust as needed)
        player.rect.y = 300
        player_velocity_y = 0
        is_jumping = False

    # Update player position and animation
    player.move(dx, 0)
    player.update()

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

    # Update the camera to follow the player
    camera.follow_sprite(player)

    # Draw everything
    game_map.draw(screen, camera)
    player.draw(screen, camera)

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
