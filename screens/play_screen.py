import pygame
import sys
from sprite import Sprite
from map import *
from camera import Camera
from utils.globals import *


def play(SCREEN):
    game_map = GameMap("assets/map/sky.jpeg",
                       "assets/map/ground.png")
    camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), map_width)

    player = Sprite(
        sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
        x=100,
        y=game_map.ground_level - 150,  # Adjust to spawn above the ground
        frame_width=32,
        frame_height=32,
        scale=5,
        ground_level=game_map.ground_level  # Pass ground level to the sprite
    )

    # Create platforms
    platforms = [
        Platform("assets/map/platform.png", 300,
                 game_map.ground_level - 200, 200, 50),
        Platform("assets/map/platform.png", 600,
                 game_map.ground_level - 300, 200, 50),
        Platform("assets/map/platform.png", 900,
                 game_map.ground_level - 150, 200, 50),
    ]

    clock = pygame.time.Clock()

    while True:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a]:
            dx = -5
            player.set_animation(5)
        if keys[pygame.K_d]:
            dx = 5
            player.set_animation(5)

        if keys[pygame.K_w]:
            player.jump()

        player.move(dx, dy)

        # Handle platform collision and falling
        on_platform = False
        for platform in platforms:
            # Check if the player is on top of the platform
            if (
                player.rect.colliderect(platform.rect)
                and player.y_velocity >= 0  # Falling or standing still
                and player.rect.bottom <= platform.rect.top + 10  # Slight overlap allowed
                # Within horizontal bounds
                and platform.rect.left <= player.rect.centerx <= platform.rect.right
            ):
                player.rect.bottom = platform.rect.top
                player.is_jumping = False
                player.y_velocity = 0
                on_platform = True
                break

        # If the player is not on any platform, apply gravity
        if not on_platform and player.rect.bottom < game_map.ground_level:
            player.is_jumping = True

        player.update()

        camera.follow_sprite(player)
        game_map.draw(SCREEN, camera)

        # Draw platforms
        for platform in platforms:
            platform.draw(SCREEN, camera)

        player.draw(SCREEN, camera)

        pygame.display.flip()
        clock.tick(60)
