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

# Initialize the player sprite
player = Sprite("assets/sprites/player/attack_2.png",
                100, 300)  # Starts at y=300

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input for player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Move left
        player.move(-5, 0)
    if keys[pygame.K_d]:  # Move right
        player.move(5, 0)
    if keys[pygame.K_w]:  # Move up
        player.move(0, -5)
    if keys[pygame.K_s]:  # Move down
        player.move(0, 5)

    # Update the camera to follow the player
    camera.follow_sprite(player)

    game_map.draw(screen)  # Draw the repeating background
    player.draw(screen, camera)  # Draw the player

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
